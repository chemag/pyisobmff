# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_uint

# ISO/IEC 23008-12:2022, Section 7.2.3.2
class ccst(FullBox):
    box_type = b"ccst"
    is_mandatory = False

    def read(self, file):
        word = read_uint(file, 4)
        self.all_ref_pics_intra = (word >> 31) & 0x1
        self.intra_pred_used = (word >> 30) & 0x1
        self.max_ref_per_pic = (word >> 26) & 0xF
        self.reserved = (word >> 0) & 0x03FFFFFF

    def contents(self):
        tuples = super().contents()
        tuples += (("all_ref_pics_intra", self.all_ref_pics_intra),)
        tuples += (("intra_pred_used", self.intra_pred_used),)
        tuples += (("max_ref_per_pic", self.max_ref_per_pic),)
        tuples += (("reserved", self.reserved),)
        return tuples
