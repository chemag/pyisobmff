# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import read_box
from .box import read_uint
from .box import read_bytes
from .box import read_utf8string
from .stbl import VisualSampleEntry


# ETSI TS 103 190-2 v1.2.1, Section E.4
class AC4SampleEntry(Box):
    box_type = b"ac-4"
    box_list = []

    def read(self, file):
        self.reserved1 = read_uint(file, 6)
        self.data_reference_index = read_uint(file, 2)
        self.reserved2 = read_uint(file, 8)
        self.channel_count = read_uint(file, 2)
        self.sample_size = read_uint(file, 2)
        self.reserved3 = read_uint(file, 4)
        self.sampling_frequency = read_uint(file, 2)
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
        repl += (f"sampling_frequency: {self.sampling_frequency}",)
        repl += (f"reserved4: {self.reserved4}",)
        for box in self.box_list:
            repl += (repr(box),)
        return super().repr(repl)
