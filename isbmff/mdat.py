# -*- coding: utf-8 -*-
from .box import Box


class Mdat(Box):
    """mdat
    """

    def __init__(self, box):
        super().__init__(box.size, box.box_type)
        self.data_size = self.size - 8
        self.data = None

    def read(self, file):
        self.data = file.read(self.data_size)

    def write(self):
        pass