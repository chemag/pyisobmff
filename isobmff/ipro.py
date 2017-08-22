# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_int
from .box import read_string


class Ipro(FullBox):
    """
    """
    is_mandatory = False

    def __init__(self, box):
        super().__init__(box=box, version=box.version, flags=box.flags)

    def __repr__(self):
        rep = super().__repr__()
        return rep

    def read(self, file):
        pass