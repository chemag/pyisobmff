# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .dref import DataEntryUrlBox
from .dref import DataEntryUrnBox
from .dref import DataReferenceBox


class DataInformationBox(FullBox):
    """Data Information Box
    """
    box_type = 'dinf'
    is_mandatry = True

    def __init__(self, size):
        super().__init__(size=size)
        self.dref = None
        self.url = None
        self.urn = None

    def __repr__(self):
        rep = super().__repr__()
        rep += self.dref.__repr__()
        return rep

    def read(self, file):
        super().read(file)
        box = Box()
        box.read(file)
        if box.size:
            if box.box_type == 'dref':
                dref = DataReferenceBox(box.size)
                dref.read(file)
                self.dref = dref
            if box.box_type == 'url ':
                url = DataEntryUrlBox(box.size)
                url.read(file)
                self.url = dref
            if box.box_type == 'urn ':
                urn = DataEntryUrnBox(box.size)
                urn.read(file)
                self.urn = urn
            else:
                box_size = box.size - 8
                if box_size > 0:
                    file.read(box_size)
