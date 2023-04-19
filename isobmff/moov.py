# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_uint


# ISO/IEC 14496-12:2022, Section 8.2.1
class MovieBox(Box):
    box_type = b"moov"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE

    def read(self, file):
        self.box_list = self.read_box_list(file)

    def contents(self):
        tuples = super().contents()
        for idx, box in enumerate(self.box_list):
            tuples += ((f"box[{idx}]", box.contents()),)
        return tuples


# ISO/IEC 14496-12:2022, Section 8.2.2
class MovieHeaderBox(FullBox):
    box_type = b"mvhd"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE

    def read(self, file):
        read_size = 8 if self.version == 1 else 4
        self.creation_time = read_uint(file, read_size)
        self.modification_time = read_uint(file, read_size)
        self.timescale = read_uint(file, 4)
        self.duration = read_uint(file, read_size)
        self.rate = read_uint(file, 4)
        self.volume = read_uint(file, 2)
        self.reserved1 = read_uint(file, 2)
        self.reserved2 = []
        for _ in range(2):
            self.reserved2.append(read_uint(file, 4))
        self.matrix = []
        for _ in range(9):
            self.matrix.append(read_uint(file, 4))
        self.pre_defined = []
        for _ in range(6):
            self.pre_defined.append(read_uint(file, 4))
        self.next_track_id = read_uint(file, 4)

    def contents(self):
        tuples = super().contents()
        tuples += (("creation_time", self.creation_time),)
        tuples += (("modification_time", self.modification_time),)
        tuples += (("timescale", self.timescale),)
        tuples += (("duration", self.duration),)
        tuples += (("rate", f"0x{self.creation_time:08x}"),)
        tuples += (("volume", f"0x{self.volume:04x}"),)
        tuples += (("reserved1", self.reserved1),)
        for idx, val in enumerate(self.reserved2):
            tuples += ((f"reserved2[{idx}]", val),)
        for idx, val in enumerate(self.matrix):
            tuples += ((f"matrix[{idx}]", f"0x{val:08x}"),)
        for idx, val in enumerate(self.pre_defined):
            tuples += (("pre_defined[{idx}]", val),)
        tuples += (("next_track_id", self.next_track_id),)
        return tuples
