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

    def __repr__(self):
        repl = ()
        repl += (f"all_ref_pics_intra: {self.all_ref_pics_intra}",)
        repl += (f"intra_pred_used: {self.intra_pred_used}",)
        repl += (f"max_ref_per_pic: {self.max_ref_per_pic}",)
        repl += (f"reserved: {self.reserved}",)
        return super().repr(repl)
