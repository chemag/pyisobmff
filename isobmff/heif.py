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
from .sgpd import VisualSampleGroupEntry


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


# ISO/IEC 23008-12:2022, Section 6.5.29
class TargetOlsProperty(ItemFullProperty):
    box_type = b"tols"

    def read(self, file):
        self.target_ols_idx = read_uint(file, 2)

    def contents(self):
        tuples = super().contents()
        tuples += (("target_ols_idx", self.target_ols_idx),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.30
class WipeTransitionEffectProperty(ItemFullProperty):
    box_type = b"wipe"

    def read(self, file):
        self.transition_direction = read_uint(file, 1)

    def contents(self):
        tuples = super().contents()
        tuples += (("transition_direction", self.transition_direction),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.31
class ZoomTransitionEffectProperty(ItemFullProperty):
    box_type = b"zoom"

    def read(self, file):
        byte0 = read_uint(file, 1)
        self.transition_direction = byte0 >> 7
        self.transition_shape = byte0 & 0x7F

    def contents(self):
        tuples = super().contents()
        tuples += (("transition_direction", self.transition_direction),)
        tuples += (("transition_shape", self.transition_shape),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.32
class FadeTransitionEffectProperty(ItemFullProperty):
    box_type = b"fade"

    def read(self, file):
        self.transition_direction = read_uint(file, 1)

    def contents(self):
        tuples = super().contents()
        tuples += (("transition_direction", self.transition_direction),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.33
class SplitTransitionEffectProperty(ItemFullProperty):
    box_type = b"splt"

    def read(self, file):
        self.transition_direction = read_uint(file, 1)

    def contents(self):
        tuples = super().contents()
        tuples += (("transition_direction", self.transition_direction),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.34
class SuggestedTransitionPeriodProperty(ItemFullProperty):
    box_type = b"stpe"

    def read(self, file):
        self.transition_period = read_uint(file, 1)

    def contents(self):
        tuples = super().contents()
        tuples += (("transition_period", self.transition_period),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.35
class SuggestedTimeDisplayDurationProperty(ItemFullProperty):
    box_type = b"ssld"

    def read(self, file):
        self.duration = read_uint(file, 2)

    def contents(self):
        tuples = super().contents()
        tuples += (("duration", self.duration),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.8.1.2
class VisualEquivalenceEntry(VisualSampleGroupEntry):
    box_type = b"eqiv"

    def read(self, file):
        super().read(file)
        self.time_offset = read_sint(file, 2)
        self.timescale_multiplier = read_uint(file, 2)

    def contents(self):
        tuples = super().contents()
        tuples += (("time_offset", self.time_offset),)
        tuples += (("timescale_multiplier", self.timescale_multiplier),)
        return tuples


## ISO/IEC 23008-12:2022, Section 6.8.6.2
# class AutoExposureBracketingEntry(VisualSampleGroupEntry):
#    box_type = b"aebr"
#
#    def read(self, file):
#        super().read(file)
#        self.exposure_step = read_uint(file, 1)
#        self.exposure_numerator = read_uint(file, 1)
#
#    def contents(self):
#        tuples = super().contents()
#        tuples += (("exposure_step", self.exposure_step),)
#        tuples += (("exposure_numerator", self.exposure_numerator),)
#        return tuples

## ISO/IEC 23008-12:2022, Section 6.8.6.3
# class WhiteBalanceBracketingEntry(VisualSampleGroupEntry):
#    box_type = b"wbbr"


## ISO/IEC 23008-12:2022, Section 6.8.6.4
# class FocusBracketingEntry(VisualSampleGroupEntry):
#    box_type = b"fobr"


## ISO/IEC 23008-12:2022, Section 6.8.6.5
# class FlashExposureBracketingEntry(VisualSampleGroupEntry):
#    box_type = b"afbr"


## ISO/IEC 23008-12:2022, Section 6.8.6.6
# class DepthOfFieldBracketingEntry(VisualSampleGroupEntry):
#    box_type = b"dobr"


## ISO/IEC 23008-12:2022, Section 6.8.8.2
# class PanoramaEntry(VisualSampleGroupEntry):
#    box_type = b"pano"


# ISO/IEC 23008-12:2022, Section 6.10.2.2
class MaskConfigurationProperty(ItemFullProperty):
    box_type = b"mskC"

    def read(self, file):
        self.bits_per_pixel = read_uint(file, 8)

    def contents(self):
        tuples = super().contents()
        tuples += (("bits_per_pixel", self.bits_per_pixel),)
        return tuples


# ISO/IEC 23008-12:2022, Section 7.2.3.2
class ccst(FullBox):
    box_type = b"ccst"
    is_mandatory = False

    def read(self, file):
        word = read_uint(file, 4)
        self.all_ref_pics_intra = (word >> 31) & 0x1
        self.intra_pred_used = (word >> 30) & 0x1
        self.max_ref_per_pic = (word >> 26) & 0xF
        self.reserved = (word >> 0) & 0x03FFFFFF

    def contents(self):
        tuples = super().contents()
        tuples += (("all_ref_pics_intra", self.all_ref_pics_intra),)
        tuples += (("intra_pred_used", self.intra_pred_used),)
        tuples += (("max_ref_per_pic", self.max_ref_per_pic),)
        tuples += (("reserved", self.reserved),)
        return tuples
