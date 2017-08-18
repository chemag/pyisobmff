# -*- coding: utf-8 -*-
"""
"""
from .box import Box
from .ftyp import Ftyp
from .mdat import Mdat
from .meta import Meta

class MediaFile(object):
    """MediaFile
    """

    def __init__(self):
        self.ftyp = None
        self.mdats = []
        self.meta = None
    
    def read(self, file_name):
        """
        """
        file = open(file_name, 'rb')
        try:
            while True:
                box = Box()
                box.read(file)
                if not box.size:
                    break
                self.__read_box(file, box)
        finally:
            file.close()

    def __read_box(self, file, box):
        if box.box_type == 'ftyp':
            ftyp = Ftyp(box)
            ftyp.read(file)
            self.ftyp = ftyp
        elif box.box_type == 'mdat':
            mdat = Mdat(box)
            mdat.read(file)
            self.mdats.append(mdat)
        elif box.box_type == 'meta':
            meta = Meta(box)
            meta.read(file)
            self.meta = meta
        else:
            box_size = box.size - 8
            if box_size > 0:
                file.read(box_size)
