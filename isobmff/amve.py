# -*- coding: utf-8 -*-
from .box import Box
from .utils import read_uint


# ISO/IEC 14496-12:2026
class AmbientViewingEnvironment(Box):
    box_type = b"amve"

    def read(self, file):
        # in units of 0.0001 lux
        self.ambient_illuminance = read_uint(file, 4)
        # normalized x/y chromaticity, in units of 0.00002
        self.ambient_light_x = read_uint(file, 2)
        self.ambient_light_y = read_uint(file, 2)

    def contents(self):
        tuples = super().contents()
        tuples += (("ambient_illuminance", self.ambient_illuminance),)
        tuples += (("ambient_light_x", self.ambient_light_x),)
        tuples += (("ambient_light_y", self.ambient_light_y),)
        return tuples
