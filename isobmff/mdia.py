# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_uint


# ISO/IEC 14496-12:2022, Section 8.4.1.1
class MediaBox(Box):
    box_type = b"mdia"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE
    box_list = []

    def read(self, file):
        self.box_list = self.read_box_list(file)

    def contents(self):
        tuples = super().contents()
        for idx, box in enumerate(self.box_list):
            tuples += ((f"box[{idx}]", box.contents()),)
        return tuples


# ISO/IEC 14496-12:2022, Section 8.4.2.1
class MediaHeaderBox(FullBox):
    box_type = b"mdhd"
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

    def contents(self):
        tuples = super().contents()
        tuples += (("creation_time", self.creation_time),)
        tuples += (("modification_time", self.modification_time),)
        tuples += (("timescale", self.timescale),)
        tuples += (("duration", self.duration),)
        tuples += (("pad", self.pad),)
        for idx, val in enumerate(self.language):
            tuples += ((f"language[{idx}]", val),)
        tuples += (("pre_defined", self.pre_defined),)
        return tuples
