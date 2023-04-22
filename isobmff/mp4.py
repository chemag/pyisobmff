# -*- coding: utf-8 -*-
from .box import FullBox
from .box import Quantity
from .box import read_uint
from .stbl import VisualSampleEntry
from .stbl import AudioSampleEntry
from .stbl import SampleEntry


# ISO/IEC 14496-14:2020, Section 6.7.2
class EDSBox(FullBox):
    box_type = b"esds"


# ISO/IEC 14496-14:2020, Section 6.7.2
class MP4VisualSampleEntry(VisualSampleEntry):
    box_type = b"mp4v"

    def read(self, file):
        super().read(file)
        self.ES = self.read_box(file)

    def contents(self):
        tuples = super().contents()
        if self.ES is not None:
            tuples += (("ES", self.ES.contents()),)
        return tuples


# ISO/IEC 14496-14:2020, Section 6.7.2
class MP4AudioSampleEntry(AudioSampleEntry):
    box_type = b"mp4a"

    def read(self, file):
        super().read(file)
        self.ES = self.read_box(file)

    def contents(self):
        tuples = super().contents()
        if self.ES is not None:
            tuples += (("ES", self.ES.contents()),)
        return tuples


# ISO/IEC 14496-14:2020, Section 6.7.2
class MpegSampleEntry(SampleEntry):
    box_type = b"mp4s"

    def read(self, file):
        super().read(file)
        self.ES = self.read_box(file)

    def contents(self):
        tuples = super().contents()
        if self.ES is not None:
            tuples += (("ES", self.ES.contents()),)
        return tuples
