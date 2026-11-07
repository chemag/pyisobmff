import io
import unittest

import isobmff
from isobmff.vvc import (
    VVCConfigurationBox,
    VVCSampleEntry,
    VVCInBandSampleEntry,
)
from isobmff.box import read_box
from tests.common import box, parse, visual_sample_entry


def vvcc(record, version=0, flags=0):
    return box(b"vvcC", bytes([version]) + flags.to_bytes(3, "big") + record)


def one_sublayer():
    return bytes.fromhex(
        "ff 00 15 5f 01 02 40 80 00 07 80 04 38 00 00 02 "
        "8f 00 01 00 03 00 79 80 90 00 01 00 03 00 81 80"
    )


def multiple_sublayers():
    return bytes.fromhex(
        "ff 80 b9 5f 02 02 40 d5 ab 80 30 02 "
        "01 02 03 04 a1 b2 c3 d4 07 80 04 38 00 00 07 "
        "0c 00 03 00 61 80 8d 00 03 00 69 80 "
        "8e 00 01 00 03 00 71 80 "
        "8f 00 01 00 03 00 79 80 90 00 01 00 03 00 81 80 "
        "17 00 01 00 03 00 b9 80 18 00 01 00 03 00 c1 80"
    )


class VVCTest(unittest.TestCase):
    def test_registered(self):
        self.assertTrue({b"vvc1", b"vvi1", b"vvcC"} <= isobmff.get_atom_list())

    def test_no_ptl(self):
        parsed, _ = parse(vvcc(b"\xfe\x00"))
        self.assertIsInstance(parsed, VVCConfigurationBox)
        self.assertEqual(parsed.version, 0)
        self.assertEqual(parsed.flags, 0)
        self.assertEqual(parsed.vvc_config.length_size_minus_one, 3)
        self.assertEqual(parsed.vvc_config.ptl_present_flag, 0)
        self.assertEqual(parsed.vvc_config.array, [])
        self.assertFalse(hasattr(parsed.vvc_config, "max_picture_width"))

    def test_one_sublayer_configuration(self):
        parsed, stream = parse(vvcc(one_sublayer()))
        record = parsed.vvc_config
        self.assertEqual((record.ols_idx, record.num_sublayers), (0, 1))
        self.assertEqual(record.bit_depth, 10)
        self.assertEqual(record.general_profile_idc, 1)
        self.assertEqual(record.general_level_idc, 64)
        self.assertEqual(record.constraint_info_bytes, b"\x80")
        self.assertEqual(record.general_constraint_info_bit_count, 6)
        self.assertEqual(record.general_constraint_info, 0)
        self.assertEqual(
            (record.max_picture_width, record.max_picture_height), (1920, 1080)
        )
        self.assertEqual([a["nal_unit_type"] for a in record.array], [15, 16])
        self.assertEqual(record.array[0]["nal_units"], [b"\x00\x79\x80"])
        self.assertEqual(stream.tell(), len(stream.getvalue()))
        self.assertIn("general_level_idc: 64", repr(parsed))

    def test_conditionals_and_singleton_arrays(self):
        parsed, _ = parse(vvcc(multiple_sublayers()))
        record = parsed.vvc_config
        self.assertEqual((record.ols_idx, record.num_sublayers), (257, 3))
        self.assertEqual(record.general_constraint_info_bit_count, 14)
        self.assertEqual(record.general_constraint_info, 0x15AB)
        self.assertEqual(record.ptl_sublayer_level_present_flag, {1: 1, 0: 0})
        self.assertEqual(record.sublayer_level_idc, {1: 48})
        self.assertEqual(
            record.general_sub_profile_idc, [0x01020304, 0xA1B2C3D4]
        )
        self.assertEqual(
            [a["nal_unit_type"] for a in record.array],
            [12, 13, 14, 15, 16, 23, 24],
        )
        self.assertEqual(record.array[0]["num_nalus"], 1)
        self.assertEqual(record.array[1]["num_nalus"], 1)

    def test_sublayer_flag_alignment(self):
        for flag_byte, levels in (
            (0x40, {0: 32}),
            (0x80, {1: 48}),
            (0xC0, {1: 48, 0: 32}),
        ):
            prefix = bytes.fromhex("ff 00 35 5f 01 02 40 80")
            suffix = (
                bytes([flag_byte])
                + bytes(levels.values())
                + bytes.fromhex("00 07 80 04 38 00 00 00")
            )
            parsed, _ = parse(vvcc(prefix + suffix))
            self.assertEqual(parsed.vvc_config.sublayer_level_idc, levels)

    def test_constraint_sizes_not_limited_to_ffmpeg_storage(self):
        for size in (1, 2, 9, 63):
            prefix = bytes.fromhex("ff 00 15 5f") + bytes([size, 2, 64])
            raw = b"\x80" + b"\xab" * (size - 1)
            suffix = bytes.fromhex("00 07 80 04 38 00 00 00")
            parsed, _ = parse(vvcc(prefix + raw + suffix))
            self.assertEqual(parsed.vvc_config.constraint_info_bytes, raw)
            self.assertEqual(
                parsed.vvc_config.general_constraint_info_bit_count,
                8 * size - 2,
            )

    def test_both_sample_entries(self):
        config = vvcc(one_sublayer())
        sibling = box(b"pasp", b"\x00\x00\x00\x01" * 2)
        for fourcc, kind in (
            (b"vvc1", VVCSampleEntry),
            (b"vvi1", VVCInBandSampleEntry),
        ):
            parsed, _ = parse(visual_sample_entry(fourcc, config + sibling))
            self.assertIsInstance(parsed, kind)
            self.assertEqual(
                [b.box_type for b in parsed.box_list], [b"vvcC", b"pasp"]
            )

    def test_truncation_at_every_record_offset(self):
        for size in range(len(multiple_sublayers())):
            data = vvcc(multiple_sublayers()[:size])
            stream = io.BytesIO(data + box(b"free", bytes(4)))
            with self.assertRaises(EOFError):
                read_box(stream, "", 0)
            self.assertEqual(stream.tell(), len(data))
            self.assertEqual(read_box(stream, "", 0).box_type, b"free")

    def test_truncated_fullbox_header_preserves_sibling(self):
        for size in range(4):
            data = box(b"vvcC", bytes(size))
            stream = io.BytesIO(data + box(b"free", bytes(4)))
            with self.assertRaises(EOFError):
                read_box(stream, "", 0)
            self.assertEqual(stream.tell(), len(data))
            self.assertEqual(read_box(stream, "", 0).box_type, b"free")

    def test_unknown_version_and_flags_preserved(self):
        for version, flags in ((1, 0), (0, 1)):
            parsed, _ = parse(vvcc(b"future", version, flags))
            self.assertIsNone(parsed.vvc_config)
            self.assertEqual(parsed.unsupported_data, b"future")
            self.assertIn("unsupported_data", repr(parsed))

    def test_truncated_unsupported_payload(self):
        for version, flags in ((1, 0), (0, 1)):
            data = vvcc(b"future", version, flags)[:-2]
            with self.assertRaises(EOFError):
                read_box(io.BytesIO(data), "", 0)

    def test_reserved_fields_and_zero_constraints(self):
        for record in (
            b"\x00\x00",
            bytes.fromhex("ff 00 15 40 01 02 40 80 00"),
            bytes.fromhex("ff 00 15 5f 00 02 40 00"),
            bytes.fromhex("ff 00 35 5f 01 02 40 80 02 00"),
            bytes.fromhex("fe 01 af 00 00"),
        ):
            with self.assertRaises(ValueError):
                parse(vvcc(record))

    def test_unknown_array_type_multiple_nalus_and_tail(self):
        record = bytes.fromhex("fe 01 9f 00 02 00 01 aa 00 02 bb cc") + b"tail"
        parsed, _ = parse(vvcc(record))
        self.assertEqual(parsed.vvc_config.array[0]["nal_unit_type"], 31)
        self.assertEqual(
            parsed.vvc_config.array[0]["nal_units"], [b"\xaa", b"\xbb\xcc"]
        )
        self.assertEqual(parsed.vvc_config.trailing_data, b"tail")

    def test_oversized_nal_length(self):
        with self.assertRaises(EOFError):
            parse(vvcc(bytes.fromhex("fe 01 8f 00 01 ff ff 00")))


if __name__ == "__main__":
    unittest.main()
