# -*- coding: utf-8 -*-
from .box import Box
from .codec import DecoderConfigurationRecord
from .stbl import VisualSampleEntry


# ISO/IEC 14496-15:2021, Section 12.3.3.
class EVCSampleEntry(VisualSampleEntry):
    box_type = b"evc1"


class EVCConfigurationBox(Box):
    box_type = b"evcC"

    def read(self, file):
        self.evc_config = EVCDecoderConfigurationRecord(self.max_offset)
        self.evc_config.read(file)

    def contents(self):
        return super().contents() + (
            ("evc_config", self.evc_config.contents()),
        )


class EVCDecoderConfigurationRecord(DecoderConfigurationRecord):
    def read(self, file):
        self._start(file)
        if self._field("configuration_version", 8) != 1:
            self._store("unsupported_data", self._remaining())
            return
        self._field("profile_idc", 8)
        self._field("level_idc", 8)
        self._field("toolset_idc_h", 32)
        self._field("toolset_idc_l", 32)
        self._field("chroma_format_idc", 2)
        self._field("bit_depth_luma_minus8", 3)
        self._field("bit_depth_chroma_minus8", 3)
        self._store("bit_depth_luma", 8 + self.bit_depth_luma_minus8)
        self._store("bit_depth_chroma", 8 + self.bit_depth_chroma_minus8)
        self._field("pic_width_in_luma_samples", 16)
        self._field("pic_height_in_luma_samples", 16)
        if self._field("reserved", 6) != 0:
            raise ValueError("invalid EVC length-size reserved bits")
        if self._field("length_size_minus_one", 2) == 2:
            raise ValueError("unsupported EVC three-byte sample NAL length")
        count = self._field("num_of_arrays", 8)
        arrays = []
        for _ in range(count):
            complete, reserved, kind = (
                self._bits(1),
                self._bits(1),
                self._bits(6),
            )
            if reserved:
                raise ValueError("invalid EVC NAL array reserved bit")
            num_nalus = self._bits(16)
            lengths, nalus = [], []
            for _ in range(num_nalus):
                length = self._bits(16)
                lengths.append(length)
                nalus.append(self._bytes(length))
            arrays.append(
                {
                    "array_completeness": complete,
                    "reserved": reserved,
                    "nal_unit_type": kind,
                    "num_nalus": num_nalus,
                    "nal_unit_lengths": lengths,
                    "nal_units": nalus,
                }
            )
        self._store("array", arrays)
        self._store("trailing_data", self._remaining())
