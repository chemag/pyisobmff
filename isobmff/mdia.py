# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import indent
from .box import read_int


class MediaBox(Box):
    box_type = "mdia"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE


class MediaHeaderBox(FullBox):
    box_type = "mdhd"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE

    def __init__(self, size, version, flags):
        super().__init__(size=size, version=version, flags=flags)
        self.creation_time = None
        self.modification_time = None
        self.timescale = None
        self.duration = None
        self.pad = None
        self.language = []  # ISO-639-2/T language code
        self.pre_defined = None

    def read(self, file):
        read_size = 8 if self.version == 1 else 4
        self.creation_time = read_int(file, read_size)
        self.modification_time = read_int(file, read_size)
        self.timescale = read_int(file, 4)
        self.duration = read_int(file, read_size)
        byte = read_int(file, 2)
        self.pad = (byte >> 15) & 0b1
        self.language.append((byte >> 10) & 0b11111)
        self.language.append((byte >> 5) & 0b11111)
        self.language.append(byte & 0b11111)
        self.pre_defined = read_int(file, 2)
