# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_box
from .box import read_uint


# ISO/IEC 14496-12:2022, Section 8.2.1
class MovieBox(Box):
    box_type = "moov"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE
    box_list = []

    def read(self, file):
        while file.tell() < self.get_max_offset():
            box = read_box(file, self.debug)
            self.box_list.append(box)

    def __repr__(self):
        repl = ()
        for box in self.box_list:
            repl += (repr(box),)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.2.2
class MovieHeaderBox(FullBox):
    box_type = "mvhd"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE
    reserved2 = []
    matrix = []
    pre_defined = []

    def read(self, file):
        read_size = 8 if self.version == 1 else 4
        self.creation_time = read_uint(file, read_size)
        self.modification_time = read_uint(file, read_size)
        self.timescale = read_uint(file, 4)
        self.duration = read_uint(file, read_size)
        self.rate = read_uint(file, 4)
        self.volume = read_uint(file, 2)
        self.reserved1 = read_uint(file, 2)
        for _ in range(2):
            self.reserved2.append(read_uint(file, 4))
        for _ in range(9):
            self.matrix.append(read_uint(file, 4))
        for _ in range(6):
            self.pre_defined.append(read_uint(file, 4))
        self.next_track_id = read_uint(file, 4)

    def __repr__(self):
        repl = ()
        repl += (f"creation_time: {self.creation_time}",)
        repl += (f"modification_time: {self.modification_time}",)
        repl += (f"timescale: {self.timescale}",)
        repl += (f"duration: {self.duration}",)
        repl += (f"rate: 0x{self.creation_time:08x}",)
        repl += (f"volume: 0x{self.volume:04x}",)
        repl += (f"reserved1: {self.reserved1}",)
        for idx, val in enumerate(self.reserved2):
            repl += (f"reserved2[{idx}]: {val}",)
        for idx, val in enumerate(self.matrix):
            repl += (f"matrix[{idx}]: 0x{val:08x}",)
        for idx, val in enumerate(self.pre_defined):
            repl += (f"pre_defined[{idx}]: {val}",)
        repl += (f"next_track_id: {self.next_track_id}",)
        return super().repr(repl)
