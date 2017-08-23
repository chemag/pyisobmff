# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_int
from .box import read_string


class ProtectionSchemeInfoBox(Box):
    box_type = 'sinf'
    is_mandatory = False
    quantity = Quantity.ONE_OR_MORE

class OriginalFormatBox(Box):
    box_type = 'frma'
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE

    def __init__(self, size):
        super().__init__(size=size)
        self.data_format = None
    
    def read(self, file):
        self.data_format = read_int(file, 4)

class SchemeTypeBox(FullBox):
    box_type = 'schm'
    is_mandatory = False
    quantity = Quantity.ZERO_OR_ONE

    def __init__(self, size):
        super().__init__(size=size)
        self.scheme_type = None
        self.scheme_version = None
        self.scheme_uri = None

    def read(self, file):
        self.scheme_type = read_int(file, 4)
        self.scheme_version = read_int(file, 4)
        if self.flags & 0b1:
            self.scheme_uri = read_string(file)

class SchemeInformationBox(Box):
    box_type = 'schi'
    is_mandatory = False
    quantity = Quantity.ZERO_OR_ONE
