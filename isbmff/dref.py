# -*- coding: utf-8 -*-
from .box import Box



class Url(Box):
    """Data Entry Url Box
    """

    def __inti__(self, file, size):
        super().__init__()
        self.size = size
        self.box_type = 'url '
        url_size = size - 8
        self.location = file.read(url_size).decode()


class Urn(Box):
    """Data Entry Url Box
    """

    def __inti__(self, file, size):
        super().__init__()
        self.size = size
        self.box_type = 'urn '
        url_size = size - 8
        self.location = file.read(url_size).decode()

class Dref(Box):
    """Data Reference Box
    """

    def __init__(self, file, size):
        super().__init__()
        self.size = size
        self.box_type = 'dref'
        self.entry_count = int.from_bytes(file.read(4), 'big')

