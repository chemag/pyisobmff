# -*- coding: utf-8 -*-
from .box import FullBox
from .box import indent
from .box import read_int


class MovieHeaderBox(FullBox):
    """Movie Box
    """
    box_type = 'mvhd'
    is_mandatory = True

    def __init__(self, size):
        super().__init__(size=size)

    def __repr__(self):
        return  super().__repr__()

    def read(self, file):
        super().read(file)
        print(file.read(self.get_box_size()))
