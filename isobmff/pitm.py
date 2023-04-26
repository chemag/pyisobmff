# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_uint


# ISO/IEC 14496-12:2022, Section 8.11.4
class PrimaryItemBox(FullBox):
    box_type = b"pitm"
    is_mandatory = False

    def read(self, file):
        self.item_id = read_uint(file, 2 if self.version == 0 else 4)

    def contents(self):
        tuples = super().contents()
        tuples += ((f"item_id", self.item_id),)
        return tuples
