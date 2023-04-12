# -*- coding: utf-8 -*-
from .box import read_box, indent
from .box import FullBox
from .box import Quantity


class MetaBox(FullBox):
    box_type = "meta"
    is_mandatory = False
    quantity = Quantity.ZERO_OR_ONE
    box_list = []

    def __repr__(self):
        rep = ""
        for box in self.box_list:
            rep += repr(box) + "\n"
        return super().__repr__() + indent(rep)

    def read(self, file):
        box = read_box(file)
        self.box_list.append(box)
