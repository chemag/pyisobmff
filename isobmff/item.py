# -*- coding: utf-8 -*-

from .utils import get_class_list
from .utils import tuples_to_string
from .utils import escape_value


class Item:
    item_type = None

    def __init__(
        self,
        item_id,
        item_type,
        fd,
    ):
        self.item_id = item_id
        self.item_type = item_type
        self.parse(fd)

    def parse(self, fd):
        # just store the payload
        self.payload = fd.read()

    def contents(self):
        # a non-Box class has no parent
        tuples = ()
        tuples += (("item_id", self.item_id),)
        tuples += (("item_type", self.item_type),)
        if type(self) is Item:
            tuples += (("payload", escape_value(self.payload)),)
        return tuples

    def __repr__(self):
        tuples = self.contents()
        return tuples_to_string(tuples, indent=0)


def get_item_list():
    item_classes = get_class_list(Item)
    return set(
        item_class.item_type
        for item_class in item_classes
        if "item_type" in dir(item_class)
    )


# coalesce with box.py code
def read_sint(file, length):
    return read_int_generic(file, length, signed=True)


def read_uint(file, length):
    return read_int_generic(file, length, signed=False)


def read_int_generic(file, length, signed):
    byte_array = file.read(length)
    if not byte_array:
        return ""
    return int.from_bytes(byte_array, byteorder="big", signed=signed)
