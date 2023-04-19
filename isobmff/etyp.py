# -*- coding: utf-8 -*-
from .box import Box
from .box import read_fourcc


# ISO/IEC 23008-12:2022, Section 4.4
class ExtendedTypeBox(Box):
    box_type = b"etyp"

    def read(self, file):
        self.compatible_combinations = []
        while file.tell() < self.get_max_offset():
            # TODO(chema): only tyco allowed here
            self.compatible_combinations = self.read_box_list(file)

    def contents(self):
        tuples = super().contents()
        for idx, box in enumerate(self.compatible_combinations):
            tuples += ((f"compatible_combination[{idx}]", box.contents()),)
        return tuples


# ISO/IEC 23008-12:2022, Section 4.4
class TypeCombinationBox(Box):
    box_type = b"tyco"

    def read(self, file):
        self.compatible_brands = []
        while file.tell() < self.get_max_offset():
            box_type = read_fourcc(file)
            self.compatible_brands.append(box_type)

    def contents(self):
        tuples = super().contents()
        for idx, val in enumerate(self.compatible_brands):
            tuples += ((f"compatible_brands[{idx}]", val),)
        return tuples
