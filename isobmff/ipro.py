# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_int
from .box import read_string


class Ipro(FullBox):
    """
    """
    box_type = 'ipro'
    is_mandatory = False

    def __init__(self, size):
        super().__init__(size=size)

    def __repr__(self):
        rep = super().__repr__()
        return rep

    def read(self, file):
        super().read(file)
        pass