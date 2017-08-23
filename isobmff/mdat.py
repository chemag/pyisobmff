# -*- coding: utf-8 -*-
from .box import Box


class MediaDataBox(Box):
    box_type = 'mdat'
    is_mandatory = False

    def __init__(self, size):
        super().__init__(size=size)
        self.data = None

    def read(self, file):
        self.data = file.read(self.get_box_size())
        print(self.data[0:20])
