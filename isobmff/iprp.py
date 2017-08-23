# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_int


class ItemPropertiesBox(Box):
    box_type = 'iprp'
    is_mandatry = False
    quantity = Quantity.ZERO_OR_ONE

class ItemPropertyContainer(Box):
    box_type = 'ipco'
    is_mandatry = True
    quantity = Quantity.EXACTLY_ONE

class ImageSpatialExtents(FullBox):
    box_type = 'ispe'

    def __init__(self, size, version, flags):
        super().__init__(size=size, version=version, flags=flags)
        self.width = None
        self.height = None

    def read(self, file):
        self.width = read_int(file, 4)
        self.height = read_int(file, 4)


class PixelAspectRatio(Box):
    box_type = 'pasp'

    def read(self, file):
        print(file.read(self.get_box_size()))

class ColorInformation(Box):
    box_type = 'colr'

    def read(self, file):
        print(file.read(self.get_box_size()))

class PixelInformation(Box):
    box_type = 'pixi'

    def read(self, file):
        print(file.read(self.get_box_size()))

class RelativeInformation(Box):
    box_type = 'rloc'

    def read(self, file):
        print(file.read(self.get_box_size()))

class ItemPropertyAssociation(FullBox):
    box_type = 'ipma'
    is_mandatry = True
    quantity = Quantity.EXACTLY_ONE

    def __init__(self, size, version, flags):
        super().__init__(size=size, version=version, flags=flags)
        self.items = []

    def read(self, file):
        entry_count = read_int(file, 4)
        id_size = 2 if self.version < 1 else 4
        for _ in range(entry_count):
            item = {}
            item['id'] = read_int(file, id_size)
            association_count = read_int(file, 1)
            item['associations'] = []
            for __ in range(association_count):
                association = {}
                if self.flags & 0b1:
                    byte = read_int(file, 2)
                    association['essential'] = (byte >> 15) & 0b1
                    association['property_index'] = byte & 0b111111111111111
                else:
                    byte = read_int(file, 1)
                    association['essential'] = (byte >> 7) & 0b1
                    association['property_index'] = byte & 0b1111111
                item['associations'].append(association)
            self.items.append(item)
