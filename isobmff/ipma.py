# -*- coding: utf-8 -*-
from .box import Box
from .box import indent
from .box import read_int


class ipma(Box):
    """SpaialExtentBox
    """
    box_type = 'ipma'

    def __init__(self, size):
        super().__init__(size=size)

    def __repr__(self):
        return  super().__repr__()

    def read(self, file):
        print(file.read(self.get_box_size()))
