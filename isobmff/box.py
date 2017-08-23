# -*- coding: utf-8 -*-
import re
from enum import Enum


class AbcBox(type):
    #TODO: human readable implementation of __repr__ 
    pass

class Box(object):
    box_type = None

    def __init__(self, size=None):
        self.size = size
        self.largesize = None

    def get_box_size(self):
        """get box size excluding header"""
        return self.size - 8

    def read(self, file):
        read_size = self.get_box_size()
        #print(file.read(read_size))
        while read_size > 0:
            box = read_box(file)
            if not box:
                break
            #TODO: Quantityでそのままsetattrか配列にappendか分ける
            setattr(self, box.box_type, box)
            read_size -= box.size

    def write(self, file):
        """write box to file"""
        pass

class FullBox(Box):
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

class Quantity(Enum):
    ZERO_OR_ONE = 0
    EXACTLY_ONE = 1
    ONE_OR_MORE = 2
    ANY_NUMBER = 3

def read_int(file, length):
    return int.from_bytes(file.read(length), byteorder='big', signed=False)

def read_string(file, length=None):
    #TODO: convert utf8
    if length:
        res = file.read(length).decode()
    else:
        res = ''.join(iter(lambda: file.read(1).decode('ascii'), '\x00'))
    return res

def indent(rep):
    return re.sub(r'^', '  ', rep, flags=re.M)

def get_class_list(cls, res=[]):
    subclasses = getattr(cls, '__subclasses__')()
    for subclass in subclasses:
        get_class_list(subclass, res)
    res.append(cls)
    return res

def read_box(file):
    size = read_int(file, 4)
    box_type = read_string(file, 4)
    print(box_type + '(' + str(size) + ')')
    box_classes = get_class_list(Box)
    box = None
    for box_class in box_classes:
        if box_class.box_type == box_type:
            box = box_class.__new__(box_class)
            if box_class.__base__.__name__ == 'FullBox':
                version = read_int(file, 1)
                flags = read_int(file, 3)
                box.__init__(size=size, version=version, flags=flags)
            else:
                box.__init__(size=size)
            if box.get_box_size():
                box.read(file)
            break
    return box
