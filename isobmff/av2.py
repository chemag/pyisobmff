# -*- coding: utf-8 -*-
from .box import Box
from .codec import DecoderConfigurationRecord
from .stbl import VisualSampleEntry


# AV2 ISOBMFF carriage in FFmpeg av2.c, introduced by bd2ed1adf4a2
# (2026-11-04). av02 is a compatible brand, not a sample entry.
class AV2SampleEntry(VisualSampleEntry):
    box_type = b"av2E"


class AV2InBandSampleEntry(VisualSampleEntry):
    box_type = b"av2e"


class AV2ConfigurationBox(Box):
    box_type = b"av2C"

    def read(self, file):
        self.av2_config = AV2CodecConfigurationRecord(self.max_offset)
        self.av2_config.read(file)

    def contents(self):
        return super().contents() + (
            ("av2_config", self.av2_config.contents()),
        )


class AV2CodecConfigurationRecord(DecoderConfigurationRecord):
    def read(self, file):
        self._start(file)
        if self._field("reserved", 8) != 0:
            raise ValueError("unsupported AV2 configuration reserved byte")
        count = self._field("count_minus_one", 8) + 1
        obus, lengths, prefixes = [], [], []
        for _ in range(count):
            # The ISOBMFF length includes the entire opaque OBU, not its
            # own ULEB128 prefix. No OBU header or codec payload is parsed.
            length, prefix = self._read_length()
            if length == 0:
                raise ValueError("zero-length AV2 configuration OBU")
            obus.append(self._bytes(length))
            lengths.append(length)
            prefixes.append(prefix)
        if self._bit_offset != len(self._data) * 8:
            raise ValueError("trailing bytes in AV2 configuration record")
        self._store("obu_count", count)
        self._store("obu_lengths", lengths)
        self._store("obu_length_prefixes", prefixes)
        self._store("config_obus", obus)

    def _read_length(self):
        value, prefix = 0, bytearray()
        for shift in range(0, 56, 7):
            byte = self._bits(8)
            prefix.append(byte)
            value |= (byte & 0x7F) << shift
            if not byte & 0x80:
                return value, bytes(prefix)
        raise ValueError("unterminated AV2 configuration OBU length")
