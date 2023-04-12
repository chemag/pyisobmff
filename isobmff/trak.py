# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import indent
from .box import read_int


class TrackBox(Box):
    box_type = 'trak'
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE

class TrackHeaderBox(FullBox):
    box_type = 'tkhd'
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE

    def __init__(self, size, version, flags):
        super().__init__(size=size, version=version, flags=flags)
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
        self.creation_time = read_int(file, read_size)
        self.modification_time = read_int(file, read_size)
        self.track_id = read_int(file, 4)
        self.reserved1 = read_int(file, 4)
        self.duration = read_int(file, read_size)
        for _ in range(2):
            self.reserved2.append(read_int(file, 4))
        self.layer = read_int(file, 2)
        self.alternate_group = read_int(file, 2)
        self.volume = read_int(file, 2)
        self.reserved3 = read_int(file, 2)
        for _ in range(9):
            self.matrix.append(read_int(file, 4))
        self.width = read_int(file, 4)
        self.height = read_int(file, 4)
