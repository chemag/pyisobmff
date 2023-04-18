# -*- coding: utf-8 -*-
from .box import Box
from .box import read_uint
from .stbl import AudioSampleEntry
from .stbl import BitRateBox


# ISO/IEC 23008-3:2015-Amd-2:2016, Section 20.4
class MHADecoderConfigurationRecord(object):
    def __init__(self, max_offset):
        self.max_offset = max_offset

    def read(self, file):
        self.configurationVersion = read_uint(file, 1)
        self.mpegh3daProfileLevelIndication = read_uint(file, 1)
        self.referenceChannelLayout = read_uint(file, 1)
        self.mpegh3daConfigLength = read_uint(file, 2)
        self.mpegh3daConfig = read_uint(file, self.mpegh3daConfigLength)

    def contents(self):
        tuples = ()
        tuples += (("configurationVersion", self.configurationVersion),)
        tuples += (
            ("mpegh3daProfileLevelIndication", self.mpegh3daProfileLevelIndication),
        )
        tuples += (("referenceChannelLayout", self.referenceChannelLayout),)
        tuples += (("mpegh3daConfigLength", self.mpegh3daConfigLength),)
        tuples += (("mpegh3daConfig", self.mpegh3daConfig),)
        return tuples


# ISO/IEC 23008-3:2015-Amd-2:2016, Section 20.5.2
class MHAConfigurationBox(Box):
    box_type = b"mhaC"

    def read(self, file):
        self.MHAConfig = MHADecoderConfigurationRecord(max_offset=self.get_max_offset())
        self.MHAConfig.read(file)

    def contents(self):
        tuples = super().contents()
        tuples += (("MHAConfig", self.MHAConfig.contents()),)
        return tuples


## ISO/IEC 23008-3:2015-Amd-2:2016, Section 20.5.2
# class MPEG4BitRateBox(BitRateBox):
#    pass


# ISO/IEC 23008-3:2015-Amd-2:2016, Section 20.5.2
class MPEG4ExtensionDescriptorsBox(Box):
    box_type = b"m4ds"
    # Descriptor Descr[0 .. 255];


# ISO/IEC 23008-3:2015-Amd-2:2016, Section 20.5.2
class MHASampleEntry(AudioSampleEntry):
    box_type = b"mha1"
    box_list = []

    def read(self, file):
        super().read(file)
        self.box_list = self.read_box_list(file)

    def contents(self):
        tuples = super().contents()
        for idx, box in enumerate(self.box_list):
            tuples += ((f"box[{idx}]", box.contents()),)
        return tuples


# ISO/IEC 23008-3:2015-Amd-2:2016, Section 20.5.2
class MHA2SampleEntry(MHASampleEntry):
    box_type = b"mha2"


# ISO/IEC 23008-3:2015-Amd-2:2016, Section 20.6.2
class MHMSampleEntry(MHASampleEntry):
    box_type = b"mhm1"


# ISO/IEC 23008-3:2015-Amd-2:2016, Section 20.6.2
class MHM2SampleEntry(MHASampleEntry):
    box_type = b"mhm2"
