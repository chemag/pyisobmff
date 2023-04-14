# -*- coding: utf-8 -*-
from .box import FullBox
from .box import Quantity
from .box import read_box
from .box import read_uint


# ISO/IEC 14496-12:2022, Section 8.7.5
class ChunkOffsetBox(FullBox):
    box_type = "stco"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE
    entries = []

    def read(self, file):
        entry_count = read_uint(file, 4)
        for _ in range(entry_count):
            entry = {}
            entry["chunk_offset"] = read_uint(file, 4)
            self.entries.append(entry)
