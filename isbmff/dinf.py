# -*- coding: utf-8 -*-
from .box import Box
from .dref import Dref


class Dinf(Box):
    """Data Information Box
    """

    def __init__(self, box):
        super().__init__(box.size, box.box_type)
        self.dref = None

    def read(self, file):
        box = Box()
        box.read(file)
        if box.size:
            if box.box_type == 'dref':
                dref = Dref(box)
                dref.read(file)
                self.dref = dref
            else:
                box_size = box.size - 8
                if box_size > 0:
                    file.read(box_size)
