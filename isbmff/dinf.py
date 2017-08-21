# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .dref import DataEntryUrlBox
from .dref import DataEntryUrnBox
from .dref import DataReferenceBox


class DataInformationBox(FullBox):
    """Data Information Box
    """

    def __init__(self, box):
        super().__init__(box, box.version, box.flags)
        self.dref = None
        self.url = None
        self.urn = None

    def __repr__(self):
        rep = super().__repr__()
        rep += self.dref.__repr__()
        return rep

    def read(self, file):
        box = Box()
        box.read(file)
        if box.size:
            full_box = FullBox(box)
            full_box.read(file)
            
            if box.box_type == 'dref':
                dref = DataReferenceBox(full_box)
                dref.read(file)
                self.dref = dref
            if box.box_type == 'url ':
                url = DataEntryUrlBox(full_box)
                url.read(file)
                self.url = dref
            if box.box_type == 'urn ':
                urn = DataEntryUrnBox(full_box)
                urn.read(file)
                self.urn = urn
            else:
                box_size = box.size - 8
                if box_size > 0:
                    file.read(box_size)
