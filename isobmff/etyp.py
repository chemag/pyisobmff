# -*- coding: utf-8 -*-
from .box import Box
from .box import read_fourcc


# ISO/IEC 23008-12:2022, Section 4.4
class ExtendedTypeBox(Box):
    box_type = b"etyp"
    compatible_combinations = []

    def read(self, file):
        while file.tell() < self.get_max_offset():
            # TODO(chema): only tyco allowed here
            self.compatible_combinations = self.read_box_list(file)

    def __repr__(self):
        repl = ()
        for box in self.compatible_combinations:
            repl += (repr(box),)
        return super().repr(repl)


# ISO/IEC 23008-12:2022, Section 4.4
class TypeCombinationBox(Box):
    box_type = b"tyco"
    compatible_brands = []

    def read(self, file):
        while file.tell() < self.get_max_offset():
            box_type = read_fourcc(file)
            self.compatible_brands.append(box_type)

    def __repr__(self):
        repl = ()
        for idx, val in enumerate(self.compatible_brands):
            repl += (f"compatible_brands[{idx}]: {val}",)
        return super().repr(repl)
