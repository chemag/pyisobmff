# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_uint
from .box import read_fixed_size_string


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
    association = []

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
class ItemPropertyContainer(Box):
    box_type = b"ipco"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE
    properties = []

    def read(self, file):
        # boxes derived from ItemProperty, ItemFullProperty,
        # or FreeSpaceBox
        self.properties = self.read_box_list(file)

    def contents(self):
        tuples = super().contents()
        for idx, box in enumerate(self.properties):
            tuples += ((f"property[{idx}]", box.contents()),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.3.2
class ImageSpatialExtents(FullBox):
    box_type = b"ispe"

    def read(self, file):
        self.width = read_uint(file, 4)
        self.height = read_uint(file, 4)

    def contents(self):
        tuples = super().contents()
        tuples += (("width", self.width),)
        tuples += (("height", self.height),)
        return tuples


# ISO/IEC 14496-12:2022, Section 12.1.4.2
class PixelAspectRatio(Box):
    box_type = b"pasp"

    def read(self, file):
        self.hSpacing = read_uint(file, 4)
        self.vSpacing = read_uint(file, 4)

    def contents(self):
        tuples = super().contents()
        tuples += (("hSpacing", self.hSpacing),)
        tuples += (("vSpacing", self.vSpacing),)
        return tuples


# ISO/IEC 14496-12:2022, Section 12.1.5
class ColorInformation(Box):
    box_type = b"colr"

    def read(self, file):
        self.colour_type = read_fixed_size_string(file, 4)
        if self.colour_type == "nclx":
            self.colour_primaries = read_uint(file, 2)
            self.transfer_characteristics = read_uint(file, 2)
            self.matrix_coefficients = read_uint(file, 2)
            byte = read_uint(file, 1)
            self.full_range_flag = byte >> 7
            self.reserved = byte % 0x7F
        elif self.colour_type == "nclc":
            # original apple quicktime spec
            # https://developer.apple.com/library/archive/technotes/tn2162/_index.html#//apple_ref/doc/uid/DTS40013070-CH1-TNTAG10
            self.colour_primaries = read_uint(file, 2)
            self.transfer_characteristics = read_uint(file, 2)
            self.matrix_coefficients = read_uint(file, 2)
        elif self.colour_type == "rICC":
            self.ICC_profile = self.read_as_bytes(file)
        elif self.colour_type == "prof":
            self.ICC_profile = self.read_as_bytes(file)

    def contents(self):
        tuples = super().contents()
        tuples += (("colour_type", self.colour_type),)
        if self.colour_type == "nclx":
            tuples += (("colour_primaries", self.colour_primaries),)
            tuples += (("transfer_characteristics", self.transfer_characteristics),)
            tuples += (("matrix_coefficients", self.matrix_coefficients),)
            tuples += (("full_range_flag", self.full_range_flag),)
            tuples += (("reserved", self.reserved),)
        elif self.colour_type == "nclc":
            tuples += (("colour_primaries", self.colour_primaries),)
            tuples += (("transfer_characteristics", self.transfer_characteristics),)
            tuples += (("matrix_coefficients", self.matrix_coefficients),)
        elif self.colour_type == "rICC":
            tuples += (("ICC_profile", f"{self.ICC_profile}"),)
        elif self.colour_type == "prof":
            tuples += (("ICC_profile", f"{self.ICC_profile}"),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.6
class PixelInformationProperty(ItemFullProperty):
    box_type = b"pixi"
    channels = []

    def read(self, file):
        num_channels = read_uint(file, 1)
        for _ in range(num_channels):
            channel = {}
            channel["bits_per_channel"] = read_uint(file, 1)
            self.channels.append(channel)

    def contents(self):
        tuples = super().contents()
        for idx, channel in enumerate(self.channels):
            tuples += (
                (f'channel[{idx}]["bits_per_channel"]', channel["bits_per_channel"]),
            )
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.7
class RelativeInformation(ItemFullProperty):
    box_type = b"rloc"

    def read(self, file):
        self.horizontal_offset = read_uint(file, 4)
        self.vertical_offset = read_uint(file, 4)

    def contents(self):
        tuples = super().contents()
        tuples += (("horizontal_offset", self.horizontal_offset),)
        tuples += (("vertical_offset", self.vertical_offset),)
        return tuples


# ISO/IEC 14496-12:2022, Section 8.11.14.2
class ItemPropertyAssociationBox(FullBox):
    box_type = b"ipma"
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

    def contents(self):
        tuples = super().contents()
        for idx, entry in enumerate(self.entries):
            tuples += ((f'entry[{idx}]["item_id"]', entry["item_id"]),)
            for jdx, association in enumerate(entry["associations"]):
                tuples += (
                    (
                        f'entry[{idx}]["associations"][{jdx}]["item"]',
                        association["item"],
                    ),
                )
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
