# -*- coding: utf-8 -*-

import re
from enum import Enum


class AbcBox(type):
    # TODO: human readable implementation of __repr__
    pass


class Box(object):
    box_type = None

    def __init__(self, offset, size=None, largesize=None):
        self.offset = offset
        self.size = size
        self.largesize = largesize

    def __repr__(self):
        rep = ""
        rep += f"offset: 0x{self.offset:08x}" + "\n"
        rep += f"box_type: {self.box_type}" + "\n"
        rep += f"size: {self.size}" + "\n"
        if self.largesize is not None:
            rep += f"largesize: {self.largesize}" + "\n"
        return "Box\n" + indent(rep)

    def get_box_size(self):
        """get box size excluding header"""
        return self.largesize - 16 if self.largesize is not None else self.size - 8

    # read the remaining bytes as simple bytes
    def read(self, file):
        remaining_size = self.get_box_size()
        self.contents = file.read(remaining_size)

    # read the remaining bytes as boxes
    def read_box(self, file):
        read_size = self.get_box_size()
        while read_size > 0:
            box = read_box(file)
            if not box:
                break
            # TODO: Divide by Quantity as it is setattr or append to array
            setattr(self, box.box_type, box)
            read_size -= box.size

    def write(self, file):
        """write box to file"""
        pass


class FullBox(Box):
    box_type = None

    def __init__(self, offset, size, largesize, version, flags):
        super().__init__(offset, size, largesize)
        self.version = version
        self.flags = flags

    def __repr__(self):
        srep = super().__repr__()
        rep = ""
        rep += f"version: {self.version}" + "\n"
        rep += f"flags: {self.flags}" + "\n"
        return "FullBox\n" + srep + indent(rep)

    def get_box_size(self):
        """get box size excluding header"""
        return self.size - 12


class UnimplementedBox(Box):
    def __init__(self, box_type, size, largesize):
        self.box_type = box_type
        super().__init__(size, largesize)

    def __repr__(self):
        return super().__repr__()

    def read(self, file):
        remaining_size = self.get_box_size()
        self.content = file.read(remaining_size)


class Quantity(Enum):
    ZERO_OR_ONE = 0
    EXACTLY_ONE = 1
    ONE_OR_MORE = 2
    ANY_NUMBER = 3


def read_int(file, length):
    byte_array = file.read(length)
    if not byte_array:
        return ""
    return int.from_bytes(byte_array, byteorder="big", signed=False)


def read_string(file, length=None):
    # TODO: convert utf8
    if length:
        res = file.read(length).decode()
    else:
        res = "".join(iter(lambda: file.read(1).decode("ascii"), "\x00"))
    return res


def indent(rep):
    return re.sub(r"^", "  ", rep, flags=re.M)


def get_class_list(cls, res=[]):
    subclasses = getattr(cls, "__subclasses__")()
    for subclass in subclasses:
        get_class_list(subclass, res)
    res.append(cls)
    return res


def read_box(file, debug=0):
    offset = file.tell()
    size = read_int(file, 4)
    if size == "":
        return None
    box_type = read_string(file, 4)
    largesize = None
    if size == 0:
        import code; code.interact(local=locals())  # python gdb/debugging
    elif size == 1:
        largesize = read_int(file, 8)

    if debug > 0:
        print(box_type + "(" + str(size) + ")")
    box_classes = get_class_list(Box)
    box = None
    for box_class in box_classes:
        if box_class.box_type == box_type:
            if box_class.__base__.__name__ == "Box":
                box = box_class(offset=offset, size=size, largesize=largesize)
            elif box_class.__base__.__name__ == "FullBox":
                version = read_int(file, 1)
                flags = read_int(file, 3)
                box = box_class(offset=offset, size=size, largesize=largesize, version=version, flags=flags)
            # read any data left
            box.read(file)
            break
    else:
        # unimplemented box
        if debug > 0:
            print(f"warning: unimplemented box offset: 0x{file.tell() - 8:08x} type: {box_type} size: 0x{size:x} next: 0x{size+file.tell():08x}")
        box = UnimplementedBox(box_type, size, largesize)
        box.read(file)
    return box
