# -*- coding: utf-8 -*-
from .box import Box


class Mdat(Box):
    """mdat
    """

    def __init__(self, file, size):
        super().__init__()
        self.size = size
        self.box_type = 'mdat'
        self.data_size = size - 8
        self.data = file.read(self.data_size)
