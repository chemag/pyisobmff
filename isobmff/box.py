# -*- coding: utf-8 -*-

import re
import string
import struct
from enum import Enum


TAB_SIZE = 2


def escape_value(s):
    if isinstance(s, str):
        # escape string
        return "".join(c if c in string.printable else "\\x%02x" % ord(c) for c in s)
    return s


def tuples_to_string(tuples, indent):
    out = ""
    for key, val in tuples:
        # TODO(chema): check no boxes as val
        if type(val) is tuple:
            out += tuples_to_string(val, indent + 1)
        else:
            tab = " " * TAB_SIZE * (indent if key == "path" else (indent + 1))
            out += f"{tab}{key}: {escape_value(val)}\n"
    return out


def find_subbox(box, full_path):
    # check if this is the box
    if box.path.strip() == full_path.strip():
        return box
    # look for boxes and lists of boxes
    b = Box
    for var, child in box.__dict__.items():
        if issubclass(child.__class__, b):
            return find_subbox(child, full_path)
        elif issubclass(child.__class__, list):
            for item in child:
                if issubclass(item.__class__, b):
                    if full_path.strip() == item.path.strip() or full_path.startswith(
                        item.path + "/"
                    ):
                        return find_subbox(item, full_path)
    return None


# decode a bytes string into a string containing only characters
# from the POSIX portable filename character set. For all other
# characters, use "\\x%02x".
#
# The Open Group Base Specifications Issue 7, 2018 edition
# IEEE Std 1003.1-2017 (Revision of IEEE Std 1003.1-2008)
#
# 3.282 Portable Filename Character Set
#
# The set of characters from which portable filenames are constructed.
#
# A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
# a b c d e f g h i j k l m n o p q r s t u v w x y z
# 0 1 2 3 4 5 6 7 8 9 . _ -
#
# The last three characters are the <period>, <underscore>, and
# <hyphen-minus> characters, respectively. See also Pathname.
PORTABLE_FILENAME_CHARACTER_SET = list(
    ord(c)
    for c in (string.ascii_uppercase + string.ascii_lowercase + string.digits + "._-")
)


def decode_posix_portable_filename(box_type):
    box_type_str = "".join(
        chr(c) if c in PORTABLE_FILENAME_CHARACTER_SET else f"\\x{c:02x}"
        for c in box_type
    )
    return box_type_str


# ISO/IEC 14496-12:2022, Section 4.2.2
class Box:
    box_type = None

    def __init__(
        self, offset, payload_offset, path, size, largesize, max_offset, debug
    ):
        self.offset = offset
        self.payload_offset = payload_offset
        self.path = path
        self.subpath = {}
        self.size = size
        self.largesize = largesize
        self.max_offset = self.offset + self.get_size()
        if max_offset is not None:
            self.max_offset = min(self.max_offset, max_offset)
        self.debug = debug

    def contents(self):
        # a non-Box class has no parent
        tuples = ()
        tuples += (("path", self.path),)
        tuples += (("offset", f"0x{self.offset:08x}"),)
        tuples += (("box_type", self.box_type),)
        tuples += (("size", self.size),)
        if self.largesize is not None:
            tuples += (("largesize", self.largesize),)
        return tuples

    def __repr__(self):
        tuples = self.contents()
        return tuples_to_string(tuples, indent=0)

    def get_parent_name(self):
        name_list = self.path.split("/")
        if len(name_list) >= 2:
            return name_list[-2]
        return "/"

    @classmethod
    def get_path(cls, path, box_type, parent):
        box_type_str = decode_posix_portable_filename(box_type)
        if parent is None:
            new_path = path + "/" + box_type_str
        elif box_type_str not in parent.subpath:
            new_path = path + "/" + box_type_str
            parent.subpath[box_type_str] = 2
        else:
            new_path = path + "/" + box_type_str + str(parent.subpath[box_type_str])
            parent.subpath[box_type_str] += 1
        return new_path

    def get_size(self):
        """get box size, including header"""
        return self.size if self.largesize is None else self.largesize

    # default read() operation
    # read the remaining bytes as just bytes
    def read(self, file):
        self.read_as_bytes(file)

    # read the remaining bytes as simple bytes
    def read_as_bytes(self, file):
        offset = file.tell()
        return file.read(self.max_offset - offset)

    # read the remaining bytes as boxes
    def read_box_list(self, file):
        box_list = []
        while file.tell() < self.max_offset:
            box = self.read_box(file)
            if box is None:
                break
            box_list.append(box)
        return box_list

    # read a single box
    def read_box(self, file):
        return read_box(file, self.path, self.debug, self, self.max_offset)

    def write(self, file):
        """write box to file"""
        pass


# ISO/IEC 14496-12:2022, Section 4.2.2
class FullBox(Box):
    box_type = None

    def __init__(
        self,
        offset,
        payload_offset,
        path,
        size,
        largesize,
        max_offset,
        version,
        flags,
        debug,
    ):
        super().__init__(
            offset, payload_offset, path, size, largesize, max_offset, debug
        )
        self.version = version
        self.flags = flags

    def contents(self):
        tuples = super().contents()
        tuples += (("version", self.version),)
        tuples += (("flags", self.flags),)
        return tuples


# generic container Box
class ContainerBox(Box):
    # used to implement generic container boxes more easily

    def read(self, file):
        self.box_list = self.read_box_list(file)

    def contents(self):
        tuples = super().contents()
        for box in self.box_list:
            tuples += (("box", box.contents()),)
        return tuples


class UnimplementedBox(Box):
    def __init__(
        self, offset, payload_offset, path, box_type, size, largesize, max_offset, debug
    ):
        self.box_type = box_type
        super().__init__(
            offset, payload_offset, path, size, largesize, max_offset, debug
        )

    def read(self, file):
        self.bytes = self.read_as_bytes(file)

    def contents(self):
        tuples = super().contents()
        if self.debug > 2:
            tuples += (("bytes", f"{self.bytes}"),)
        return tuples


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


def read_extended_type(file):
    return file.read(16)


def read_utf8string(file, max_len):
    if max_len == 0:
        return ""
    bstr = file.read(1)
    nbytes = 1
    while bstr[-1] != 0 and nbytes < max_len:
        bstr += file.read(1)
    return bstr.decode("ascii", errors="ignore")


def read_bytes(file, length):
    return file.read(length)


def indent(rep):
    return re.sub(r"^", "  ", rep, flags=re.M)


def ntohl(num):
    return struct.unpack(">I", struct.pack("=I", num))[0]


def ntohs(num):
    return struct.unpack(">H", struct.pack("=H", num))[0]


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


def get_atom_list():
    box_classes = get_class_list(Box)
    return [box_class.box_type for box_class in box_classes]


def get_class_type(cls):
    while cls:
        if cls.__name__ == "Box":
            return "Box"
        elif cls.__name__ == "FullBox":
            return "FullBox"
        cls = cls.__base__
    return "Unknown"


# TODO(chema): move function to Box/BoxHeader/FullBox/FullBoxHeader
def read_box(file, path, debug, parent=None, max_offset=None):
    # 1. read the BoxHeader fields
    offset = file.tell()
    if max_offset is not None and (max_offset - file.tell()) < 4:
        raise Exception(
            f"error: read_box() no space for size field in Box Header max_offset: 0x{max_offset:08x} file.tell(): 0x{file.tell():08x}"
        )
        return None
    size = read_uint(file, 4)
    if size == "":
        raise Exception(
            f"error: read_box() empty size field in Box Header file.tell(): 0x{file.tell():08x}"
        )
        return None
    try:
        if max_offset is not None and (max_offset - file.tell()) < 4:
            raise Exception(
                f"error: read_box() no space for box_type field in Box Header max_offset: 0x{max_offset:08x} file.tell(): 0x{file.tell():08x}"
            )
            return None
        box_type = read_fourcc(file)
    except:
        raise Exception(f"error: cannot read box type at location 0x{offset+4:08x}")
    if debug > 2:
        print(f"read_box() offset: 0x{offset:08x} size: 0x{size:08x} type: {box_type}")
    largesize = None
    if size == 0:
        raise Exception(f"error: UNIMPLEMENTED size=0 BoxHeader (Section 4.2.2 Page 8)")
    elif size == 1:
        if max_offset is not None and (max_offset - file.tell()) < 8:
            raise Exception(
                f"error: read_box() no space for largesize field in Box Header max_offset: 0x{max_offset:08x} file.tell(): 0x{file.tell():08x}"
            )
            return None
        largesize = read_uint(file, 8)
    full_box_type = box_type
    if box_type == b"uuid":
        if max_offset is not None and (max_offset - file.tell()) < 16:
            raise Exception(
                f"error: read_box() no space for extended_type field in Box Header max_offset: 0x{max_offset:08x} file.tell(): 0x{file.tell():08x}"
            )
            return None
        extended_type = read_extended_type(file)
        full_box_type = extended_type
    payload_offset = file.tell()
    # 2. calculate the full path
    new_path = Box.get_path(path, box_type, parent)
    # 3. find the right Box/FullBox
    box_classes = get_class_list(Box)
    box = None
    for box_class in box_classes:
        if box_class.box_type == full_box_type:
            class_type = get_class_type(box_class)
            if class_type == "Box":
                box = box_class(
                    offset=offset,
                    payload_offset=payload_offset,
                    path=new_path,
                    size=size,
                    largesize=largesize,
                    max_offset=max_offset,
                    debug=debug,
                )
            elif class_type == "FullBox":
                if max_offset is not None and (max_offset - file.tell()) < 4:
                    raise Exception(
                        f"error: read_box() no space for version/flags field in Box Header max_offset: 0x{max_offset:08x} file.tell(): 0x{file.tell():08x}"
                    )
                    return None
                version = read_uint(file, 1)
                flags = read_uint(file, 3)
                box = box_class(
                    offset=offset,
                    payload_offset=payload_offset,
                    path=new_path,
                    size=size,
                    largesize=largesize,
                    version=version,
                    flags=flags,
                    max_offset=max_offset,
                    debug=debug,
                )
            else:
                raise Exception(f"error: INVALID BOX TYPE (offset: 0x{offset:08x})")
                break
            # read the box
            box.read(file)
            break
    else:
        # unimplemented box
        if debug > 0:
            print(
                f"warning: unimplemented box offset: 0x{offset:08x} type: {full_box_type} size: 0x{size:x} next: 0x{size+offset:08x}"
            )
        box = UnimplementedBox(
            offset,
            payload_offset,
            new_path,
            full_box_type,
            size,
            largesize,
            max_offset,
            debug,
        )
        box.read(file)
    return box
