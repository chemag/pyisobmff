# -*- coding: utf-8 -*-
from .box import FullBox
from .box import Quantity
from .box import read_uint


# ISO/IEC 14496-12:2022, Section 8.7.5
class ChunkOffsetBox(FullBox):
    box_type = b"stco"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE

    def read(self, file):
        entry_count = read_uint(file, 4)
        self.entries = []
        for _ in range(entry_count):
            entry = {}
            entry["chunk_offset"] = read_uint(file, 4)
            self.entries.append(entry)

    def contents(self):
        tuples = super().contents()
        for idx, val in enumerate(self.entries):
            tuples += ((f'entry[{idx}]["chunk_offset"]', val["chunk_offset"]),)
        return tuples


# ISO/IEC 14496-12:2022, Section 8.7.5
class ChunkLargeOffsetBox(FullBox):
    box_type = b"co64"

    def read(self, file):
        entry_count = read_uint(file, 4)
        self.entries = []
        for _ in range(entry_count):
            entry = {}
            entry["chunk_offset"] = read_uint(file, 8)
            self.entries.append(entry)

    def contents(self):
        tuples = super().contents()
        for idx, val in enumerate(self.entries):
            tuples += ((f'entry[{idx}]["chunk_offset"]', val["chunk_offset"]),)
        return tuples
