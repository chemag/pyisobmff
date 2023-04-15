# -*- coding: utf-8 -*-
from .box import read_box
from .box import FullBox
from .box import Quantity


class MetaBox(FullBox):
    box_type = "meta"
    is_mandatory = False
    quantity = Quantity.ZERO_OR_ONE
    box_list = []

    def read(self, file):
        while file.tell() < self.get_max_offset():
            box = read_box(file, self.debug)
            self.box_list.append(box)

    def __repr__(self):
        repl = ()
        for box in self.box_list:
            repl += (repr(box),)
        return super().repr(repl)
