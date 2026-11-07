import io
import unittest

import isobmff
from isobmff.evc import EVCConfigurationBox, EVCSampleEntry
from isobmff.box import read_box
from tests.common import box, parse, visual_sample_entry


def minimal():
    return bytes.fromhex(
        "01 00 1e 00 00 00 00 00 00 00 00 40 00 40 00 40 03 00"
    )


def main_profile():
    return bytes.fromhex(
        "01 01 3c 01 23 45 67 89 ab cd ef 52 07 80 04 38 03 04 "
        "98 00 01 00 03 32 00 80 99 00 01 00 03 34 00 80 "
        "9a 00 01 00 03 36 00 80 1c 00 01 00 03 3a 00 80"
    )


class EVCTest(unittest.TestCase):
    def test_registered(self):
        self.assertTrue({b"evc1", b"evcC"} <= isobmff.get_atom_list())

    def test_baseline_configuration_is_not_fullbox(self):
        parsed, _ = parse(box(b"evcC", minimal()))
        self.assertIsInstance(parsed, EVCConfigurationBox)
        record = parsed.evc_config
        self.assertEqual(record.configuration_version, 1)
        self.assertEqual(record.profile_idc, 0)
        self.assertEqual(record.level_idc, 30)
        self.assertEqual(record.toolset_idc_h, 0)
        self.assertEqual(record.toolset_idc_l, 0)
        self.assertEqual(record.chroma_format_idc, 1)
        self.assertEqual(
            (record.bit_depth_luma, record.bit_depth_chroma), (8, 8)
        )
        self.assertEqual(
            (
                record.pic_width_in_luma_samples,
                record.pic_height_in_luma_samples,
            ),
            (64, 64),
        )
        self.assertEqual(record.length_size_minus_one, 3)
        self.assertEqual(record.array, [])
        self.assertFalse(hasattr(parsed, "flags"))

    def test_main_profile_and_opaque_nalus(self):
        parsed, stream = parse(box(b"evcC", main_profile()))
        record = parsed.evc_config
        self.assertEqual(record.profile_idc, 1)
        self.assertEqual(record.toolset_idc_h, 0x01234567)
        self.assertEqual(record.toolset_idc_l, 0x89ABCDEF)
        self.assertEqual(
            (record.bit_depth_luma, record.bit_depth_chroma), (10, 10)
        )
        self.assertEqual(
            (
                record.pic_width_in_luma_samples,
                record.pic_height_in_luma_samples,
            ),
            (1920, 1080),
        )
        self.assertEqual(
            [a["nal_unit_type"] for a in record.array], [24, 25, 26, 28]
        )
        self.assertEqual(
            [a["array_completeness"] for a in record.array], [1, 1, 1, 0]
        )
        self.assertEqual(record.array[0]["nal_units"], [b"\x32\x00\x80"])
        self.assertEqual(stream.tell(), len(stream.getvalue()))
        self.assertIn("toolset_idc_h:", repr(parsed))

    def test_sample_entry_and_sibling(self):
        payload = box(b"evcC", main_profile()) + box(
            b"pasp", b"\x00\x00\x00\x01" * 2
        )
        parsed, _ = parse(visual_sample_entry(b"evc1", payload))
        self.assertIsInstance(parsed, EVCSampleEntry)
        self.assertEqual((parsed.width, parsed.height), (640, 480))
        self.assertEqual(
            [b.box_type for b in parsed.box_list], [b"evcC", b"pasp"]
        )

    def test_valid_sample_length_sizes(self):
        for length_size in (0, 1, 3):
            record = bytearray(minimal())
            record[16] = length_size
            parsed, _ = parse(box(b"evcC", bytes(record)))
            self.assertEqual(
                parsed.evc_config.length_size_minus_one, length_size
            )

    def test_invalid_reserved_bits_and_length_size(self):
        for byte in (0x80, 2):
            record = bytearray(minimal())
            record[16] = byte
            with self.assertRaises(ValueError):
                parse(box(b"evcC", bytes(record)))
        record = bytearray(main_profile())
        record[18] |= 0x40
        with self.assertRaises(ValueError):
            parse(box(b"evcC", bytes(record)))

    def test_truncation_at_every_offset(self):
        for size in range(len(main_profile())):
            data = box(b"evcC", main_profile()[:size])
            stream = io.BytesIO(data + box(b"free", bytes(4)))
            with self.assertRaises(EOFError):
                read_box(stream, "", 0)
            self.assertEqual(stream.tell(), len(data))
            self.assertEqual(read_box(stream, "", 0).box_type, b"free")

    def test_unknown_version_preserved(self):
        parsed, _ = parse(box(b"evcC", b"\x02future"))
        self.assertEqual(parsed.evc_config.configuration_version, 2)
        self.assertEqual(parsed.evc_config.unsupported_data, b"future")
        self.assertFalse(hasattr(parsed.evc_config, "profile_idc"))

    def test_unknown_type_multiple_nalus_and_tail(self):
        record = minimal()[:-1] + bytes.fromhex(
            "01 bf 00 02 00 01 aa 00 02 bb cc"
        )
        parsed, _ = parse(box(b"evcC", record + b"tail"))
        self.assertEqual(parsed.evc_config.array[0]["nal_unit_type"], 63)
        self.assertEqual(parsed.evc_config.array[0]["nal_unit_lengths"], [1, 2])
        self.assertEqual(
            parsed.evc_config.array[0]["nal_units"], [b"\xaa", b"\xbb\xcc"]
        )
        self.assertEqual(parsed.evc_config.trailing_data, b"tail")

    def test_oversized_nal_length(self):
        record = minimal()[:-1] + bytes.fromhex("01 98 00 01 ff ff 00")
        with self.assertRaises(EOFError):
            parse(box(b"evcC", record))


if __name__ == "__main__":
    unittest.main()
