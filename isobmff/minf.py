# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_box
from .box import read_uint, read_sint


# ISO/IEC 14496-12:2022, Section 8.4.4.2
class MediaInformationBox(Box):
    box_type = "minf"
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


# ISO/IEC 14496-12:2022, Section 12.1.2
class VideoMediaHeaderBox(FullBox):
    box_type = "vmhd"
    is_mandatory = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.graphicsmode = None
        self.opcolor = []

    def read(self, file):
        self.graphicsmode = read_uint(file, 2)
        for _ in range(3):
            self.opcolor.append(read_uint(file, 2))


# ISO/IEC 14496-12:2022, Section 12.2.2
class SoundMediaHeaderBox(FullBox):
    box_type = "smhd"
    is_mandatory = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.balance = None
        self.reserved = None

    def read(self, file):
        self.balance = read_sint(file, 2)
        self.reserved = read_uint(file, 2)


# ISO/IEC 14496-12:2022, Section 12.4.3
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
        self.max_pdu_size = read_uint(file, 2)
        self.avg_pdu_size = read_uint(file, 2)
        self.max_bit_rate = read_uint(file, 4)
        self.avg_bit_rate = read_uint(file, 4)
        self.reserved = read_uint(file, 4)


# ISO/IEC 14496-12:2022, Section 8.4.5.2
class NullMediaHeaderBox(FullBox):
    box_type = "nmhd"
    is_mandatory = True
