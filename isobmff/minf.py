# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_int


class MediaInformationBox(Box):
    box_type = "minf"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE


class VideoMediaHeaderBox(FullBox):
    box_type = "vmhd"
    is_mandatory = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.graphicsmode = None
        self.opcolor = []

    def read(self, file):
        self.graphicsmode = read_int(file, 2)
        for _ in range(3):
            self.opcolor.append(read_int(file, 2))


class SoundMediaHeaderBox(FullBox):
    box_type = "smhd"
    is_mandatory = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.balance = None
        self.reserved = None

    def read(self, file):
        self.balance = read_int(file, 2)
        self.reserved = read_int(file, 2)


class HintMediaHeaderBox(FullBox):
    box_type = "hmhd"
    is_mandatory = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_pdu_size = None
        self.avg_pdu_size = None
        self.max_bit_rate = None
        self.avg_bit_rate = None
        self.reserved = None

    def read(self, file):
        self.max_pdu_size = read_int(file, 2)
        self.avg_pdu_size = read_int(file, 2)
        self.max_bit_rate = read_int(file, 4)
        self.avg_bit_rate = read_int(file, 4)
        self.reserved = read_int(file, 4)


class NullMediaHeaderBox(FullBox):
    box_type = "nmhd"
    is_mandatory = True
