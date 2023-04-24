# -*- coding: utf-8 -*-
from .box import Box
from .box import read_uint
from .box import read_bytes
from .stbl import VisualSampleEntry


# ISO/IEC 14496-15:2022, Section 5.4.2.1.2
class AVCSampleEntry(VisualSampleEntry):
    box_type = b"avc1"

    def read(self, file):
        super().read(file)
        # already included in the VisualSampleEntry box_list
        # self.config = self.read_box(file)

    def contents(self):
        tuples = super().contents()
        # tuples += (("config", self.config.contents()),)
        return tuples


# ISO/IEC 14496-15:2022, Section 5.4.2.1.2
class AVC3SampleEntry(AVCSampleEntry):
    box_type = b"avc3"


# ISO/IEC 14496-15:2022, Section 5.4.2.1.2
class AVC2SampleEntry(VisualSampleEntry):
    box_type = b"avc2"

    def read(self, file):
        super().read(file)
        # already included in the VisualSampleEntry box_list
        # self.avcconfig = self.read_box(file)

    def contents(self):
        tuples = super().contents()
        # tuples += (("avcconfig", self.avcconfig.contents()),)
        return tuples


# ISO/IEC 14496-15:2022, Section 5.4.2.1.2
class AVC4SampleEntry(AVC2SampleEntry):
    box_type = b"avc4"


# ISO/IEC 14496-15:2022, Section 5.4.2.1.2
class AVCConfigurationBox(Box):
    box_type = b"avcC"

    def read(self, file):
        self.avc_config = AVCDecoderConfigurationRecord(max_offset=self.max_offset)
        self.avc_config.read(file)

    def contents(self):
        tuples = super().contents()
        tuples += (("avc_config", self.avc_config.contents()),)
        return tuples


# ISO/IEC 14496-15:2022, Section 5.3.2.1.2
class AVCDecoderConfigurationRecord:
    def __init__(self, max_offset):
        self.max_offset = max_offset

    def read(self, file):
        if file.tell() >= self.max_offset:
            # out of data in the box: let's punt here
            self.reserved1 = None
            return
        self.configurationVersion = read_uint(file, 1)
        self.AVCProfileIndication = read_uint(file, 1)
        self.profile_compatibility = read_uint(file, 1)
        self.AVCLevelIndication = read_uint(file, 1)
        byte4 = read_uint(file, 1)
        self.reserved1 = (byte4 >> 2) & 0x3F
        self.lengthSizeMinusOne = byte4 & 0x03
        byte5 = read_uint(file, 1)
        self.reserved2 = (byte5 >> 5) & 0x07
        numOfSequenceParameterSets = byte5 & 0x1F
        self.sps = []
        for _ in range(numOfSequenceParameterSets):
            sequenceParameterSetLength = read_uint(file, 2)
            self.sps.append(read_bytes(file, sequenceParameterSetLength))
        numOfPictureParameterSets = read_uint(file, 1)
        self.pps = []
        for _ in range(numOfPictureParameterSets):
            pictureParameterSetLength = read_uint(file, 2)
            self.pps.append(read_bytes(file, pictureParameterSetLength))
        # ensure there are enough bytes for the remaining fields
        self.sps_ext = []
        if file.tell() >= self.max_offset:
            # out of data in the box: let's punt here
            self.reserved3 = None
            return
        if self.AVCProfileIndication not in [66, 77, 88]:
            byte = read_uint(file, 1)
            self.reserved3 = (byte >> 2) & 0x3F
            self.chroma_format = byte & 0x03
            byte = read_uint(file, 1)
            self.reserved4 = (byte >> 3) & 0x1F
            self.bit_depth_luma_minus8 = byte & 0x07
            byte = read_uint(file, 1)
            self.reserved5 = (byte >> 3) & 0x1F
            self.bit_depth_chroma_minus8 = byte & 0x07
            numOfSequenceParameterSetExt = read_uint(file, 1)
            for _ in range(numOfSequenceParameterSetExt):
                sequenceParameterSetExtLength = read_uint(file, 2)
                self.sps_ext.append(read_bytes(file, sequenceParameterSetExtLength))

    def contents(self):
        # a non-Box class has no parent
        tuples = ()
        if self.reserved1 is None:
            return tuples
        tuples += (("configurationVersion", self.configurationVersion),)
        tuples += (("AVCProfileIndication", self.AVCProfileIndication),)
        tuples += (("profile_compatibility", self.profile_compatibility),)
        tuples += (("AVCLevelIndication", self.AVCLevelIndication),)
        tuples += (("reserved1", bin(self.reserved1)),)
        tuples += (("lengthSizeMinusOne", self.lengthSizeMinusOne),)
        tuples += (("reserved2", bin(self.reserved2)),)
        for idx, val in enumerate(self.sps):
            tuples += ((f"sps[{idx}]", val),)
        for idx, val in enumerate(self.pps):
            tuples += ((f"pps[{idx}]", val),)
        if self.reserved3 is not None and self.AVCProfileIndication not in [66, 77, 88]:
            tuples += (("reserved3", bin(self.reserved3)),)
            tuples += (("chroma_format", self.chroma_format),)
            tuples += (("reserved4", bin(self.reserved4)),)
            tuples += (("bit_depth_luma_minus8", self.bit_depth_luma_minus8),)
            tuples += (("reserved5", bin(self.reserved5)),)
            tuples += (("bit_depth_chroma_minus8", self.bit_depth_chroma_minus8),)
            for idx, val in enumerate(self.sps_ext):
                tuples += ((f"sps_ext[{idx}]", val),)
        return tuples
