# -*- coding: utf-8 -*-
from .box import FullBox
from .box import Quantity
from .box import indent
from .box import read_int
from .box import read_string


class HandlerReferenceBox(FullBox):
    box_type = "hdlr"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE

    def __init__(self, size, version, flags):
        super().__init__(size=size, version=version, flags=flags)
        self.pre_defined = None
        self.handler_type = None
        self.reserved = []
        self.name = None

    def __repr__(self):
        rep = "handler_type: " + self.handler_type + "\n"
        rep += "name: " + self.name
        return super().__repr__() + indent(rep)

    def read(self, file):
        self.pre_defined = read_int(file, 4)
        self.handler_type = read_string(file, 4)
        for _ in range(3):  # 3*4=12bytes
            self.reserved.append(read_int(file, 4))
        self.name = read_string(file)
