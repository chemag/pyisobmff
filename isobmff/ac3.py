# -*- coding: utf-8 -*-
from .box import Box
from .box import read_box
from .box import read_uint
from .box import read_bytes
from .stbl import VisualSampleEntry


# ETSI TS 102 366 v1.4.1, Section F.3
class AC3SampleEntry(Box):
    box_type = b"ac-3"
    box_list = []

    def read(self, file):
        self.reserved1 = read_uint(file, 6)
        self.data_reference_index = read_uint(file, 2)
        self.reserved2 = read_uint(file, 8)
        self.channel_count = read_uint(file, 2)
        self.sample_size = read_uint(file, 2)
        self.reserved3 = read_uint(file, 4)
        self.sampling_rate = read_uint(file, 2)
        self.reserved4 = read_uint(file, 2)
        while file.tell() < self.get_max_offset():
            box = read_box(file, self.debug)
            self.box_list.append(box)

    def __repr__(self):
        repl = ()
        repl += (f"reserved1: {self.reserved1}",)
        repl += (f"data_reference_index: {self.data_reference_index}",)
        repl += (f"reserved2: {self.reserved2}",)
        repl += (f"channel_count: {self.channel_count}",)
        repl += (f"sample_size: {self.sample_size}",)
        repl += (f"reserved3: {self.reserved3}",)
        repl += (f"sampling_rate: {self.sampling_rate}",)
        repl += (f"reserved4: {self.reserved4}",)
        for box in self.box_list:
            repl += (repr(box),)
        return super().repr(repl)


# ETSI TS 102 366 v1.4.1, Section F.4
class AC3SpecificBox(Box):
    box_type = b"dac3"

    def read(self, file):
        total_bytes = read_uint(file, 3)
        self.fscod = total_bytes >> 22
        self.bsid = (total_bytes >> 17) & 0x1F
        self.bsmod = (total_bytes >> 14) & 0x07
        self.acmod = (total_bytes >> 11) & 0x07
        self.lfeon = (total_bytes >> 10) & 0x01
        self.bit_rate_code = (total_bytes >> 5) & 0x1F
        self.reserved = total_bytes & 0x1F

    def __repr__(self):
        repl = ()
        repl += (f"fscod: {self.fscod}",)
        repl += (f"bsid: {self.bsid}",)
        repl += (f"bsmod: {self.bsmod}",)
        repl += (f"acmod: {self.acmod}",)
        repl += (f"lfeon: {self.lfeon}",)
        repl += (f"bit_rate_code: {self.bit_rate_code}",)
        repl += (f"reserved: {self.reserved}",)
        return super().repr(repl)
