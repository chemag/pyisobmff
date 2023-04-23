# -*- coding: utf-8 -*-
from .box import FullBox
from .box import Quantity
from .box import read_uint
from .box import read_bytes


# ISO/IEC 14496-12:2022, Section 8.7.4
class SampleToChunkBox(FullBox):
    box_type = b"stsc"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE

    def read(self, file):
        entry_count = read_uint(file, 4)
        self.entries = []
        for _ in range(entry_count):
            entry = {}
            entry["first_chunk"] = read_uint(file, 4)
            entry["samples_per_chunk"] = read_uint(file, 4)
            entry["sample_description_index"] = read_uint(file, 4)
            self.entries.append(entry)
        # read the rest of the box
        max_len = self.max_offset - file.tell()
        self.remaining = read_bytes(file, max_len)
