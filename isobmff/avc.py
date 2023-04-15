# -*- coding: utf-8 -*-
from .box import Box
from .box import Quantity
from .box import read_box
from .box import read_uint
from .box import read_bytes
from .stbl import VisualSampleEntry


# ISO/IEC 14496-15:2022, Section 5.4.2.1.2
class AVCSampleEntry(VisualSampleEntry):
    box_type = "avc1"

    def read(self, file):
        super().read(file)
        self.config = read_box(file, self.debug)

    def __repr__(self):
        repl = ()
        repl += (f"config: {self.config}",)
        return super().repr(repl)


# ISO/IEC 14496-15:2022, Section 5.4.2.1.2
class AVC3SampleEntry(AVCSampleEntry):
    box_type = "avc3"


# ISO/IEC 14496-15:2022, Section 5.4.2.1.2
class AVC2SampleEntry(VisualSampleEntry):
    box_type = "avc2"

    def read(self, file):
        super().read(file)
        self.avcconfig = read_box(file, self.debug)

    def __repr__(self):
        repl = ()
        repl += (f"avcconfig: {self.avcconfig}",)
        return super().repr(repl)


# ISO/IEC 14496-15:2022, Section 5.4.2.1.2
class AVC3SampleEntry(AVCSampleEntry):
    box_type = "avc3"


# ISO/IEC 14496-15:2022, Section 5.4.2.1.2
class AVCConfigurationBox(Box):
    box_type = "avcC"

    def read(self, file):
        self.avc_config = AVCDecoderConfigurationRecord()
        self.avc_config.read(file)

    def __repr__(self):
        repl = ()
        repl += (f"avc_config: {self.avc_config}",)
        return super().repr(repl)


# ISO/IEC 14496-15:2022, Section 5.3.2.1.2
class AVCDecoderConfigurationRecord(object):
    sps = []
    pps = []
    sps_ext = []

    def read(self, file):
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
        for _ in range(numOfSequenceParameterSets):
            sequenceParameterSetLength = read_uint(file, 2)
            self.sps.append(read_bytes(file, sequenceParameterSetLength))
        numOfPictureParameterSets = read_uint(file, 1)
        for _ in range(numOfPictureParameterSets):
            pictureParameterSetLength = read_uint(file, 2)
            self.pps.append(read_bytes(file, pictureParameterSetLength))
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

    def __repr__(self):
        repl = ()
        repl += (f"configurationVersion: {self.configurationVersion}",)
        repl += (f"AVCProfileIndication: {self.AVCProfileIndication}",)
        repl += (f"profile_compatibility: {self.profile_compatibility}",)
        repl += (f"AVCLevelIndication: {self.AVCLevelIndication}",)
        repl += (f"reserved1: {bin(self.reserved1)}",)
        repl += (f"lengthSizeMinusOne: {self.lengthSizeMinusOne}",)
        repl += (f"reserved2: {bin(self.reserved2)}",)
        for idx, val in enumerate(self.sps):
            repl += (f'sps[{idx}]: "{val}"',)
        for idx, val in enumerate(self.pps):
            repl += (f'pps[{idx}]: "{val}"',)
        if self.AVCProfileIndication not in [66, 77, 88]:
            repl += (f"reserved3: {bin(self.reserved3)}",)
            repl += (f"chroma_format: {self.chroma_format}",)
            repl += (f"reserved4: {bin(self.reserved4)}",)
            repl += (f"bit_depth_luma_minus8: {self.bit_depth_luma_minus8}",)
            repl += (f"reserved5: {bin(self.reserved5)}",)
            repl += (f"bit_depth_chroma_minus8: {self.bit_depth_chroma_minus8}",)
            for idx, val in enumerate(self.sps_ext):
                repl += (f'sps_ext[{idx}]: "{val}"',)
        return "\n".join(repl)
