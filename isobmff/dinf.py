# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_box
from .box import read_uint
from .box import read_utf8string


# ISO/IEC 14496-12:2022, Section 8.7.1.2
class DataInformationBox(Box):
    box_type = b"dinf"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE
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


# ISO/IEC 14496-12:2022, Section 8.7.2.2
class DataReferenceBox(FullBox):
    box_type = b"dref"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE
    data_entry = []

    def read(self, file):
        entry_count = read_uint(file, 4)
        for _ in range(entry_count):
            # only DataEntryBaseBox boxes here
            box = read_box(file, self.debug)
            if not box:
                break
            self.data_entry.append(box)

    def __repr__(self):
        repl = ()
        for box in self.data_entry:
            repl += (repr(box),)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.7.2.2
class DataEntryBaseBox(FullBox):
    pass


# ISO/IEC 14496-12:2022, Section 8.7.2.2
class DataEntryUrlBox(DataEntryBaseBox):
    box_type = b"url "
    is_mandatory = True

    def read(self, file):
        max_len = self.get_max_offset() - file.tell()
        self.location = read_utf8string(file, max_len)

    def __repr__(self):
        repl = ()
        repl += (f'location: "{self.location}"',)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.7.2.2
class DataEntryUrnBox(DataEntryBaseBox):
    box_type = b"urn "
    is_mandatory = True

    def read(self, file):
        max_len = self.get_max_offset() - file.tell()
        self.name = read_utf8string(file, max_len)
        max_len = self.get_max_offset() - file.tell()
        self.location = read_utf8string(file, max_len)

    def __repr__(self):
        repl = ()
        repl += (f'name: "{self.name}"',)
        repl += (f'location: "{self.location}"',)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.7.2.2
class DataEntryImdaBox(DataEntryBaseBox):
    box_type = b"imdt"
    is_mandatory = False

    def read(self, file):
        self.imda_ref_identifier = read_uint(file, 4)

    def __repr__(self):
        repl = ()
        repl += (f'imda_ref_identifier: "{self.imda_ref_identifier}"',)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.7.2.2
class DataEntrySeqNumImdaBox(DataEntryBaseBox):
    box_type = b"snim"
    is_mandatory = False
