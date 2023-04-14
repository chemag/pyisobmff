# -*- coding: utf-8 -*-
from .box import FullBox
from .box import Quantity
from .box import read_box
from .box import read_uint


# ISO/IEC 14496-12:2022, Section 8.11.5.2
class ItemProtectionBox(FullBox):
    box_type = "ipro"
    is_mandatory = False
    quantity = Quantity.ZERO_OR_ONE
    protection_informations = []

    def read(self, file):
        protection_count = read_uint(file, 2)
        for _ in range(protection_count):
            box = read_box(file)
            if not box:
                break
            if box.box_type == "sinf":
                self.protection_informations.append(box)

    def __repr__(self):
        repl = ()
        for box in self.protection_informations:
            repl += (repr(box),)
        return super().repr(repl)
