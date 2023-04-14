# -*- coding: utf-8 -*-
from .box import Box
from .box import read_box
from .box import read_fixed_size_string


# ISO/IEC 23008-12:2022, Section 4.4
class ExtendedTypeBox(Box):
    box_type = "etyp"
    compatible_combinations = []

    def read(self, file):
        while file.tell() < self.get_max_offset():
            box = read_box(file)
            # TODO(chema): only tyco allowed here
            self.compatible_combinations.append(box)

    def __repr__(self):
        repl = ()
        for box in self.compatible_combinations:
            repl += (repr(box),)
        return super().repr(repl)


# ISO/IEC 23008-12:2022, Section 4.4
class TypeCombinationBox(Box):
    box_type = "tyco"
    compatible_brands = []

    def read(self, file):
        while file.tell() < self.get_max_offset():
            box_type = read_fixed_size_string(file, 4)
            self.compatible_brands.append(box_type)

    def __repr__(self):
        repl = ()
        for idx, val in enumerate(self.compatible_brands):
            repl += (f"compatible_brands[{idx}]: {val}",)
        return super().repr(repl)
