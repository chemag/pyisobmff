import io
import unittest

import isobmff
from isobmff.av2 import (
    AV2ConfigurationBox,
    AV2SampleEntry,
    AV2InBandSampleEntry,
)
from isobmff.box import read_box
from tests.common import box, parse, visual_sample_entry


def configuration():
    return bytes.fromhex("00 01 03 04 aa bb 03 c0 05 77")


class AV2Test(unittest.TestCase):
    def test_registered_sample_entries_not_brand(self):
        self.assertTrue({b"av2E", b"av2e", b"av2C"} <= isobmff.get_atom_list())
        self.assertNotIn(b"av02", isobmff.get_atom_list())

    def test_configuration_keeps_obus_opaque(self):
        parsed, stream = parse(box(b"av2C", configuration()))
        self.assertIsInstance(parsed, AV2ConfigurationBox)
        record = parsed.av2_config
        self.assertEqual(record.reserved, 0)
        self.assertEqual(record.obu_count, 2)
        self.assertEqual(record.obu_lengths, [3, 3])
        self.assertEqual(record.obu_length_prefixes, [b"\x03", b"\x03"])
        self.assertEqual(record.config_obus, [b"\x04\xaa\xbb", b"\xc0\x05\x77"])
        self.assertEqual(stream.tell(), len(stream.getvalue()))
        self.assertIn("obu_count: 2", repr(parsed))
        self.assertFalse(hasattr(record, "seq_profile"))

    def test_multibyte_length_prefix(self):
        payload = b"\x00\x00\x82\x01" + bytes(range(130))
        parsed, _ = parse(box(b"av2C", payload))
        self.assertEqual(parsed.av2_config.obu_lengths, [130])
        self.assertEqual(parsed.av2_config.obu_length_prefixes, [b"\x82\x01"])
        self.assertEqual(parsed.av2_config.config_obus, [bytes(range(130))])

    def test_maximum_count_and_eight_byte_length(self):
        parsed, _ = parse(box(b"av2C", b"\x00\xff" + b"\x01\xaa" * 256))
        self.assertEqual(parsed.av2_config.obu_count, 256)
        self.assertEqual(parsed.av2_config.config_obus, [b"\xaa"] * 256)
        prefix = b"\x81" + b"\x80" * 6 + b"\x00"
        parsed, _ = parse(box(b"av2C", b"\x00\x00" + prefix + b"\xaa"))
        self.assertEqual(parsed.av2_config.obu_length_prefixes, [prefix])
        self.assertEqual(parsed.av2_config.config_obus, [b"\xaa"])

    def test_sample_entries_and_child_boundaries(self):
        config = box(b"av2C", configuration())
        sibling = box(b"pasp", b"\x00\x00\x00\x01" * 2)
        for fourcc, kind in (
            (b"av2E", AV2SampleEntry),
            (b"av2e", AV2InBandSampleEntry),
        ):
            parsed, _ = parse(visual_sample_entry(fourcc, config + sibling))
            self.assertIsInstance(parsed, kind)
            self.assertEqual((parsed.width, parsed.height), (640, 480))
            self.assertEqual(
                [b.box_type for b in parsed.box_list], [b"av2C", b"pasp"]
            )

    def test_truncation_at_every_offset(self):
        for size in range(len(configuration())):
            data = box(b"av2C", configuration()[:size])
            stream = io.BytesIO(data + box(b"free", bytes(4)))
            with self.assertRaises(EOFError):
                read_box(stream, "", 0)
            self.assertEqual(stream.tell(), len(data))
            self.assertEqual(read_box(stream, "", 0).box_type, b"free")

    def test_invalid_count_and_trailing_data(self):
        for payload in (configuration() + b"\x00", b"\x00\x00\x00"):
            with self.assertRaises(ValueError):
                parse(box(b"av2C", payload))
        with self.assertRaises(EOFError):
            parse(box(b"av2C", b"\x00\x01\x01\xaa"))

    def test_reserved_byte_and_unterminated_length(self):
        for payload in (b"\x01\x00\x01\x00", b"\x00\x00" + b"\x80" * 8):
            with self.assertRaises(ValueError):
                parse(box(b"av2C", payload))

    def test_noncodec_bytes_are_preserved_not_interpreted(self):
        # Deliberately not a valid elementary-codec header. This parser
        # understands ISOBMFF framing, not AV2 OBU syntax or conformance.
        parsed, _ = parse(box(b"av2C", b"\x00\x00\x01\xff"))
        self.assertEqual(parsed.av2_config.config_obus, [b"\xff"])


if __name__ == "__main__":
    unittest.main()
