# -*- coding: utf-8 -*-

import re
from enum import Enum


class AbcBox(type):
    # TODO: human readable implementation of __repr__
    pass


# ISO/IEC 14496-12:2022, Section 4.2.2
class Box(object):
    box_type = None

    def __init__(self, offset, size, largesize, debug):
        self.offset = offset
        self.size = size
        self.largesize = largesize
        self.debug = debug

    def repr(self, repl=None):
        new_repl = ()
        new_repl += (f"offset: 0x{self.offset:08x}",)
        new_repl += (f"box_type: {self.box_type}",)
        new_repl += (f"size: {self.size}",)
        if self.largesize is not None:
            new_repl += (f"largesize: {self.largesize}",)
        if repl is not None:
            new_repl += repl
        return f"[{self.box_type}]\n" + indent("\n".join(new_repl))

    def __repr__(self):
        return self.repr()

    def get_max_offset(self):
        """get box size excluding header"""
        return self.offset + (self.size if self.largesize is None else self.largesize)

    # read the remaining bytes as simple bytes
    def read(self, file):
        offset = file.tell()
        max_offset = self.get_max_offset()
        self.contents = file.read(max_offset - offset)

    # read the remaining bytes as boxes
    def read_box(self, file):
        while file.tell() < max_offset:
            box = read_box(file, self.debug)
            if not box:
                break

    def write(self, file):
        """write box to file"""
        pass


# ISO/IEC 14496-12:2022, Section 4.2.2
class FullBox(Box):
    box_type = None

    def __init__(self, offset, size, largesize, version, flags, debug):
        super().__init__(offset, size, largesize, debug)
        self.version = version
        self.flags = flags

    def repr(self, repl=None):
        new_repl = ()
        new_repl += (f"version: {self.version}",)
        new_repl += (f"flags: {self.flags}",)
        if repl is not None:
            new_repl += repl
        return super().repr(new_repl)

    def __repr__(self):
        return self.repr()


# generic container Box
class ContainerBox(Box):
    # used to implement generic container boxes more easily
    box_list = []

    def read(self, file):
        while file.tell() < self.get_max_offset():
            box = read_box(file, self.debug)
            self.box_list.append(box)

    def __repr__(self):
        repl = ()
        for box in self.box_list:
            repl += (repr(box),)
        return super().repr(repl)


class UnimplementedBox(Box):
    def __init__(self, offset, box_type, size, largesize, debug):
        self.box_type = box_type
        super().__init__(offset, size, largesize, debug)

    def __repr__(self):
        return super().__repr__()

    def read(self, file):
        offset = file.tell()
        max_offset = self.get_max_offset()
        self.content = file.read(max_offset - offset)


class Quantity(Enum):
    ZERO_OR_ONE = 0
    EXACTLY_ONE = 1
    ONE_OR_MORE = 2
    ANY_NUMBER = 3


def read_sint(file, length):
    return read_int_generic(file, length, signed=True)


def read_uint(file, length):
    return read_int_generic(file, length, signed=False)


def read_int_generic(file, length, signed):
    byte_array = file.read(length)
    if not byte_array:
        return ""
    return int.from_bytes(byte_array, byteorder="big", signed=signed)


def read_fixed_size_string(file, length):
    return file.read(length).decode("ascii")


def read_fourcc(file):
    return file.read(4)


def read_utf8string(file, max_len):
    if max_len == 0:
        return ""
    bstr = file.read(1)
    nbytes = 1
    while bstr[-1] != 0 and nbytes < max_len:
        bstr += file.read(1)
    return bstr.decode("ascii")


def read_bytes(file, length):
    return file.read(length)


def indent(rep):
    return re.sub(r"^", "  ", rep, flags=re.M)


def int_to_fixed_point_16_16(num):
    int_part = num >> 16
    frac_part = (num & 0xFFFF) / 0xFFFF
    return int_part + frac_part


def get_class_list(cls, res=[]):
    subclasses = getattr(cls, "__subclasses__")()
    for subclass in subclasses:
        get_class_list(subclass, res)
    res.append(cls)
    return res


def get_class_type(cls):
    while cls:
        if cls.__name__ == "Box":
            return "Box"
        elif cls.__name__ == "FullBox":
            return "FullBox"
        cls = cls.__base__
    return "Unknown"


def read_box(file, debug):
    offset = file.tell()
    size = read_uint(file, 4)
    if size == "":
        return None
    try:
        box_type = read_fourcc(file)
    except:
        raise Exception(f"error: cannot read box type at location 0x{offset+4:08x}")
    if debug > 1:
        print(f"read_box() offset: 0x{offset:08x} size: 0x{size:08x} type: {box_type}")
    largesize = None
    if size == 0:
        raise Exception(f"ERROR: UNIMPLEMENTED size=0 BoxHeader (Section 4.2.2 Page 8)")
    elif size == 1:
        largesize = read_uint(file, 8)
    box_classes = get_class_list(Box)
    box = None
    for box_class in box_classes:
        if box_class.box_type == box_type:
            class_type = get_class_type(box_class)
            if class_type == "Box":
                box = box_class(
                    offset=offset, size=size, largesize=largesize, debug=debug
                )
            elif class_type == "FullBox":
                version = read_uint(file, 1)
                flags = read_uint(file, 3)
                box = box_class(
                    offset=offset,
                    size=size,
                    largesize=largesize,
                    version=version,
                    flags=flags,
                    debug=debug,
                )
            else:
                print(f"ERROR: INVALID BOX TYPE (offset: 0x{offset:08x})")
                break
            # read any data left
            box.read(file)
            break
    else:
        # unimplemented box
        if debug > 0:
            print(
                f"warning: unimplemented box offset: 0x{offset:08x} type: {box_type} size: 0x{size:x} next: 0x{size+offset:08x}"
            )
        box = UnimplementedBox(offset, box_type, size, largesize, debug)
        box.read(file)
    return box
