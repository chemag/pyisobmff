# -*- coding: utf-8 -*-
from .box import Box
from .box import Quantity
from .box import read_uint
from .box import read_fixed_size_string


# ISO/IEC 23008-12:2022, Section 4.3.2
class FileTypeBox(Box):
    box_type = "ftyp"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE
    compatible_brands = []

    def read(self, file):
        self.major_brand = read_fixed_size_string(file, 4)
        self.minor_version = read_uint(file, 4)
        num_compatible_brands = int((self.size - 16) / 4)
        for _ in range(num_compatible_brands):
            compat_brand = read_fixed_size_string(file, 4)
            self.compatible_brands.append(compat_brand)

    def __repr__(self):
        repl = ()
        repl += (f"major_brand: {self.major_brand}",)
        repl += (f"minor_version: {self.minor_version}",)
        repl += (f"compatible_brands: \"{','.join(self.compatible_brands)}\"",)
        return super().repr(repl)


# ISO/IEC 23008-12:2022, Section 8.16.2
class SegmentTypeBox(FileTypeBox):
    box_type = "styp"
