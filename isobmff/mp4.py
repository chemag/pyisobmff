# -*- coding: utf-8 -*-
from .box import FullBox
from .box import Quantity
from .box import read_box
from .box import read_uint
from .stbl import VisualSampleEntry


# ISO/IEC 14496-14:2020, Section 6.7.2
class EDSBox(FullBox):
    box_type = "esds"


# ISO/IEC 14496-14:2020, Section 6.7.2
class MP4VisualSampleEntry(VisualSampleEntry):
    box_type = "mp4v"

    def read(self, file):
        super().read(file)
        self.ES = read_box(file, self.debug)

    def __repr__(self):
        repl = ()
        repl += (f"ES: {self.ES}",)
        return super().repr(repl)
