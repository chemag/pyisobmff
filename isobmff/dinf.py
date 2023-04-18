# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
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
            self.box_list = self.read_box_list(file)

    def contents(self):
        tuples = super().contents()
        for idx, box in enumerate(self.box_list):
            tuples += ((f"box[{idx}]", box.contents()),)
        return tuples


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
            self.data_entry = self.read_box_list(file)

    def contents(self):
        tuples = super().contents()
        for idx, box in enumerate(self.data_entry):
            tuples += ((f"data_entry[{idx}]", box.contents()),)
        return tuples


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

    def contents(self):
        tuples = super().contents()
        tuples += (("location", f'"{self.location}"'),)
        return tuples


# ISO/IEC 14496-12:2022, Section 8.7.2.2
class DataEntryUrnBox(DataEntryBaseBox):
    box_type = b"urn "
    is_mandatory = True

    def read(self, file):
        max_len = self.get_max_offset() - file.tell()
        self.name = read_utf8string(file, max_len)
        max_len = self.get_max_offset() - file.tell()
        self.location = read_utf8string(file, max_len)

    def contents(self):
        tuples = super().contents()
        tuples += (("name", self.name),)
        tuples += (("location", self.location),)
        return tuples


# ISO/IEC 14496-12:2022, Section 8.7.2.2
class DataEntryImdaBox(DataEntryBaseBox):
    box_type = b"imdt"
    is_mandatory = False

    def read(self, file):
        self.imda_ref_identifier = read_uint(file, 4)

    def contents(self):
        tuples = super().contents()
        tuples += (("imda_ref_identifier", self.imda_ref_identifier),)
        return tuples


# ISO/IEC 14496-12:2022, Section 8.7.2.2
class DataEntrySeqNumImdaBox(DataEntryBaseBox):
    box_type = b"snim"
    is_mandatory = False
