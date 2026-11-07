# -*- coding: utf-8 -*-
from .box import FullBox
from .codec import DecoderConfigurationRecord
from .stbl import VisualSampleEntry


# ISO/IEC 14496-15, VVCDecoderConfigurationRecord.
# Sublayer flags are MSB-first, followed by reserved alignment bits; see
# GPAC descriptors.c and FFmpeg cbs_h266.c, not the legacy muxer packing.
class VVCSampleEntry(VisualSampleEntry):
    box_type = b"vvc1"


class VVCInBandSampleEntry(VisualSampleEntry):
    box_type = b"vvi1"


class VVCConfigurationBox(FullBox):
    box_type = b"vvcC"

    def read(self, file):
        if file.tell() > self.max_offset:
            file.seek(self.max_offset)
            raise EOFError("truncated vvcC FullBox header")
        self.vvc_config = None
        if self.version != 0 or self.flags != 0:
            expected = self.max_offset - file.tell()
            self.unsupported_data = self.read_as_bytes(file)
            if len(self.unsupported_data) != expected:
                raise EOFError("truncated unsupported vvcC payload")
            return
        self.vvc_config = VVCDecoderConfigurationRecord(self.max_offset)
        self.vvc_config.read(file)

    def contents(self):
        tuples = super().contents()
        if self.vvc_config is None:
            return tuples + (("unsupported_data", self.unsupported_data),)
        return tuples + (("vvc_config", self.vvc_config.contents()),)


class VVCDecoderConfigurationRecord(DecoderConfigurationRecord):
    def read(self, file):
        self._start(file)
        if self._field("reserved1", 5) != 31:
            raise ValueError("invalid VVC reserved bits")
        self._field("length_size_minus_one", 2)
        self._field("ptl_present_flag", 1)
        if self.ptl_present_flag:
            self._read_ptl()
        count = self._field("num_of_arrays", 8)
        arrays = []
        for _ in range(count):
            complete, reserved, kind = (
                self._bits(1),
                self._bits(2),
                self._bits(5),
            )
            if reserved:
                raise ValueError("invalid VVC NAL array reserved bits")
            # OPI/DCI arrays contain exactly one NAL and omit num_nalus.
            num_nalus = 1 if kind in (12, 13) else self._bits(16)
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

    def _read_ptl(self):
        self._field("ols_idx", 9)
        if self._field("num_sublayers", 3) == 0:
            raise ValueError("invalid VVC sublayer count")
        self._field("constant_frame_rate", 2)
        self._field("chroma_format_idc", 2)
        self._field("bit_depth_minus8", 3)
        self._store("bit_depth", 8 + self.bit_depth_minus8)
        if self._field("reserved2", 5) != 31:
            raise ValueError("invalid VVC bit-depth reserved bits")
        if self._field("reserved3", 2) != 0:
            raise ValueError("invalid VVC constraint-count reserved bits")
        count = self._field("num_bytes_constraint_info", 6)
        if count == 0:
            raise ValueError("VVC constraint-info count must be nonzero")
        self._field("general_profile_idc", 7)
        self._field("general_tier_flag", 1)
        self._field("general_level_idc", 8)
        raw = self._bytes(count)
        self._store("constraint_info_bytes", raw)
        self._store("ptl_frame_only_constraint_flag", raw[0] >> 7)
        self._store("ptl_multilayer_enabled_flag", (raw[0] >> 6) & 1)
        width = 8 * count - 2
        self._store("general_constraint_info_bit_count", width)
        self._store(
            "general_constraint_info",
            int.from_bytes(raw, "big") & ((1 << width) - 1),
        )
        flags = {}
        if self.num_sublayers > 1:
            for i in range(self.num_sublayers - 2, -1, -1):
                flags[i] = self._bits(1)
            if self._field("reserved4", 9 - self.num_sublayers) != 0:
                raise ValueError("invalid VVC sublayer alignment bits")
        self._store("ptl_sublayer_level_present_flag", flags)
        levels = {i: self._bits(8) for i, present in flags.items() if present}
        self._store("sublayer_level_idc", levels)
        count = self._field("ptl_num_sub_profiles", 8)
        self._store(
            "general_sub_profile_idc", [self._bits(32) for _ in range(count)]
        )
        self._field("max_picture_width", 16)
        self._field("max_picture_height", 16)
        self._field("avg_frame_rate", 16)
