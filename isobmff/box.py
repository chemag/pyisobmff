# -*- coding: utf-8 -*-
import re

class Box(object):
    """Box
    """

    def __init__(self, size=None, box_type=None):
        self.size = size
        self.box_type = box_type
        self.largesize = None

    def __repr__(self):
        return self.box_type + '(' + str(self.size) + ')\n'

    def get_box_size(self):
        """get box size excluding header"""
        return self.size - 8

    def read(self, file):
        """read box from file"""
        self.size = read_int(file, 4)
        self.box_type = read_string(file, 4)

    def write(self, file):
        """write box to file"""
        pass


class FullBox(Box):
    """FullBox"""

    def __init__(self, box, version=None, flags=None):
        super().__init__(box.size, box.box_type)
        self.version = version
        self.flags = flags

    def __repr__(self):
        srep = super().__repr__()
        rep = ' v' + str(self.version) + '\n'
        return re.sub('\n', rep, srep, flags=re.MULTILINE)

    def get_box_size(self):
        """get box size excluding header"""
        return self.size - 12

    def read(self, file):
        """read box from file"""
        self.version = read_int(file, 1)
        self.flags = read_int(file, 3)

    def write(self, file):
        pass


def read_int(file, length):
    """readint"""
    return int.from_bytes(file.read(length), 'big')

def read_string(file, length=None):
    """readstring
    TODO: convert utf8
    """
    if length:
        res = file.read(length).decode()
    else:
        res = ''.join(iter(lambda: file.read(1).decode('ascii'), '\x00'))
    return res

def indent(rep):
    """indent 2 spaces"""
    return re.sub(r'^', '  ', rep, flags=re.M)
