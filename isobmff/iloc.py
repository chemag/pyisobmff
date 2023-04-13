# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_int


class ItemLocationBox(FullBox):
    box_type = "iloc"
    is_mandatory = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.offset_size = None
        self.length_size = None
        self.base_offset_size = None
        self.index_size = None
        self.reserved = None
        self.items = []

    def __repr__(self):
        repl = ()
        repl += (f"offset_size: {self.offset_size}",)
        repl += (f"length_size: {self.length_size}",)
        return super().repr(repl)

    # Section 8.11.3.2
    def read(self, file):
        byte = read_int(file, 1)
        self.offset_size = (byte >> 4) & 0b1111
        self.length_size = byte & 0b1111
        byte = read_int(file, 1)
        self.base_offset_size = (byte >> 4) & 0b1111
        if self.version in [1, 2]:
            self.index_size = byte & 0b1111
        else:
            self.reserved = byte & 0b1111
        if self.version < 2:
            item_count = read_int(file, 2)
        elif self.version == 2:
            item_count = read_int(file, 4)
        self.items = []
        for _ in range(item_count):
            item = {}
            if self.version < 2:
                item["item_id"] = read_int(file, 2)
            elif self.version == 2:
                item["item_id"] = read_int(file, 4)
            if self.version in [1, 2]:
                half = read_int(file, 2)
                item["construction_method"] = half & 0b1111
            item["data_reference_index"] = read_int(file, 2)
            item["base_offset"] = read_int(file, self.base_offset_size)
            extent_count = read_int(file, 2)
            item["extents"] = []
            for _ in range(extent_count):
                extent = {}
                if self.version in [1, 2] and self.index_size > 0:
                    item["item_reference_index"] = read_int(file, self.index_size)

                extent["extent_offset"] = read_int(file, self.offset_size)
                extent["extent_length"] = read_int(file, self.length_size)
                item["extents"].append(extent)
            self.items.append(item)
