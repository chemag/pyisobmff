# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_uint
from .box import read_box


# ISO/IEC 14496-12:2022, Section 8.4.1.1
class MediaBox(Box):
    box_type = "mdia"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE
    box_list = []

    def read(self, file):
        while file.tell() < self.get_max_offset():
            box = read_box(file)
            self.box_list.append(box)

    def __repr__(self):
        repl = ()
        for box in self.box_list:
            repl += (repr(box),)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.4.2.1
class MediaHeaderBox(FullBox):
    box_type = "mdhd"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE
    # ISO-639-2/T language code
    language = []

    def read(self, file):
        read_size = 8 if self.version == 1 else 4
        self.creation_time = read_uint(file, read_size)
        self.modification_time = read_uint(file, read_size)
        self.timescale = read_uint(file, 4)
        self.duration = read_uint(file, read_size)
        byte = read_uint(file, 2)
        self.pad = (byte >> 15) & 0b1
        self.language.append((byte >> 10) & 0b11111)
        self.language.append((byte >> 5) & 0b11111)
        self.language.append(byte & 0b11111)
        self.pre_defined = read_uint(file, 2)

    def __repr__(self):
        repl = ()
        repl += (f"creation_time: {self.creation_time}",)
        repl += (f"modification_time: {self.modification_time}",)
        repl += (f"timescale: {self.timescale}",)
        repl += (f"duration: {self.duration}",)
        repl += (f"pad: {self.pad}",)
        for idx, val in enumerate(self.language):
            repl += (f"language[{idx}]: {val}",)
        repl += (f"pre_defined: {self.pre_defined}",)
        return super().repr(repl)
