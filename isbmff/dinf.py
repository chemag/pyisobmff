# -*- coding: utf-8 -*-
from .box import Box
from .dref import Dref


class Dinf(Box):
    """Data Information Box
    """

    def __init__(self, file, size):
        super().__init__()
        self.size = size
        self.box_type = 'dinf'
        self.dref = None
        size = int.from_bytes(file.read(4), 'big')
        if size:
            self.__read_box(file, size)

    def __read_box(self, file, size):
        box_type = file.read(4).decode()
        box_size = size - 8

        if box_type == 'dref':
            self.dref = Dref(file, size)
        else:
            if box_size > 0:
                file.read(box_size)

        return box_size