# -*- coding: utf-8 -*-
from .box import Box


class MediaDataBox(Box):
    box_type = 'mdat'
    is_mandatory = False

    def __init__(self, size):
        super().__init__(size=size)
        self.data_offset = None

    def read(self, file):
        print(file.tell())
        self.data_offset = file.tell()
        file.read(self.get_box_size())
