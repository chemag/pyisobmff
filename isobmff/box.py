# -*- coding: utf-8 -*-
"""
"""
import re


class AbcBox(type):
    pass


class Box(object):
    """Box
    """
    box_type = None

    def __init__(self, size=None):
        self.size = size
        self.largesize = None

    def __repr__(self):
        return self.box_type + '(' + str(self.size) + ')\n'

    def get_box_size(self):
        """get box size excluding header"""
        return self.size - 8

    def read(self, file):
        """read box from file
        read_size = self.get_box_size()
        #print(file.read(read_size))
        while read_size > 0:
            box = read_box(file)
            if not box:
                break
            setattr(self, box.box_type, box)
            read_size -= box.size
        """ 
        pass

    def write(self, file):
        """write box to file"""
        pass


class FullBox(Box):
    """FullBox"""
    box_type = None

    def __init__(self, size, version=None, flags=None):
        super().__init__(size)
        self.version = version
        self.flags = flags

    def __repr__(self):
        srep = super().__repr__()
        rep = ' v' + str(self.version) + '\n'
        return re.sub('\n', rep, srep, flags=re.MULTILINE)

    def get_box_size(self):
        """get box size excluding header"""
        return self.size - 12


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

def read_box(file):
    """read box from file"""
    size = read_int(file, 4)
    box_type = read_string(file, 4)
    print(box_type + '(' + str(size) + ')')
    box = None

    for subclass in getattr(Box, '__subclasses__')():
        if subclass.box_type == box_type:
            box = subclass.__new__(subclass)
            box.__init__(size=size)
            if box.get_box_size():
                box.read(file)
            #print(subclass.__name__)
    # TODO: 探索は1for文で済ませたい
    for subclass in getattr(FullBox, '__subclasses__')():
        if subclass.box_type == box_type:
            version = read_int(file, 1)
            flags = read_int(file, 3)                    
            box = subclass.__new__(subclass)
            box.__init__(size=size, version=version, flags=flags)
            if box.get_box_size():
                box.read(file)

    return box
