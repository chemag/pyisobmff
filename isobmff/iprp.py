# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_uint
from .box import read_fixed_size_string
from .box import read_bytes
from .box import read_box


# ISO/IEC 14496-12:2022, Section 8.11.14.2
class ItemProperty(Box):
    pass


# ISO/IEC 14496-12:2022, Section 8.11.14.2
class ItemFullProperty(FullBox):
    pass


# ISO/IEC 14496-12:2022, Section 8.11.14.2
class ItemPropertiesBox(Box):
    box_type = "iprp"
    is_mandatory = False
    quantity = Quantity.ZERO_OR_ONE
    association = []

    def read(self, file):
        # must be ItemPropertyContainerBox
        self.property_container = read_box(file, self.debug)
        while file.tell() < self.get_max_offset():
            # must be ItemPropertyAssociationBox
            box = read_box(file, self.debug)
            self.association.append(box)

    def __repr__(self):
        repl = ()
        repl += (repr(self.property_container),)
        for box in self.association:
            repl += (repr(box),)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.11.14.2
class ItemPropertyContainer(Box):
    box_type = "ipco"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE
    properties = []

    def read(self, file):
        while file.tell() < self.get_max_offset():
            # boxes derived from ItemProperty, ItemFullProperty,
            # or FreeSpaceBox
            box = read_box(file, self.debug)
            self.properties.append(box)

    def __repr__(self):
        repl = ()
        for box in self.properties:
            repl += (repr(box),)
        return super().repr(repl)


# ISO/IEC 23008-12:2022, Section 6.5.3.2
class ImageSpatialExtents(FullBox):
    box_type = "ispe"

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


# ISO/IEC 14496-12:2022, Section 12.1.5
class ColorInformation(Box):
    box_type = "colr"

    def read(self, file):
        self.colour_type = read_fixed_size_string(file, 4)
        if self.colour_type == "nclx":
            self.colour_primaries = read_uint(file, 2)
            self.transfer_characteristics = read_uint(file, 2)
            self.matrix_coefficients = read_uint(file, 2)
            byte = read_uint(file, 1)
            self.full_range_flag = byte >> 7
            self.reserved = byte % 0x7F
        elif self.colour_type == "rICC":
            offset = file.tell()
            max_offset = self.get_max_offset()
            self.ICC_profile = read_bytes(file, max_offset - offset)
        elif self.colour_type == "prof":
            offset = file.tell()
            max_offset = self.get_max_offset()
            self.ICC_profile = read_bytes(file, max_offset - offset)

    def __repr__(self):
        repl = ()
        repl += (f"colour_type: {self.colour_type}",)
        if self.colour_type == "nclx":
            repl += (f"colour_primaries: {self.colour_primaries}",)
            repl += (f"transfer_characteristics: {self.transfer_characteristics}",)
            repl += (f"matrix_coefficients: {self.matrix_coefficients}",)
            repl += (f"full_range_flag: {self.full_range_flag}",)
            repl += (f"reserved: {self.reserved}",)
        elif self.colour_type == "rICC":
            repl += (f'ICC_profile: "{self.ICC_profile}"',)
        elif self.colour_type == "prof":
            repl += (f'ICC_profile: "{self.ICC_profile}"',)
        return super().repr(repl)


# ISO/IEC 23008-12:2022, Section 6.5.6
class PixelInformationProperty(ItemFullProperty):
    box_type = "pixi"
    channels = []

    def read(self, file):
        num_channels = read_fixed_size_string(file, 1)
        for _ in range(num_channels):
            channel = {}
            channel.bits_per_channel = read_fixed_size_string(file, 1)
            self.channels.append(channel)

    def __repr__(self):
        repl = ()
        for idx, channel in enumerate(self.channels):
            repl += (
                f'channel[{idx}]["bits_per_channel"]: {channel["bits_per_channel"]}',
            )
        return super().repr(repl)


# ISO/IEC 23008-12:2022, Section 6.5.7
class RelativeInformation(ItemFullProperty):
    box_type = "rloc"

    def read(self, file):
        self.horizontal_offset = read_fixed_size_string(file, 4)
        self.vertical_offset = read_fixed_size_string(file, 4)

    def __repr__(self):
        repl = ()
        repl += (f"horizontal_offset: {self.horizontal_offset}",)
        repl += (f"vertical_offset: {self.vertical_offset}",)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.11.14.2
class ItemPropertyAssociationBox(FullBox):
    box_type = "ipma"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE
    entries = []

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
