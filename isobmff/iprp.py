# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .utils import read_uint


# ISO/IEC 14496-12:2022, Section 8.11.14.2
class ItemProperty(Box):
    pass


# ISO/IEC 14496-12:2022, Section 8.11.14.2
class ItemFullProperty(FullBox):
    pass


# ISO/IEC 14496-12:2022, Section 8.11.14.2
class ItemPropertiesBox(Box):
    box_type = b"iprp"
    is_mandatory = False
    quantity = Quantity.ZERO_OR_ONE

    def read(self, file):
        # must be ItemPropertyContainerBox
        self.property_container = self.read_box(file)
        # must be ItemPropertyAssociationBox
        self.association = self.read_box_list(file)

    def contents(self):
        tuples = super().contents()
        tuples += (("property_container", self.property_container.contents()),)
        for idx, box in enumerate(self.association):
            tuples += ((f"box[{idx}]", box.contents()),)
        return tuples


# ISO/IEC 14496-12:2022, Section 8.11.14.2
class ItemPropertyContainerBox(Box):
    box_type = b"ipco"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE

    def read(self, file):
        # boxes derived from ItemProperty, ItemFullProperty,
        # or FreeSpaceBox
        self.properties = self.read_box_list(file)

    def contents(self):
        tuples = super().contents()
        for idx, box in enumerate(self.properties):
            tuples += ((f"property[{idx}]", box.contents()),)
        return tuples


# ISO/IEC 14496-12:2022, Section 8.11.14.2
class ItemPropertyAssociationBox(FullBox):
    box_type = b"ipma"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE

    def read(self, file):
        entry_count = read_uint(file, 4)
        self.entries = []
        for _ in range(entry_count):
            entry = {}
            if self.version < 1:
                entry["item_id"] = read_uint(file, 2)
            else:
                entry["item_id"] = read_uint(file, 4)
            association_count = read_uint(file, 1)
            entry["associations"] = []
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
                    "essential": essential,
                    "property_index": property_index,
                }
                entry["associations"].append(association)
            self.entries.append(entry)

    def contents(self):
        tuples = super().contents()
        for idx, entry in enumerate(self.entries):
            tuples += ((f'entry[{idx}]["item_id"]', entry["item_id"]),)
            for jdx, association in enumerate(entry["associations"]):
                tuples += (
                    (
                        f'entry[{idx}]["associations"][{jdx}]["essential"]',
                        association["essential"],
                    ),
                )
                tuples += (
                    (
                        f'entry[{idx}]["associations"][{jdx}]["property_index"]',
                        association["property_index"],
                    ),
                )
        return tuples
