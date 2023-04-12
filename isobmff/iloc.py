# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_int
from .box import indent


class ItemLocationBox(FullBox):
    box_type = 'iloc'
    is_mandatory = False

    def __init__(self, size, version, flags):
        super().__init__(size=size, version=version, flags=flags)
        self.offset_size = None
        self.length_size = None
        self.base_offset_size = None
        self.reserved = None
        self.items = []

    def __repr__(self):
        rep = 'offset_size:' + str(self.offset_size) + '\n'
        rep += 'length_size:' + str(self.length_size)
        return super().__repr__() + indent(rep)

    def read(self, file):
        byte = read_int(file, 1)
        self.offset_size = (byte >> 4) & 0b1111
        self.length_size = byte & 0b1111
        byte = read_int(file, 1)
        self.base_offset_size = (byte >> 4) & 0b1111
        self.reserved = byte & 0b1111
        self.items = []
        item_count = read_int(file, 2)

        for _ in range(item_count):
            item = {}
            item['item_id'] = read_int(file, 2)
            item['data_reference_index'] = read_int(file, 2)
            item['base_offset'] = read_int(file, self.base_offset_size)
            extent_count = read_int(file, 2)
            item['extents'] = []
            for _ in range(extent_count):
                extent = {}
                extent['extent_offset'] = read_int(file, self.offset_size)
                extent['extent_length'] = read_int(file, self.length_size)
                item['extents'].append(extent)
            self.items.append(item)
