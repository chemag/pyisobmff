# -*- coding: utf-8 -*-
from .box import read_box
from .box import FullBox
from .box import Quantity


class MetaBox(FullBox):
    box_type = "meta"
    is_mandatory = False
    quantity = Quantity.ZERO_OR_ONE
    box_list = []

    def __repr__(self):
        repl = ()
        for box in self.box_list:
            repl += (repr(box),)
        return super().repr(repl)

    def read(self, file):
        box = read_box(file)
        self.box_list.append(box)
