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


def tuples_to_string(tuples, indent, tab_size=TAB_SIZE):
    out = ""
    for key, val in tuples:
        # TODO(chema): check no boxes as val
        if type(val) is tuple:
            out += tuples_to_string(val, indent + 1)
        else:
            tab = " " * tab_size * (indent if key == "path" else (indent + 1))
            out += f"{tab}{key}: {escape_value(val)}\n"
    return out


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


def decode_posix_portable_filename(in_str):
    out_str = "".join(
        chr(c) if c in PORTABLE_FILENAME_CHARACTER_SET else f"\\x{c:02x}"
        for c in in_str
    )
    return out_str


# class management
def get_class_list(cls, res=set()):
    subclasses = getattr(cls, "__subclasses__")()
    for subclass in subclasses:
        get_class_list(subclass, res)
    res |= {cls}
    return set(res)


# binary i/o
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
    while nbytes < max_len:
        bstr += file.read(1)
        nbytes += 1
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
