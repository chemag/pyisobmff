# -*- coding: utf-8 -*-
from .box import Box


class Url(Box):
    """Data Entry Url Box
    """

    def __init__(self, box):
        super().__init__(box.size, box.box_type)
        self.location = None

    def read(self, file):
        url_size = self.size - 8
        self.location = file.read(url_size).decode()


class Urn(Box):
    """Data Entry Url Box
    """

    def __init__(self, box):
        super().__init__(box.size, box.box_type)
        self.location = None

    def read(self, file):
        url_size = self.size - 8
        self.location = file.read(url_size).decode()


class Dref(Box):
    """Data Reference Box
    """

    def __init__(self, box):
        super().__init__(box.size, box.box_type)
        self.entry_count = None

    def read(self, file):
        self.entry_count = int.from_bytes(file.read(4), 'big')
