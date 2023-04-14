# -*- coding: utf-8 -*-
from .box import Box


class MediaDataBox(Box):
    box_type = "mdat"
    is_mandatory = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_offset = None

    def read(self, file):
        # store the offset
        self.data_offset = file.tell()
        offset = file.tell()
        max_offset = self.get_max_offset()
        file.read(max_offset - offset)
