# -*- coding: utf-8 -*-
from .box import Box


class Ftyp(Box):
    """File Type Box
    """

    def __init__(self, box):
        super().__init__(box.size, box.box_type)
        self.majar_brand = None
        self.minor_version = None
        self.compatible_brands = []

    def __repr__(self):
        rep = super().__repr__()
        rep += '  ' + self.majar_brand + '\n'
        rep += '  ' + str(self.minor_version) + '\n'
        rep += '  '
        for brand in self.compatible_brands:
            rep += brand + ','
        return rep

    def read(self, file):
        self.majar_brand = file.read(4).decode()
        self.minor_version = int.from_bytes(file.read(4), 'big')
        num_compatible_brands = int((self.size - 16) / 4)
        for _ in range(num_compatible_brands):
            self.compatible_brands.append(file.read(4).decode())

