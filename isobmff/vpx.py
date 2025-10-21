# -*- coding: utf-8 -*-
from .box import FullBox
from .box import Quantity
from .box import read_uint
from .stbl import VisualSampleEntry


# VP9 Codec ISO Media File Format Binding
# https://www.webmproject.org/vp9/mp4/


class VP09SampleEntry(VisualSampleEntry):
    """VP9 Sample Entry"""

    box_type = b"vp09"
    is_mandatory = True
    quantity = Quantity.ONE_OR_MORE

    def read(self, file):
        super().read(file)
        # The VPCodecConfigurationBox is already included in the VisualSampleEntry box_list

    def contents(self):
        tuples = super().contents()
        return tuples


class VPCodecConfigurationBox(FullBox):
    """VP Codec Configuration Box - contains VPCodecConfigurationRecord"""

    box_type = b"vpcC"

    def read(self, file):
        self.vp_config = VPCodecConfigurationRecord(max_offset=self.max_offset)
        self.vp_config.read(file)

    def contents(self):
        tuples = super().contents()
        tuples += (("vp_config", self.vp_config.contents()),)
        return tuples


class VPCodecConfigurationRecord:
    """VP Codec Configuration Record - contains VP9 decoder configuration"""

    # https://www.webmproject.org/vp9/mp4/

    def __init__(self, max_offset):
        self.max_offset = max_offset

    def read(self, file):
        # Read the configuration according to VPCodecConfigurationRecord format
        self.profile = read_uint(file, 1)  # unsigned int(8) profile
        self.level = read_uint(file, 1)  # unsigned int(8) level

        # Read bitDepth (4), chromaSubsampling (3), videoFullRangeFlag (1)
        byte = read_uint(file, 1)
        self.bit_depth = (byte >> 4) & 0x0F  # unsigned int(4) bitDepth
        self.chroma_subsampling = (
            byte >> 1
        ) & 0x07  # unsigned int(3) chromaSubsampling
        self.video_full_range_flag = byte & 0x01  # unsigned int(1) videoFullRangeFlag

        self.colour_primaries = read_uint(file, 1)  # unsigned int(8) colourPrimaries
        self.transfer_characteristics = read_uint(
            file, 1
        )  # unsigned int(8) transferCharacteristics
        self.matrix_coefficients = read_uint(
            file, 1
        )  # unsigned int(8) matrixCoefficients

        self.codec_initialization_data_size = read_uint(
            file, 2
        )  # unsigned int(16) codecIntializationDataSize

        # Read codec initialization data if present
        if self.codec_initialization_data_size > 0:
            self.codec_initialization_data = file.read(
                self.codec_initialization_data_size
            )
        else:
            self.codec_initialization_data = b""

    def contents(self):
        # a non-Box class has no parent
        tuples = ()
        tuples += (("profile", self.profile),)
        tuples += (("level", self.level),)
        tuples += (("bit_depth", self.bit_depth),)
        tuples += (("chroma_subsampling", self.chroma_subsampling),)
        tuples += (("video_full_range_flag", self.video_full_range_flag),)
        tuples += (("colour_primaries", self.colour_primaries),)
        tuples += (("transfer_characteristics", self.transfer_characteristics),)
        tuples += (("matrix_coefficients", self.matrix_coefficients),)
        tuples += (
            ("codec_initialization_data_size", self.codec_initialization_data_size),
        )
        if self.codec_initialization_data_size > 0:
            tuples += (("codec_initialization_data", self.codec_initialization_data),)
        return tuples
