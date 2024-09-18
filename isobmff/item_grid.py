# -*- coding: utf-8 -*-
from .item import Item
from .box import read_uint


# ISO/IEC 23008-12:2022, Section 6.6.2.3
class GridItem(Item):
    item_type = b"grid"

    def parse(self, fd):
        # just store the payload
        # unsigned int(8) version = 0;
        self.version = read_uint(fd, 1)
        # unsigned int(8) flags;
        self.flags = read_uint(fd, 1)
        # tmp, non-parsable variable
        # unsigned int FieldLength = ((flags & 1) + 1) * 16;
        FieldLengthBytes = ((self.flags & 1) + 1) * 2
        # unsigned int(8) rows_minus_one;
        self.rows_minus_one = read_uint(fd, 1)
        # unsigned int(8) columns_minus_one;
        self.columns_minus_one = read_uint(fd, 1)
        # unsigned int(FieldLength) output_width;
        self.output_width = read_uint(fd, FieldLengthBytes)
        # unsigned int(FieldLength) output_height;
        self.output_height = read_uint(fd, FieldLengthBytes)

    def contents(self):
        tuples = super().contents()
        tuples += (("version", self.version),)
        tuples += (("flags", self.flags),)
        tuples += (("rows_minus_one", self.rows_minus_one),)
        tuples += (("columns_minus_one", self.columns_minus_one),)
        tuples += (("output_width", self.output_width),)
        tuples += (("output_height", self.output_height),)
        return tuples
