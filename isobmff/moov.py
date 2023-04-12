# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import indent
from .box import read_box
from .box import read_int


class MovieBox(Box):
    box_type = 'moov'
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE

class MovieHeaderBox(FullBox):
    box_type = 'mvhd'
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE

    def __init__(self, size, version, flags):
        super().__init__(size=size, version=version, flags=flags)
        self.creation_time = None
        self.modification_time = None
        self.timescale = None
        self.duration = None
        self.rate = None
        self.volume = None
        self.reserved1 = None
        self.reserved2 = []
        self.matrix = []
        self.pre_defined = []
        self.next_track_id = None

    def read(self, file):
        read_size = 8 if self.version == 1 else 4
        self.creation_time = read_int(file, read_size)
        self.modification_time = read_int(file, read_size)
        self.timescale = read_int(file, 4)
        self.duration = read_int(file, read_size)
        self.rate = read_int(file, 4)
        self.volume = read_int(file, 2)
        self.reserved1 = read_int(file, 2)
        for _ in range(2):
            self.reserved2.append(read_int(file, 4))
        for _ in range(9):
            self.matrix.append(read_int(file, 4))
        for _ in range(6):
            self.pre_defined.append(read_int(file, 4))
        self.next_track_id = read_int(file, 4)
