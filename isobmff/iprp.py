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
    properties = []

    def read(self, file):
        self.property_container = read_box(file)
        offset = file.tell()
        max_offset = offset + self.get_payload_size()
        while file.tell() < max_offset:
            box = read_box(file)
            self.properties.append(box)

    def __repr__(self):
        repl = ()
        for box in self.properties:
            repl += (repr(box),)
        return super().repr(repl)


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
    entries = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def read(self, file):
        entry_count = read_uint(file, 4)
        entry = {}
        for _ in range(entry_count):
            if self.version < 1:
                entry["item_id"] = read_uint(file, 2)
            else:
                entry["item_id"] = read_uint(file, 4)
            association_count = read_uint(file, 1)
            associations = []
            for _ in range(association_count):
                if self.flags & 1 == 1:
                    item = read_uint(file, 2)
                    essential = item >> 15
                    property_index = item & 0x7FFF
                else:
                    item = read_uint(file, 1)
                    essential = item >> 7
                    property_index = item & 0x7F
                association = {
                    "item": item,
                    "essential": essential,
                    "property_index": property_index,
                }
                associations.append(association)
            entry["associations"] = associations
        self.entries.append(entry)

    def __repr__(self):
        repl = ()
        for idx, entry in enumerate(self.entries):
            repl += (f'entry[{idx}]["item_id"]: {entry["item_id"]}',)
            for jdx, association in enumerate(entry["associations"]):
                repl += (
                    f'entry[{idx}]["associations"][{jdx}]["item"]: {association["item"]}',
                )
                repl += (
                    f'entry[{idx}]["associations"][{jdx}]["essential"]: {association["essential"]}',
                )
                repl += (
                    f'entry[{idx}]["associations"][{jdx}]["property_index"]: {association["property_index"]}',
                )
        return super().repr(repl)
