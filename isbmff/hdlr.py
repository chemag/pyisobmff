# -*- coding: utf-8 -*-
from .box import Box


class Hdlr(Box):
    """Handler Reference Box
    """

    def __init__(self, file, size):
        super().__init__()
        self.size = size
        self.box_type = 'hdlr'
        self.pre_defined = int.from_bytes(file.read(4), 'big')
        self.handler_type = int.from_bytes(file.read(4), 'big')
        self.reserved = []
        for _ in range(3):
            self.reserved.append(int.from_bytes(file.read(4), 'big'))


    def __repr__(self):
        rep = super().__repr__()
        return rep
