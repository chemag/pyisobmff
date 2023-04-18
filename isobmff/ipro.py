# -*- coding: utf-8 -*-
from .box import FullBox
from .box import Quantity
from .box import read_uint


# ISO/IEC 14496-12:2022, Section 8.11.5.2
class ItemProtectionBox(FullBox):
    box_type = b"ipro"
    is_mandatory = False
    quantity = Quantity.ZERO_OR_ONE
    protection_informations = []

    def read(self, file):
        protection_count = read_uint(file, 2)
        for _ in range(protection_count):
            box = self.read_box(file)
            if box is None:
                break
            if box.box_type == "sinf":
                self.protection_informations.append(box)

    def contents(self):
        tuples = super().contents()
        for idx, box in enumerate(self.protection_informations):
            tuples += ((f"box[{idx}]", box.contents()),)
        return tuples
