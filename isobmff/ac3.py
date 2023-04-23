# -*- coding: utf-8 -*-
from .box import Box
from .box import read_uint


# ETSI TS 102 366 v1.4.1, Section F.3
class AC3SampleEntry(Box):
    box_type = b"ac-3"

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

    def contents(self):
        tuples = super().contents()
        tuples += (("reserved1", self.reserved1),)
        tuples += (("data_reference_index", self.data_reference_index),)
        tuples += (("reserved2", self.reserved2),)
        tuples += (("channel_count", self.channel_count),)
        tuples += (("sample_size", self.sample_size),)
        tuples += (("reserved3", self.reserved3),)
        tuples += (("sampling_rate", self.sampling_rate),)
        tuples += (("reserved4", self.reserved4),)
        for idx, box in enumerate(self.box_list):
            tuples += ((f"box[{idx}]", box.contents()),)
        return tuples


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

    def contents(self):
        tuples = super().contents()
        tuples += (("fscod", self.fscod),)
        tuples += (("bsid", self.bsid),)
        tuples += (("bsmod", self.bsmod),)
        tuples += (("acmod", self.acmod),)
        tuples += (("lfeon", self.lfeon),)
        tuples += (("bit_rate_code", self.bit_rate_code),)
        tuples += (("reserved", self.reserved),)
        return tuples


# ETSI TS 102 366 v1.4.1, Section F.5
class EC3SampleEntry(Box):
    box_type = b"ec-3"

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

    def contents(self):
        tuples = super().contents()
        tuples += (("reserved1", self.reserved1),)
        tuples += (("data_reference_index", self.data_reference_index),)
        tuples += (("reserved2", self.reserved2),)
        tuples += (("channel_count", self.channel_count),)
        tuples += (("sample_size", self.sample_size),)
        tuples += (("reserved3", self.reserved3),)
        tuples += (("sampling_rate", self.sampling_rate),)
        tuples += (("reserved4", self.reserved4),)
        for idx, box in enumerate(self.box_list):
            tuples += ((f"box[{idx}]", box.contents()),)
        return tuples


# ETSI TS 102 366 v1.4.1, Section F.6
class EC3SpecificBox(Box):
    box_type = b"dec3"

    def read(self, file):
        half = read_uint(file, 2)
        self.data_rate = half >> 13
        num_ind_sub = half & 0x07
        self.subs = []
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
        max_len = self.max_offset - file.tell()
        self.reserved4 = read_uint(file, max_len)

    def contents(self):
        tuples = super().contents()
        tuples += (("data_rate", self.data_rate),)
        for idx, val in enumerate(self.subs):
            tuples += ((f'sub[{idx}]["fscod"]', val["fscod"]),)
            tuples += ((f'sub[{idx}]["bsid"]', val["bsid"]),)
            tuples += ((f'sub[{idx}]["reserved1"]', val["reserved1"]),)
            tuples += ((f'sub[{idx}]["avsc"]', val["avsc"]),)
            tuples += ((f'sub[{idx}]["bsmod"]', val["bsmod"]),)
            tuples += ((f'sub[{idx}]["acmod"]', val["acmod"]),)
            tuples += ((f'sub[{idx}]["lfeon"]', val["lfeon"]),)
            tuples += ((f'sub[{idx}]["reserved2"]', val["reserved2"]),)
            tuples += ((f'sub[{idx}]["num_dep_sub"]', val["num_dep_sub"]),)
            if "reserved3" in val:
                tuples += ((f'sub[{idx}]["reserved3"]', val["reserved3"]),)
            else:
                tuples += ((f'sub[{idx}]["chan_loc"]', val["chan_loc"]),)
        tuples += (("reserved4", self.reserved4),)
        return tuples
