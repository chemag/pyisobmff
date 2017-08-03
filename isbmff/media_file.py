# -*- coding: utf-8 -*-
"""
"""
from .ftyp import Ftyp
from .mdat import Mdat
from .meta import Meta

class MediaFile(object):
    """MediaFile
    """

    def __init__(self, file_name):
        self.mdats = []
        f = open(file_name, 'rb')
        try:
            while True:
                size = int.from_bytes(f.read(4), 'big')
                if not size:
                    break
                self.__read_box(f, size)
        finally:
            f.close()

    def __read_box(self, file, size):
        box_type = file.read(4).decode()

        if box_type == 'ftyp':
            self.ftyp = Ftyp(file, size)
        elif box_type == 'mdat':
            self.mdats.append(Mdat(file, size))
        elif box_type == 'meta':
            self.meta = Meta(file, size)
        else:
            box_size = size - 8
            if box_size > 0:
                file.read(box_size)
