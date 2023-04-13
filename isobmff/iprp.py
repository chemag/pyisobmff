# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_uint
from .box import read_box


# ISO/IEC 14496-12:2022, Section 8.11.4.2
class ItemPropertiesBox(Box):
    box_type = "iprp"
    is_mandatory = False
    quantity = Quantity.ZERO_OR_ONE
    association = []

    def read(self, file):
        self.property_container = read_box(file)
        offset = file.tell()
        max_offset = offset + self.get_payload_size()
        while file.tell() < max_offset:
            box = read_box(file)
            self.association.append(box)

    def __repr__(self):
        repl = ()
        repl += (repr(self.property_container),)
        for box in self.association:
            repl += (repr(box),)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.11.4.2
class ItemPropertyContainer(Box):
    box_type = "ipco"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE


# ISO/IEC 23008-12:2022, Section 6.5.3.2
class ImageSpatialExtents(FullBox):
    box_type = "ispe"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def read(self, file):
        self.width = read_uint(file, 4)
        self.height = read_uint(file, 4)

    def __repr__(self):
        repl = ()
        repl += (f"width: {self.width}",)
        repl += (f"height: {self.height}",)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 12.1.4.2
class PixelAspectRatio(Box):
    box_type = "pasp"

    def read(self, file):
        self.hSpacing = read_uint(file, 4)
        self.vSpacing = read_uint(file, 4)

    def __repr__(self):
        repl = ()
        repl += (f"hSpacing: {self.hSpacing}",)
        repl += (f"vSpacing: {self.vSpacing}",)
        return super().repr(repl)


class ColorInformation(Box):
    box_type = "colr"

    def read(self, file):
        print(f"colr: {file.read(self.get_payload_size())}")


class PixelInformation(Box):
    box_type = "pixi"

    def read(self, file):
        print(f"pixi: {file.read(self.get_payload_size())}")


class RelativeInformation(Box):
    box_type = "rloc"

    def read(self, file):
        print(f"rloc: {file.read(self.get_payload_size())}")


# ISO/IEC 14496-12:2022, Section 8.11.4.2
class ItemPropertyAssociation(FullBox):
    box_type = "ipma"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = []

    def read(self, file):
        entry_count = read_uint(file, 4)
        id_size = 2 if self.version < 1 else 4
        for _ in range(entry_count):
            item = {}
            item["id"] = read_uint(file, id_size)
            association_count = read_uint(file, 1)
            item["associations"] = []
            for __ in range(association_count):
                association = {}
                if self.flags & 0b1:
                    byte = read_uint(file, 2)
                    association["essential"] = (byte >> 15) & 0b1
                    association["property_index"] = byte & 0b111111111111111
                else:
                    byte = read_uint(file, 1)
                    association["essential"] = (byte >> 7) & 0b1
                    association["property_index"] = byte & 0b1111111
                item["associations"].append(association)
            self.items.append(item)
