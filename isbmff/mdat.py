# -*- coding: utf-8 -*-
from .box import Box


class MediaDataBox(Box):
    """MediaDataBox
    """

    def __init__(self, box):
        super().__init__(size=box.size, box_type=box.box_type)
        self.data_size = self.size - 8
        self.data = None

    def read(self, file):
        self.data = file.read(self.data_size)

    def write(self):
        pass