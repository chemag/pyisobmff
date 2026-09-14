# -*- coding: utf-8 -*-
from .box import Box
from .utils import read_uint
from .utils import read_fixed_size_string


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
