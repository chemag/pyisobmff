# -*- coding: utf-8 -*-
"""
"""
from .box import Box
from .box import FullBox
from .box import indent
from .ftyp import FileTypeBox
from .mdat import MediaDataBox
from .meta import MetaBox
from .moov import MovieBox


class MediaFile(object):
    """MediaFile
    """

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
            self.ftyp = FileTypeBox(box)
            self.ftyp.read(file)
        elif box.box_type == 'mdat':
            mdat = MediaDataBox(box)
            mdat.read(file)
            self.mdats.append(mdat)
        elif box.box_type == 'meta':
            full_box = FullBox(box)
            full_box.read(file)
            self.meta = MetaBox(full_box)
            self.meta.read(file)
        elif box.box_type == 'moov':
            self.moov = MovieBox(box)
            self.moov.read(file)
        else:
            box_size = box.size - 8
            if box_size > 0:
                file.read(box_size)
