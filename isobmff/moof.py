# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_uint


# ISO/IEC 14496-12:2022, Section 8.8.4
class MovieFragmentBox(Box):
    box_type = b"moof"
    box_list = []

    def read(self, file):
        # must have 1 MovieFragmentHeaderBox
        # must have 1+ TrackFragmentBoxes
        self.box_list = self.read_box_list(file)

    def __repr__(self):
        repl = ()
        if self.debug > 2:
            for box in self.box_list:
                repl += (repr(box),)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.8.5
class MovieFragmentHeaderBox(FullBox):
    box_type = b"mfhd"

    def read(self, file):
        self.sequence_number = read_uint(file, 4)

    def __repr__(self):
        repl = ()
        repl += (f"sequence_number: {self.sequence_number}",)
        return super().repr(repl)
