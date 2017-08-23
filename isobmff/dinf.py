# -*- coding: utf-8 -*-
"""
dinf
"""
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_box
from .box import read_int
from .box import read_string


class DataInformationBox(Box):
    """Data Information Box
    """
    box_type = 'dinf'
    is_mandatry = True
    quantity = Quantity.EXACTLY_ONE


class DataReferenceBox(FullBox):
    """Data Reference Box
    """
    box_type = 'dref'
    is_mandatry = True
    quantity = Quantity.EXACTLY_ONE

    def __init__(self, size, version, flags):
        super().__init__(size=size, version=version, flags=flags)
        self.data_entry = []

    def read(self, file):
        entry_count = read_int(file, 4)
        for _ in range(entry_count):
            box = read_box(file)
            if not box:
                break
            self.data_entry.append(box)


class DataEntryUrlBox(FullBox):
    """Data Entry Url Box
    """
    box_type = 'url '
    is_mandatry = True

    def __init__(self, size, version, flags):
        super().__init__(size=size, version=version, flags=flags)
        self.location = None

    def read(self, file):
        self.location = read_string(file)


class DataEntryUrnBox(FullBox):
    """Data Entry Urn Box
    """
    box_type = 'urn '
    is_mandatry = True

    def __init__(self, size, version, flags):
        super().__init__(size=size, version=version, flags=flags)
        self.name = None
        self.location = None

    def read(self, file):
        self.name = read_string(file)
        self.location = read_string(file)
