# -*- coding: utf-8 -*-
from .box import Box
from .box import Quantity
from .box import indent
from .box import read_int
from .box import read_string


class FileTypeBox(Box):
    box_type = "ftyp"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.major_brand = None
        self.minor_version = None
        self.compatible_brands = []

    def __repr__(self):
        rep = "major_brand: " + str(self.major_brand) + "\n"
        rep += "minor_version: " + str(self.minor_version) + "\n"
        rep += "compatible_brands: "
        for brand in self.compatible_brands:
            rep += brand + ","
        return super().__repr__() + indent(rep)

    def read(self, file):
        self.major_brand = read_string(file, 4)
        self.minor_version = read_int(file, 4)
        num_compatible_brands = int((self.size - 16) / 4)
        for _ in range(num_compatible_brands):
            compat_brand = read_string(file, 4)
            self.compatible_brands.append(compat_brand)
