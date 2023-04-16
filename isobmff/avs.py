# -*- coding: utf-8 -*-
from .box import Box
from .box import read_box
from .box import read_uint
from .box import read_bytes
from .stbl import VisualSampleEntry


# IEEE 1857.3-2013, Section 4.2.3.3.1
class AvsSampleEntry(VisualSampleEntry):
    box_type = b"avs2"

    def read(self, file):
        super().read(file)
        self.config = read_box(file, self.debug)

    def __repr__(self):
        repl = ()
        repl += (f"config: {self.config}",)
        return super().repr(repl)
