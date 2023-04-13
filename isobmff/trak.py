# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_box
from .box import read_uint
from .box import read_sint
from .box import int_to_fixed_point_16_16


# ISO/IEC 14496-12:2022, Section 8.3.1
class TrackBox(Box):
    box_type = "trak"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE
    box_list = []

    def read(self, file):
        offset = file.tell()
        max_offset = offset + self.get_payload_size()
        while file.tell() < max_offset:
            box = read_box(file)
            self.box_list.append(box)

    def __repr__(self):
        repl = ()
        for box in self.box_list:
            repl += (repr(box),)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.3.2
class TrackHeaderBox(FullBox):
    box_type = "tkhd"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.creation_time = None
        self.modification_time = None
        self.track_id = None
        self.duration = None
        self.reserved1 = None
        self.reserved2 = []
        self.layer = None
        self.alternate_group = None
        self.volume = None
        self.reserved3 = None
        self.matrix = []
        self.width = None
        self.height = None

    def read(self, file):
        read_size = 8 if self.version == 1 else 4
        self.creation_time = read_uint(file, read_size)
        self.modification_time = read_uint(file, read_size)
        self.track_id = read_uint(file, 4)
        self.reserved1 = read_uint(file, 4)
        self.duration = read_uint(file, read_size)
        for _ in range(2):
            self.reserved2.append(read_uint(file, 4))
        self.layer = read_sint(file, 2)
        self.alternate_group = read_uint(file, 2)
        self.volume = read_uint(file, 2)
        self.reserved3 = read_uint(file, 2)
        for _ in range(9):
            self.matrix.append(read_uint(file, 4))
        self.width = read_uint(file, 4)
        self.height = read_uint(file, 4)

    def __repr__(self):
        repl = ()
        repl += (f"creation_time: {self.creation_time}",)
        repl += (f"modification_time: {self.modification_time}",)
        repl += (f"track_id: {self.track_id}",)
        repl += (f"reserved1: {self.reserved1}",)
        repl += (f"duration: {self.duration}",)
        for idx, val in enumerate(self.reserved2):
            repl += (f"reserved2[{idx}]: {val}",)
        repl += (f"layer: {self.layer}",)
        repl += (f"alternate_group: {self.alternate_group}",)
        repl += (f"volume: 0x{self.volume:04x}",)
        repl += (f"reserved3: {self.reserved3}",)
        for idx, val in enumerate(self.matrix):
            repl += (f"matrix[{idx}]: 0x{val:08x}",)
        repl += (f"width: {int_to_fixed_point_16_16(self.width)}",)
        repl += (f"height: {int_to_fixed_point_16_16(self.height)}",)
        return super().repr(repl)
