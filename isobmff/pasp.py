# -*- coding: utf-8 -*-
from .box import Box
from .utils import read_uint


# ISO/IEC 14496-12:2022, Section 12.1.4.2
class PixelAspectRatio(Box):
    box_type = b"pasp"

    def read(self, file):
        self.hSpacing = read_uint(file, 4)
        self.vSpacing = read_uint(file, 4)

    def contents(self):
        tuples = super().contents()
        tuples += (("hSpacing", self.hSpacing),)
        tuples += (("vSpacing", self.vSpacing),)
        return tuples
