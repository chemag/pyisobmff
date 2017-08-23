# -*- coding: utf-8 -*-
from .box import FullBox
from .box import indent
from .box import read_box
from .box import read_string


class ItemPropertiesBox(FullBox):
    """Item Properties Box
    """
    box_type = 'iprp'

    def __init__(self, size, version, flags):
        super().__init__(size=size, version=version, flags=flags)
        self.ipco = None

    def __repr__(self):
        return super().__repr__() + indent(self.ipco.__repr__())

    def read(self, file):
        typ = read_string(file, 4) #ipco
        read_size = self.size - 16
        if typ == 'ipco':
            self.ipco = ItemPropertyContainer(read_size)
            self.ipco.read(file)

class ItemPropertyContainer(object):
    """Item Property Container"""

    def __init__(self, size):
        self.size = size
        self.hvcc = None
        self.ispes = []

    def __repr__(self):
        rep = 'ipco\n'
        rep += self.hvcc.__repr__() + '\n'
        for ispe in self.ispes:
            rep += ispe.__repr__()
        return indent(rep)

    def read(self, file):
        """read"""
        read_size = self.size
        while read_size > 0:
            print('read_size : ' + str(read_size))
            box = read_box(file)
            if not box:
                break
            setattr(self, box.box_type, box)
            read_size -= box.size
