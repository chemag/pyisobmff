# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import read_box
from .box import read_uint


# ISO/IEC 14496-12:2022, Section 8.8.1
class MovieExtendsBox(Box):
    box_type = "mvex"
    box_list = []

    def read(self, file):
        # optional MovieExtendsHeaderBox
        # other boxes
        while file.tell() < self.get_max_offset():
            box = read_box(file, self.debug)
            self.box_list.append(box)

    def __repr__(self):
        repl = ()
        for box in self.box_list:
            repl += (repr(box),)
        return super().repr(repl)
