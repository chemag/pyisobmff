# -*- coding: utf-8 -*-
from .box import FullBox
from .box import indent
from .box import read_int


class PrimaryItemBox(FullBox):
    box_type = 'pitm'
    is_mandatory = False

    def read(self, file):
        self.item_id = read_int(file, 2)
