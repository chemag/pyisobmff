# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_uint


# ISO/IEC 14496-12:2022, Section 8.11.3.2
class ItemLocationBox(FullBox):
    box_type = b"iloc"
    is_mandatory = False
    items = []

    def read(self, file):
        byte0 = read_uint(file, 1)
        self.offset_size = (byte0 >> 4) & 0b1111
        self.length_size = byte0 & 0b1111
        byte1 = read_uint(file, 1)
        self.base_offset_size = (byte1 >> 4) & 0b1111
        if self.version in [1, 2]:
            self.index_size = byte1 & 0b1111
        else:
            self.reserved = byte1 & 0b1111
        if self.version < 2:
            item_count = read_uint(file, 2)
        elif self.version == 2:
            item_count = read_uint(file, 4)
        self.items = []
        for _ in range(item_count):
            item = {}
            if self.version < 2:
                item["item_id"] = read_uint(file, 2)
            elif self.version == 2:
                item["item_id"] = read_uint(file, 4)
            if self.version in [1, 2]:
                half = read_uint(file, 2)
                item["reserved"] = half >> 4
                item["construction_method"] = half & 0b1111
            item["data_reference_index"] = read_uint(file, 2)
            item["base_offset"] = read_uint(file, self.base_offset_size)
            extent_count = read_uint(file, 2)
            item["extents"] = []
            for _ in range(extent_count):
                extent = {}
                if self.version in [1, 2] and self.index_size > 0:
                    item["item_reference_index"] = read_uint(file, self.index_size)

                extent["extent_offset"] = read_uint(file, self.offset_size)
                extent["extent_length"] = read_uint(file, self.length_size)
                item["extents"].append(extent)
            self.items.append(item)

    def contents(self):
        tuples = super().contents()
        tuples += (("offset_size", self.offset_size),)
        tuples += (("length_size", self.length_size),)
        if self.version in [1, 2]:
            tuples += (("index_size", self.index_size),)
        else:
            tuples += (("reserved", self.reserved),)
        for idx, item in enumerate(self.items):
            tuples += ((f'item[{idx}]["item_id"]', item["item_id"]),)
            if self.version in [1, 2]:
                tuples += ((f'item[{idx}]["reserved"]', item["reserved"]),)
                tuples += (
                    (
                        f'item[{idx}]["construction_method"]',
                        item["construction_method"],
                    ),
                )
            tuples += (
                (f'item[{idx}]["data_reference_index"]', item["data_reference_index"]),
            )
            tuples += ((f'item[{idx}]["base_offset"]', item["base_offset"]),)
            for jdx, extent in enumerate(item["extents"]):
                if self.version in [1, 2] and self.index_size > 0:
                    tuples += (
                        (
                            f'item[{idx}]["extent"][{jdx}]["item_reference_index"]',
                            extent["item_reference_index"],
                        ),
                    )
                tuples += (
                    (
                        f'item[{idx}]["extent"][{jdx}]["extent_offset"]',
                        f'0x{extent["extent_offset"]:08x}',
                    ),
                )
                tuples += (
                    (
                        f'item[{idx}]["extent"][{jdx}]["extent_length"]',
                        extent["extent_length"],
                    ),
                )
        return tuples
