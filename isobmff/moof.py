# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_box
from .box import read_uint


# ISO/IEC 14496-12:2022, Section 8.8.4
class MovieFragmentBox(Box):
    box_type = "moof"
    box_list = []

    def read(self, file):
        # must have 1 MovieFragmentHeaderBox
        # must have 1+ TrackFragmentBoxes
        while file.tell() < self.get_max_offset():
            box = read_box(file)
            self.box_list.append(box)

    def __repr__(self):
        repl = ()
        for box in self.box_list:
            repl += (repr(box),)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.8.5
class MovieFragmentHeaderBox(FullBox):
    box_type = "mfhd"

    def read(self, file):
        self.sequence_number = read_uint(file, 4)

    def __repr__(self):
        repl = ()
        repl += (f"sequence_number: {self.sequence_number}",)
        return super().repr(repl)
