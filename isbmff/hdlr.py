# -*- coding: utf-8 -*-
from .box import Box


class Hdlr(Box):
    """Handler Reference Box
    """

    def __init__(self, box):
        super().__init__(box.size, box.box_type)
        self.pre_defined = None
        self.handler_type = None
        self.reserved = []

    def __repr__(self):
        rep = super().__repr__()
        return rep

    def read(self, file):
        self.pre_defined = int.from_bytes(file.read(4), 'big')
        self.handler_type = int.from_bytes(file.read(4), 'big')
        for _ in range(3):
            self.reserved.append(int.from_bytes(file.read(4), 'big'))

