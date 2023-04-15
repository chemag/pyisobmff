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
