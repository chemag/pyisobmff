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
        file.read(self.get_payload_size())
