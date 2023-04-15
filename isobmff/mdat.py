# -*- coding: utf-8 -*-
from .box import Box


class MediaDataBox(Box):
    box_type = b"mdat"
    is_mandatory = False

    def read(self, file):
        max_offset = self.get_max_offset()
        file.seek(max_offset)
