# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_int
from .box import read_string


class DataEntryUrlBox(FullBox):
    """Data Entry Url Box
    """

    def __init__(self, box):
        super().__init__(box, box.version, box.flags)
        self.location = None

    def read(self, file):
        #url_size = self.size - 8
        self.location = read_string(file)


class DataEntryUrnBox(FullBox):
    """Data Entry Urn Box
    """

    def __init__(self, box):
        super().__init__(box, box.version, box.flags)
        self.location = None

    def read(self, file):
        #url_size = self.size - 8
        self.location = read_string(file)


class DataReferenceBox(FullBox):
    """Data Reference Box
    """

    def __init__(self, box):
        super().__init__(box, box.version, box.flags)
        self.entry_count = None

    def read(self, file):
        self.entry_count = read_int(file, 4)
