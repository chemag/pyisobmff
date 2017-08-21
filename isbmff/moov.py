# -*- coding: utf-8 -*-
from .box import Box
from .box import indent
from .box import read_int


class MovieBox(Box):
    """Movie Box
    """

    def __init__(self, box):
        super().__init__(size=box.size, box_type=box.box_type)

    def __repr__(self):
        return  super().__repr__()

    def read(self, file):
        print(file.read(self.get_box_size()))
