import io
import tempfile
import unittest

import isobmff
from isobmff.av1 import AV1ConfigurationBox, AV1SampleEntry
from isobmff.box import read_box
from tests.common import bits, box, movie, parse, visual_sample_entry


def configuration(delay=False):
    return (
        bits(
            (1, 1),
            (7, 1),
            (3, 2),
            (5, 13),
            (1, 1),
            (1, 1),
            (1, 1),
            (1, 0),
            (1, 0),
            (1, 0),
            (2, 0),
            (3, 0),
            (1, int(delay)),
            (4, 7 if delay else 0),
        )
        + b"\x0a\x01\x00"
    )


class AV1Test(unittest.TestCase):
    def test_registered(self):
        self.assertTrue({b"av01", b"av1C"} <= isobmff.get_atom_list())

    def test_configuration_and_obus(self):
        parsed, stream = parse(box(b"av1C", configuration(True)))
        self.assertIsInstance(parsed, AV1ConfigurationBox)
        record = parsed.av1_config
        self.assertEqual(record.version, 1)
        self.assertEqual(record.seq_profile, 2)
        self.assertEqual(record.seq_level_idx_0, 13)
        self.assertEqual(record.seq_tier_0, 1)
        self.assertEqual(record.bit_depth, 12)
        self.assertEqual(record.initial_presentation_delay_minus_one, 7)
        self.assertEqual(record.config_obus, b"\x0a\x01\x00")
        self.assertEqual(stream.tell(), len(stream.getvalue()))
        self.assertIn(("config_obus", b"\x0a\x01\x00"), record.contents())
        self.assertIn("seq_level_idx_0: 13", repr(parsed))

    def test_eight_and_ten_bit_without_obus(self):
        for header, depth in (
            (b"\x81\x00\x0c\x00", 8),
            (b"\x81\x00\x4c\x00", 10),
        ):
            parsed, _ = parse(box(b"av1C", header))
            self.assertEqual(parsed.av1_config.bit_depth, depth)
            self.assertEqual(parsed.av1_config.reserved2, 0)
            self.assertEqual(parsed.av1_config.config_obus, b"")
            self.assertFalse(
                hasattr(
                    parsed.av1_config, "initial_presentation_delay_minus_one"
                )
            )

    def test_sample_entry_preserves_sibling(self):
        config = box(b"av1C", configuration())
        sibling = box(b"pasp", b"\x00\x00\x00\x01" * 2)
        parsed, _ = parse(visual_sample_entry(b"av01", config + sibling))
        self.assertIsInstance(parsed, AV1SampleEntry)
        self.assertEqual((parsed.width, parsed.height), (640, 480))
        self.assertEqual(
            [b.box_type for b in parsed.box_list], [b"av1C", b"pasp"]
        )

    def test_mediafile_nested_navigation(self):
        data = movie(b"av01", box(b"av1C", configuration()))
        with tempfile.NamedTemporaryFile() as f:
            f.write(data)
            f.flush()
            parsed = isobmff.MediaFile(f.name, 0)
            parsed.read()
        target = parsed.find_subbox("/moov/trak/mdia/minf/stbl/stsd/av01/av1C")
        self.assertIsInstance(target, AV1ConfigurationBox)

    def test_truncated_configuration_does_not_read_next_box(self):
        for size in range(4):
            data = box(b"av1C", configuration()[:size])
            sibling = box(b"free", bytes(4))
            stream = io.BytesIO(data + sibling)
            with self.assertRaises(EOFError):
                read_box(stream, "", 0, max_offset=len(data + sibling))
            self.assertEqual(stream.tell(), len(data))
            self.assertEqual(read_box(stream, "", 0).box_type, b"free")

    def test_invalid_marker_and_version(self):
        for header in (b"\x01\x00\x00\x00", b"\x82\x00\x00\x00"):
            with self.assertRaises(ValueError):
                parse(box(b"av1C", header))

    def test_physical_truncation(self):
        data = box(b"av1C", configuration())[:-1]
        with self.assertRaises(EOFError):
            # No parent clamp: The declared box extends past physical EOF.
            read_box(io.BytesIO(data), "", 0)


if __name__ == "__main__":
    unittest.main()
