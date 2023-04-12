# -*- coding: utf-8 -*-
from .box import indent
from .box import read_box


class MediaFile(object):

    def __init__(self):
        self.ftyp = None
        self.mdats = []
        self.meta = None
        self.moov = None

    def __repr__(self):
        rep = self.ftyp.__repr__() + '\n'
        rep += self.meta.__repr__() + '\n'
        rep += self.moov.__repr__() + '\n'
        for mdat in self.mdats:
            rep += mdat.__repr__() + '\n'
        return 'ISOBaseMediaFile\n' + indent(rep)

    def read(self, file_name):
        file = open(file_name, 'rb')
        try:
            while True:
                box = read_box(file)
                if not box:
                    break
                if box.box_type == 'mdat':
                    self.mdats.append(box)
                else:
                    setattr(self, box.box_type, box)
        finally:
            file.close()
