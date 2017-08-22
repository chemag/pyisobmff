# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import indent
from .box import read_int
from .box import read_string
from .hvc import HEVCConfigurationBox
from .ispe import SpaialExtentBox


class ItemPropertiesBox(FullBox):
    """Item Properties Box
    """

    def __init__(self, box):
        super().__init__(box=box, version=box.version, flags=box.flags)
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
        read_size = self.size
        while read_size > 0:
            print('read_size : ' + str(read_size))
            box = Box()
            box.read(file)
            if not box.size:
                break
            self.__read_box(file, box)
            read_size -= box.size

    def __read_box(self, file, box):
        print(box.box_type + ' ' + str(box.size))

        if box.box_type == 'hvcC':
            self.hvcc = HEVCConfigurationBox(box)
            self.hvcc.read(file)
        if box.box_type == 'ispe':
            ispe = SpaialExtentBox(box)
            ispe.read(file)
            self.ispes.append(ispe)
        if box.box_type == 'ipma':
            print(file.read(box.size - 8))
        else:
            pass
            #box_size = box.size - 8
            #if box_size > 0:
            #    print(file.read(box_size))
