# -*- coding: utf-8 -*-
from .box import Box
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
        self.box_list = self.read_box_list(file)

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


# ETSI TS 102 366 v1.4.1, Section F.5
class EC3SampleEntry(Box):
    box_type = b"ec-3"
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
        self.box_list = self.read_box_list(file)

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


# ETSI TS 102 366 v1.4.1, Section F.6
class EC3SpecificBox(Box):
    box_type = b"dec3"
    subs = []

    def read(self, file):
        half = read_uint(file, 2)
        self.data_rate = half >> 13
        num_ind_sub = half & 0x07
        for _ in range(num_ind_sub):
            sub = {}
            byte1 = read_uint(file, 1)
            sub["fscod"] = byte1 >> 6
            sub["bsid"] = (byte1 >> 1) & 0x1F
            sub["reserved1"] = byte1 & 0x01
            byte2 = read_uint(file, 1)
            sub["avsc"] = byte2 >> 7
            sub["bsmod"] = (byte2 >> 4) & 0x07
            sub["acmod"] = (byte2 >> 1) & 0x07
            sub["lfeon"] = byte2 & 0x01
            byte3 = read_uint(file, 1)
            sub["reserved2"] = byte3 >> 5
            sub["num_dep_sub"] = (byte3 >> 1) & 0x0F
            rem = byte3 & 0x01
            if sub["num_dep_sub"] > 0:
                byte4 = read_uint(file, 1)
                rem = (rem << 8) | byte4
                sub["chan_loc"] = rem
            else:
                sub["reserved3"] = rem
            self.subs.append(sub)
        max_len = self.get_max_offset() - file.tell()
        self.reserved4 = read_uint(file, max_len)

    def __repr__(self):
        repl = ()
        repl += (f"data_rate: {self.data_rate}",)
        for idx, val in enumerate(self.subs):
            repl += (f'sub[{idx}]["fscod"]: {val["fscod"]}',)
            repl += (f'sub[{idx}]["bsid"]: {val["bsid"]}',)
            repl += (f'sub[{idx}]["reserved1"]: {val["reserved1"]}',)
            repl += (f'sub[{idx}]["avsc"]: {val["avsc"]}',)
            repl += (f'sub[{idx}]["bsmod"]: {val["bsmod"]}',)
            repl += (f'sub[{idx}]["acmod"]: {val["acmod"]}',)
            repl += (f'sub[{idx}]["lfeon"]: {val["lfeon"]}',)
            repl += (f'sub[{idx}]["reserved2"]: {val["reserved2"]}',)
            repl += (f'sub[{idx}]["num_dep_sub"]: {val["num_dep_sub"]}',)
            if "reserved3" in val:
                repl += (f'sub[{idx}]["reserved3"]: {val["reserved3"]}',)
            else:
                repl += (f'sub[{idx}]["chan_loc"]: {val["chan_loc"]}',)
        repl += (f"reserved4: {self.reserved4}",)
        return super().repr(repl)
