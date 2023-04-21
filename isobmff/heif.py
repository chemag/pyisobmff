# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_uint
from .box import read_fixed_size_string
from .box import read_utf8string
from .iprp import ItemFullProperty
from .iprp import ItemProperty


# ISO/IEC 23008-12:2022, Section 6.5.3
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


# ISO/IEC 23008-12:2022, Section 6.5.6
class PixelInformationProperty(ItemFullProperty):
    box_type = b"pixi"

    def read(self, file):
        num_channels = read_uint(file, 1)
        self.channels = []
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


# ISO/IEC 23008-12:2022, Section 6.5.8
class AuxiliaryTypeProperty(ItemFullProperty):
    box_type = b"auxC"

    def read(self, file):
        max_len = self.get_max_offset() - file.tell()
        self.aux_type = read_utf8string(file, max_len)
        self.aux_subtype = []
        while file.tell() < self.get_max_offset():
            self.aux_subtype.append(read_uint(file, 1))

    def contents(self):
        tuples = super().contents()
        tuples += (("aux_type", self.aux_type),)
        for idx, val in enumerate(self.aux_subtype):
            tuples += ((f"aux_subtype[{idx}]", val),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.10
class ImageRotation(ItemProperty):
    box_type = b"rloc"

    def read(self, file):
        self.reserved = read_uint(file, 6)
        self.angle = read_uint(file, 2)

    def contents(self):
        tuples = super().contents()
        tuples += (("reserved", self.reserved),)
        tuples += (("angle", self.angle),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.11
class LayerSelectorProperty(ItemProperty):
    box_type = b"lsel"

    def read(self, file):
        self.layer_id = read_uint(file, 2)

    def contents(self):
        tuples = super().contents()
        tuples += (("layer_id", self.layer_id),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.12
class ImageMirror(ItemProperty):
    box_type = b"imir"

    def read(self, file):
        self.reserved = read_uint(file, 7)
        self.axis = read_uint(file, 1)

    def contents(self):
        tuples = super().contents()
        tuples += (("reserved", self.reserved),)
        tuples += (("axis", self.axis),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.13
class ImageScaling(ItemFullProperty):
    box_type = b"iscl"

    def read(self, file):
        self.target_width_numerator = read_uint(file, 2)
        self.target_width_denominator = read_uint(file, 2)
        self.target_height_numerator = read_uint(file, 2)
        self.target_height_denominator = read_uint(file, 2)

    def contents(self):
        tuples = super().contents()
        tuples += (("target_width_numerator", self.target_width_numerator),)
        tuples += (("target_width_denominator", self.target_width_denominator),)
        tuples += (("target_height_numerator", self.target_height_numerator),)
        tuples += (("target_height_denominator", self.target_height_denominator),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.17
class RequiredReferenceTypesProperty(ItemFullProperty):
    box_type = b"rref"

    def read(self, file):
        reference_type_count = read_uint(file, 1)
        self.reference_type = []
        for _ in range(reference_type_count):
            self.reference_type.append(read_uint(file, 4))

    def contents(self):
        tuples = super().contents()
        for idx, val in enumerate(self.reference_type):
            tuples += ((f"reference_type[{idx}]", val),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.18
class CreationTimeProperty(ItemFullProperty):
    box_type = b"crtt"

    def read(self, file):
        self.creation_time = read_uint(file, 8)

    def contents(self):
        tuples = super().contents()
        tuples += (("creation_time", self.creation_time),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.19
class ModificationTimeProperty(ItemFullProperty):
    box_type = b"mdft"

    def read(self, file):
        self.modification_time = read_uint(file, 8)

    def contents(self):
        tuples = super().contents()
        tuples += (("modification_time", self.modification_time),)
        return tuples
