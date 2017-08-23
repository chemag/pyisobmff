# -*- coding: utf-8 -*-
from .box import Box


class MediaDataBox(Box):
    """Media Data Box
    """
    box_type = 'mdat'
    is_mandatory = False

    def __init__(self, size):
        super().__init__(size=size)
        self.data = None

    def read(self, file):
        self.data = file.read(self.get_box_size())

    def write(self):
        pass