# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_int
from .box import read_string


class DataEntryUrlBox(FullBox):
    """Data Entry Url Box
    """
    box_type = 'url '
    is_mandatry = True

    def __init__(self, size):
        super().__init__(size=size)
        self.location = None

    def read(self, file):
        super().read(file)
        #url_size = self.size - 8
        self.location = read_string(file)


class DataEntryUrnBox(FullBox):
    """Data Entry Urn Box
    """
    box_type = 'urn '
    is_mandatry = True

    def __init__(self, size):
        super().__init__(size=size)
        self.location = None

    def read(self, file):
        super().read(file)
        #url_size = self.size - 8
        self.location = read_string(file)


class DataReferenceBox(FullBox):
    """Data Reference Box
    """
    box_type = 'dref'
    is_mandatry = True

    def __init__(self, size):
        super().__init__(size=size)
        self.entry_count = None

    def read(self, file):
        super().read(file)
        self.entry_count = read_int(file, 4)
