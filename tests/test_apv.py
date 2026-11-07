import io
import unittest

import isobmff
from isobmff.apv import APVConfigurationBox, APVSampleEntry
from isobmff.box import read_box
from tests.common import box, parse, visual_sample_entry


def apvc(record, version=0, flags=0):
    return box(b"apvC", bytes([version]) + flags.to_bytes(3, "big") + record)


def frame_without_color():
    return bytes.fromhex("01 2c d2 03 00 00 07 80 00 00 04 38 24 00")


def frame_with_color():
    return bytes.fromhex(
        "03 2c d2 03 00 00 0f 00 00 00 08 70 24 02 09 10 09 80"
    )


def configuration(multiple=False):
    frames = frame_without_color()
    if multiple:
        frames += frame_with_color()
    return bytes([1, 1, 1, 2 if multiple else 1]) + frames


class APVTest(unittest.TestCase):
    def test_registered(self):
        self.assertTrue({b"apv1", b"apvC"} <= isobmff.get_atom_list())
        self.assertNotIn(b"aPv1", isobmff.get_atom_list())

    def test_fullbox_and_record_versions_are_distinct(self):
        parsed, stream = parse(apvc(configuration()))
        self.assertIsInstance(parsed, APVConfigurationBox)
        self.assertEqual((parsed.version, parsed.flags), (0, 0))
        record = parsed.apv_config
        self.assertEqual(record.configuration_version, 1)
        self.assertEqual(record.entry_count, 1)
        self.assertEqual(record.entries[0]["pbu_type"], 1)
        frame = record.entries[0]["frame_info"][0]
        self.assertEqual(frame["profile_idc"], 44)
        self.assertEqual(frame["level_idc"], 210)
        self.assertEqual(frame["band_idc"], 3)
        self.assertEqual(
            (frame["frame_width"], frame["frame_height"]), (1920, 1080)
        )
        self.assertEqual(frame["chroma_format_idc"], 2)
        self.assertEqual(frame["bit_depth"], 12)
        self.assertEqual(frame["capture_time_distance_ignored"], 1)
        self.assertEqual(frame["capture_time_distance"], 0)
        self.assertNotIn("color_primaries", frame)
        self.assertEqual(stream.tell(), len(stream.getvalue()))
        self.assertIn("frame_width", repr(parsed))

    def test_nested_frame_variations_and_color(self):
        parsed, _ = parse(apvc(configuration(True)))
        entry = parsed.apv_config.entries[0]
        self.assertEqual(entry["frame_info_count"], 2)
        frame = entry["frame_info"][1]
        self.assertEqual(
            (frame["frame_width"], frame["frame_height"]), (3840, 2160)
        )
        self.assertEqual(frame["capture_time_distance"], 2)
        self.assertEqual(frame["color_primaries"], 9)
        self.assertEqual(frame["transfer_characteristics"], 16)
        self.assertEqual(frame["matrix_coefficients"], 9)
        self.assertEqual(frame["full_range_flag"], 1)

    def test_multiple_entries_and_zero_counts(self):
        record = (
            b"\x01\x02\x01\x01"
            + frame_without_color()
            + b"\x05\x01"
            + frame_with_color()
        )
        parsed, _ = parse(apvc(record))
        self.assertEqual(
            [e["pbu_type"] for e in parsed.apv_config.entries], [1, 5]
        )
        parsed, _ = parse(apvc(b"\x01\x00"))
        self.assertEqual(parsed.apv_config.entries, [])
        parsed, _ = parse(apvc(b"\x01\x01\x01\x00"))
        self.assertEqual(parsed.apv_config.entries[0]["frame_info"], [])

    def test_capture_distance_not_omitted_when_ignored(self):
        frame = bytearray(frame_without_color())
        frame[-1] = 7
        parsed, _ = parse(apvc(b"\x01\x01\x01\x01" + frame))
        self.assertEqual(
            parsed.apv_config.entries[0]["frame_info"][0][
                "capture_time_distance"
            ],
            7,
        )

    def test_sample_entry_and_sibling(self):
        config = apvc(configuration())
        sibling = box(b"pasp", b"\x00\x00\x00\x01" * 2)
        parsed, _ = parse(visual_sample_entry(b"apv1", config + sibling))
        self.assertIsInstance(parsed, APVSampleEntry)
        self.assertEqual((parsed.width, parsed.height), (640, 480))
        self.assertEqual(
            [b.box_type for b in parsed.box_list], [b"apvC", b"pasp"]
        )

    def test_truncation_at_every_record_offset(self):
        for size in range(len(configuration(True))):
            data = apvc(configuration(True)[:size])
            stream = io.BytesIO(data + box(b"free", bytes(4)))
            with self.assertRaises(EOFError):
                read_box(stream, "", 0)
            self.assertEqual(stream.tell(), len(data))
            self.assertEqual(read_box(stream, "", 0).box_type, b"free")

    def test_truncated_fullbox_header_preserves_sibling(self):
        for size in range(4):
            data = box(b"apvC", bytes(size))
            stream = io.BytesIO(data + box(b"free", bytes(4)))
            with self.assertRaises(EOFError):
                read_box(stream, "", 0)
            self.assertEqual(stream.tell(), len(data))
            self.assertEqual(read_box(stream, "", 0).box_type, b"free")

    def test_unknown_versions_and_flags_preserved(self):
        for version, flags in ((1, 0), (0, 1)):
            parsed, _ = parse(apvc(b"future", version, flags))
            self.assertIsNone(parsed.apv_config)
            self.assertEqual(parsed.unsupported_data, b"future")
        parsed, _ = parse(apvc(b"\x02future"))
        self.assertEqual(parsed.apv_config.configuration_version, 2)
        self.assertEqual(parsed.apv_config.unsupported_data, b"future")
        self.assertFalse(hasattr(parsed.apv_config, "entries"))

    def test_truncated_unsupported_payload(self):
        for version, flags in ((1, 0), (0, 1)):
            data = apvc(b"future", version, flags)[:-2]
            with self.assertRaises(EOFError):
                read_box(io.BytesIO(data), "", 0)

    def test_both_reserved_fields(self):
        record = bytearray(configuration())
        record[4] |= 0x80
        with self.assertRaises(ValueError):
            parse(apvc(bytes(record)))
        record = bytearray(configuration(True))
        record[-1] |= 1
        with self.assertRaises(ValueError):
            parse(apvc(bytes(record)))

    def test_trailing_bytes_preserved(self):
        parsed, _ = parse(apvc(configuration() + b"tail"))
        self.assertEqual(parsed.apv_config.trailing_data, b"tail")

    def test_dimensions_are_unsigned_32bit_not_minus_one(self):
        frame = bytearray(frame_without_color())
        frame[4:8] = (0x01020304).to_bytes(4, "big")
        frame[8:12] = (0x80000001).to_bytes(4, "big")
        parsed, _ = parse(apvc(b"\x01\x01\x01\x01" + frame))
        info = parsed.apv_config.entries[0]["frame_info"][0]
        self.assertEqual(info["frame_width"], 0x01020304)
        self.assertEqual(info["frame_height"], 0x80000001)


if __name__ == "__main__":
    unittest.main()
