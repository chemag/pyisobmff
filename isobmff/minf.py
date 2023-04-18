# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_uint, read_sint


# ISO/IEC 14496-12:2022, Section 8.4.4.2
class MediaInformationBox(Box):
    box_type = b"minf"
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


# ISO/IEC 14496-12:2022, Section 12.1.2
class VideoMediaHeaderBox(FullBox):
    box_type = b"vmhd"
    is_mandatory = True
    opcolor = []

    def read(self, file):
        self.graphicsmode = read_uint(file, 2)
        for _ in range(3):
            self.opcolor.append(read_uint(file, 2))

    def contents(self):
        tuples = super().contents()
        tuples += (("graphicsmode", self.graphicsmode),)
        for idx, val in enumerate(self.opcolor):
            tuples += ((f"opcolor[{idx}]", val),)
        return tuples


# ISO/IEC 14496-12:2022, Section 12.2.2
class SoundMediaHeaderBox(FullBox):
    box_type = b"smhd"
    is_mandatory = True

    def read(self, file):
        self.balance = read_sint(file, 2)
        self.reserved = read_uint(file, 2)

    def contents(self):
        tuples = super().contents()
        tuples += (("balance", self.balance),)
        tuples += (("reserved", self.reserved),)
        return tuples


# ISO/IEC 14496-12:2022, Section 12.4.3
class HintMediaHeaderBox(FullBox):
    box_type = b"hmhd"
    is_mandatory = True

    def read(self, file):
        self.max_pdu_size = read_uint(file, 2)
        self.avg_pdu_size = read_uint(file, 2)
        self.max_bit_rate = read_uint(file, 4)
        self.avg_bit_rate = read_uint(file, 4)
        self.reserved = read_uint(file, 4)

    def contents(self):
        tuples = super().contents()
        tuples += (("max_pdu_size", self.max_pdu_size),)
        tuples += (("avg_pdu_size", self.avg_pdu_size),)
        tuples += (("max_bit_rate", self.max_bit_rate),)
        tuples += (("avg_bit_rate", self.avg_bit_rate),)
        tuples += (("reserved", self.reserved),)
        return tuples


# ISO/IEC 14496-12:2022, Section 8.4.5.2
class NullMediaHeaderBox(FullBox):
    box_type = b"nmhd"
    is_mandatory = True


# ISO/IEC 14496-12:2022, Section 12.6
class SubtitleMediaHeaderBox(FullBox):
    box_type = b"sthd"
