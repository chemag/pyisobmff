# -*- coding: utf-8 -*-
from .box import Box


class MediaDataBox(Box):
    box_type = b"mdat"
    is_mandatory = False

    def read(self, file):
        # skip the remaining data
        # TODO: this should be centralized
        file.seek(self.max_offset)
