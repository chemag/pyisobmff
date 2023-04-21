# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_uint
from .box import read_sint
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


# ISO/IEC 23008-12:2022, Section 6.5.20
class UserDescriptionProperty(ItemFullProperty):
    box_type = b"udes"

    def read(self, file):
        max_len = self.get_max_offset() - file.tell()
        self.lang = read_utf8string(file, max_len)
        max_len = self.get_max_offset() - file.tell()
        self.name = read_utf8string(file, max_len)
        max_len = self.get_max_offset() - file.tell()
        self.description = read_utf8string(file, max_len)
        max_len = self.get_max_offset() - file.tell()
        self.tags = read_utf8string(file, max_len)

    def contents(self):
        tuples = super().contents()
        tuples += (("lang", self.lang),)
        tuples += (("name", self.name),)
        tuples += (("description", self.description),)
        tuples += (("tags", self.tags),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.21
class AccessibilityTextProperty(ItemFullProperty):
    box_type = b"altt"

    def read(self, file):
        max_len = self.get_max_offset() - file.tell()
        self.alt_text = read_utf8string(file, max_len)
        max_len = self.get_max_offset() - file.tell()
        self.alt_lang = read_utf8string(file, max_len)

    def contents(self):
        tuples = super().contents()
        tuples += (("alt_text", self.alt_text),)
        tuples += (("alt_lang", self.alt_lang),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.22
class AutoExposureProperty(ItemFullProperty):
    box_type = b"aebr"

    def read(self, file):
        self.exposure_step = read_uint(file, 1)
        self.exposure_numerator = read_uint(file, 1)

    def contents(self):
        tuples = super().contents()
        tuples += (("exposure_step", self.exposure_step),)
        tuples += (("exposure_numerator", self.exposure_numerator),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.23
class WhiteBalanceProperty(ItemFullProperty):
    box_type = b"wbbr"

    def read(self, file):
        self.blue_amber = read_uint(file, 2)
        self.green_magenta = read_sint(file, 1)

    def contents(self):
        tuples = super().contents()
        tuples += (("blue_amber", self.blue_amber),)
        tuples += (("green_magenta", self.green_magenta),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.24
class FocusProperty(ItemFullProperty):
    box_type = b"fobr"

    def read(self, file):
        self.focus_distance_numerator = read_uint(file, 2)
        self.focus_distance_denominator = read_uint(file, 2)

    def contents(self):
        tuples = super().contents()
        tuples += (("focus_distance_numerator", self.focus_distance_numerator),)
        tuples += (("focus_distance_denominator", self.focus_distance_denominator),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.25
class FlashExposureProperty(ItemFullProperty):
    box_type = b"afbr"

    def read(self, file):
        self.flash_exposure_numerator = read_uint(file, 1)
        self.flash_exposure_denominator = read_uint(file, 1)

    def contents(self):
        tuples = super().contents()
        tuples += (("flash_exposure_numerator", self.flash_exposure_numerator),)
        tuples += (("flash_exposure_denominator", self.flash_exposure_denominator),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.26
class DepthOfFieldProperty(ItemFullProperty):
    box_type = b"dobr"

    def read(self, file):
        self.f_stop_numerator = read_uint(file, 1)
        self.f_stop_denominator = read_uint(file, 1)

    def contents(self):
        tuples = super().contents()
        tuples += (("f_stop_numerator", self.f_stop_numerator),)
        tuples += (("f_stop_denominator", self.f_stop_denominator),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.27
class PanoramaProperty(ItemFullProperty):
    box_type = b"pano"

    def read(self, file):
        self.panorama_direction = read_uint(file, 1)
        if self.panorama_direction >= 4 and self.panorama_direction <= 5:
            self.rows_minus_one = read_uint(file, 1)
            self.columns_minus_one = read_uint(file, 1)

    def contents(self):
        tuples = super().contents()
        tuples += (("panorama_direction", self.panorama_direction),)
        if self.panorama_direction >= 4 and self.panorama_direction <= 5:
            tuples += (("rows_minus_one", self.rows_minus_one),)
            tuples += (("columns_minus_one", self.columns_minus_one),)
        return tuples
