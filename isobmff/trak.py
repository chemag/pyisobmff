# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_uint
from .box import read_sint
from .box import int_to_fixed_point_16_16


# ISO/IEC 14496-12:2022, Section 8.3.1
class TrackBox(Box):
    box_type = b"trak"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE

    def read(self, file):
        self.box_list = self.read_box_list(file)

    def contents(self):
        tuples = super().contents()
        for idx, box in enumerate(self.box_list):
            tuples += ((f"box[{idx}]", box.contents()),)
        return tuples


# ISO/IEC 14496-12:2022, Section 8.3.2
class TrackHeaderBox(FullBox):
    box_type = b"tkhd"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE

    def read(self, file):
        read_size = 8 if self.version == 1 else 4
        self.creation_time = read_uint(file, read_size)
        self.modification_time = read_uint(file, read_size)
        self.track_id = read_uint(file, 4)
        self.reserved1 = read_uint(file, 4)
        self.duration = read_uint(file, read_size)
        self.reserved2 = []
        for _ in range(2):
            self.reserved2.append(read_uint(file, 4))
        self.layer = read_sint(file, 2)
        self.alternate_group = read_uint(file, 2)
        self.volume = read_uint(file, 2)
        self.reserved3 = read_uint(file, 2)
        self.matrix = []
        for _ in range(9):
            self.matrix.append(read_uint(file, 4))
        self.width = read_uint(file, 4)
        self.height = read_uint(file, 4)

    def contents(self):
        tuples = super().contents()
        tuples += (("creation_time", self.creation_time),)
        tuples += (("modification_time", self.modification_time),)
        tuples += (("track_id", self.track_id),)
        tuples += (("reserved1", self.reserved1),)
        tuples += (("duration", self.duration),)
        for idx, val in enumerate(self.reserved2):
            tuples += ((f"reserved2[{idx}]", val),)
        tuples += (("layer", self.layer),)
        tuples += (("alternate_group", self.alternate_group),)
        tuples += (("volume", f"0x{self.volume:04x}"),)
        tuples += (("reserved3", self.reserved3),)
        for idx, val in enumerate(self.matrix):
            tuples += ((f"matrix[{idx}]", f"0x{val:08x}"),)
        tuples += (("width", f"{int_to_fixed_point_16_16(self.width)}"),)
        tuples += (("height", f"{int_to_fixed_point_16_16(self.height)}"),)
        return tuples
