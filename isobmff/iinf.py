# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_uint
from .box import read_fixed_size_string
from .box import read_utf8string


# ISO/IEC 14496-12:2022, Section 8.11.6.2
class ItemInformationBox(FullBox):
    box_type = b"iinf"
    is_mandatory = False
    item_infos = []

    def read(self, file):
        count_size = 2 if self.version == 0 else 4
        entry_count = read_uint(file, count_size)
        for _ in range(entry_count):
            box = self.read_box(file)
            if box is None:
                break
            if box.box_type == "infe":
                self.item_infos.append(box)

    def contents(self):
        tuples = super().contents()
        tuples += (("entry_count", str(len(self.item_infos))),)
        for idx, item_info in enumerate(self.item_infos):
            tuples += ((f"item_info[{idx}]", item_info.contents()),)
        return tuples


# ISO/IEC 14496-12:2022, Section 8.11.6.2
class ItemInformationEntry(FullBox):
    box_type = b"infe"

    def read(self, file):
        if self.version == 0 or self.version == 1:
            self.item_id = read_uint(file, 2)
            self.item_protection_index = read_uint(file, 2)
            max_len = self.get_max_offset() - file.tell()
            self.item_name = read_utf8string(file, max_len)
            max_len = self.get_max_offset() - file.tell()
            self.content_type = read_utf8string(file, max_len)
            max_len = self.get_max_offset() - file.tell()
            self.content_encoding = read_utf8string(file, max_len)
        if self.version == 1:
            extension_type = read_fixed_size_string(file, 4)
            fdel = FDItemInfoExtension()
            fdel.read(file)
            self.item_info_extension = fdel
        if self.version >= 2:
            if self.version == 2:
                self.item_id = read_uint(file, 2)
            elif self.version == 3:
                self.item_id = read_uint(file, 4)
            self.item_protection_index = read_uint(file, 2)
            self.item_type = read_fixed_size_string(file, 4)
            max_len = self.get_max_offset() - file.tell()
            self.item_name = read_utf8string(file, max_len)
            if self.item_type == "mime":
                max_len = self.get_max_offset() - file.tell()
                self.content_type = read_utf8string(file, max_len)
                max_len = self.get_max_offset() - file.tell()
                self.content_encoding = read_utf8string(file, max_len)
            elif self.item_type == "uri ":
                max_len = self.get_max_offset() - file.tell()
                self.uri_type = read_utf8string(file, max_len)

    def contents(self):
        tuples = super().contents()
        if self.version == 0 or self.version == 1:
            tuples += (("item_id", self.item_id),)
            tuples += (("item_protection_index", self.item_protection_index),)
            tuples += (("item_name", self.item_name),)
            tuples += (("content_type", self.content_type),)
            tuples += (("content_encoding", self.content_encoding),)
        if self.version == 1:
            tuples += (("extension_type", self.extension_type),)
            tuples += (("item_info_extension", self.item_info_extension.contents()),)
        if self.version >= 2:
            tuples += (("item_id", self.item_id),)
            tuples += (("item_protection_index", self.item_protection_index),)
            tuples += (("item_type", self.item_type),)
            tuples += (("item_name", self.item_name),)
            if self.item_type == "mime":
                tuples += (("content_type", self.content_type),)
                tuples += (("content_encoding", self.content_encoding),)
            elif self.item_type == "uri ":
                tuples += (("uri_type", self.uri_type),)
        return tuples


# ISO/IEC 14496-12:2022, Section 8.11.6.2
# Note that this class descends from ItemInfoExtension.
class FDItemInfoExtension(object):
    group_ids = []

    def read(self, file):
        max_len = self.get_max_offset() - file.tell()
        self.content_location = read_utf8string(file, max_len)
        max_len = self.get_max_offset() - file.tell()
        self.content_md5 = read_utf8string(file, max_len)
        self.content_length = read_uint(file, 8)
        self.transfer_length = read_uint(file, 8)
        entry_count = read_uint(file, 1)
        for _ in range(entry_count):
            group_id = read_uint(file, 4)
            self.group_ids.append(group_id)

    def contents(self):
        tuples = ()
        tuples += (("content_location", self.content_location),)
        tuples += (("content_md5", self.content_md5),)
        tuples += (("content_length", self.content_length),)
        tuples += (("transfer_length", self.transfer_length),)
        for idx, val in enumerate(self.group_ids):
            tuples += ((f"group_ids[{idx}]", val),)
        return tuples
