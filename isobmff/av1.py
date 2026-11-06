# -*- coding: utf-8 -*-
from .box import Box
from .codec import DecoderConfigurationRecord
from .stbl import VisualSampleEntry


# AV1 Codec ISO Media File Format Binding, Sections 2.2 and 2.3.
# https://aomediacodec.github.io/av1-isobmff/
class AV1SampleEntry(VisualSampleEntry):
    box_type = b"av01"


class AV1ConfigurationBox(Box):
    box_type = b"av1C"

    def read(self, file):
        self.av1_config = AV1CodecConfigurationRecord(self.max_offset)
        self.av1_config.read(file)

    def contents(self):
        return super().contents() + (
            ("av1_config", self.av1_config.contents()),
        )


class AV1CodecConfigurationRecord(DecoderConfigurationRecord):
    def read(self, file):
        self._start(file)
        if self._field("marker", 1) != 1:
            raise ValueError("invalid AV1 configuration marker")
        if self._field("version", 7) != 1:
            raise ValueError("unsupported AV1 configuration version")
        self._field("seq_profile", 3)
        self._field("seq_level_idx_0", 5)
        self._field("seq_tier_0", 1)
        self._field("high_bitdepth", 1)
        self._field("twelve_bit", 1)
        self._field("monochrome", 1)
        self._field("chroma_subsampling_x", 1)
        self._field("chroma_subsampling_y", 1)
        self._field("chroma_sample_position", 2)
        self._field("reserved1", 3)
        self._field("initial_presentation_delay_present", 1)
        if self.initial_presentation_delay_present:
            self._field("initial_presentation_delay_minus_one", 4)
        else:
            self._field("reserved2", 4)
        depth = 12 if self.twelve_bit else 10
        self._store("bit_depth", depth if self.high_bitdepth else 8)
        # OBUs belong to the codec syntax, not the ISOBMFF box parser.
        self._store("config_obus", self._remaining())
