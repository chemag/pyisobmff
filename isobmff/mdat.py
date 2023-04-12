# -*- coding: utf-8 -*-
from .box import Box, indent


class MediaDataBox(Box):
    box_type = "mdat"
    is_mandatory = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_offset = None

    def __repr__(self):
        rep = f"data_offset: 0x{self.data_offset:08x}"
        return super().__repr__() + indent(rep)

    def read(self, file):
        # store the offset
        self.data_offset = file.tell()
        file.read(self.get_box_size())
