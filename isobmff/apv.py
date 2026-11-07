# -*- coding: utf-8 -*-
from .box import FullBox
from .codec import DecoderConfigurationRecord
from .stbl import VisualSampleEntry


# OpenAPV readme/apv_isobmff.md, APVConfigurationBox and
# APVDecoderConfigurationRecord. Box version 0 and record version 1
# are independent; this is not the elementary access-unit header.
class APVSampleEntry(VisualSampleEntry):
    box_type = b"apv1"


class APVConfigurationBox(FullBox):
    box_type = b"apvC"

    def read(self, file):
        if file.tell() > self.max_offset:
            file.seek(self.max_offset)
            raise EOFError("truncated apvC FullBox header")
        self.apv_config = None
        if self.version != 0 or self.flags != 0:
            expected = self.max_offset - file.tell()
            self.unsupported_data = self.read_as_bytes(file)
            if len(self.unsupported_data) != expected:
                raise EOFError("truncated unsupported apvC payload")
            return
        self.apv_config = APVDecoderConfigurationRecord(self.max_offset)
        self.apv_config.read(file)

    def contents(self):
        tuples = super().contents()
        if self.apv_config is None:
            return tuples + (("unsupported_data", self.unsupported_data),)
        return tuples + (("apv_config", self.apv_config.contents()),)


class APVDecoderConfigurationRecord(DecoderConfigurationRecord):
    def read(self, file):
        self._start(file)
        if self._field("configuration_version", 8) != 1:
            self._store("unsupported_data", self._remaining())
            return
        count = self._field("entry_count", 8)
        entries = []
        for _ in range(count):
            entry = {
                "pbu_type": self._bits(8),
                "frame_info_count": self._bits(8),
            }
            entry["frame_info"] = [
                self._frame_info() for _ in range(entry["frame_info_count"])
            ]
            entries.append(entry)
        self._store("entries", entries)
        self._store("trailing_data", self._remaining())

    def _frame_info(self):
        header = self._bits(8)
        info = {
            "reserved1": header >> 2,
            "color_description_present_flag": (header >> 1) & 1,
            "capture_time_distance_ignored": header & 1,
        }
        if info["reserved1"]:
            raise ValueError("invalid APV frame-info reserved bits")
        info["profile_idc"] = self._bits(8)
        info["level_idc"] = self._bits(8)
        info["band_idc"] = self._bits(8)
        info["frame_width"] = self._bits(32)
        info["frame_height"] = self._bits(32)
        info["chroma_format_idc"] = self._bits(4)
        info["bit_depth_minus8"] = self._bits(4)
        info["bit_depth"] = 8 + info["bit_depth_minus8"]
        # This byte exists even when the preceding ignored flag is set.
        info["capture_time_distance"] = self._bits(8)
        if info["color_description_present_flag"]:
            info["color_primaries"] = self._bits(8)
            info["transfer_characteristics"] = self._bits(8)
            info["matrix_coefficients"] = self._bits(8)
            info["full_range_flag"] = self._bits(1)
            info["reserved2"] = self._bits(7)
            if info["reserved2"]:
                raise ValueError("invalid APV color-description reserved bits")
        return info
