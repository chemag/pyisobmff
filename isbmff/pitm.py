# -*- coding: utf-8 -*-
from .box import FullBox
from .box import indent
from .box import read_int


class PrimaryItemBox(FullBox):
    """Primary Item Box
    """

    def __init__(self, box):
        super().__init__(box, box.version, box.flags)
        self.item_id = None

    def __repr__(self):
        rep = 'item_id: ' + str(self.item_id)
        return  super().__repr__() + indent(rep)

    def read(self, file):
        self.item_id = read_int(file, 2)
