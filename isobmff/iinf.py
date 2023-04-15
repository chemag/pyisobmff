# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_box
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
            box = read_box(file, self.debug)
            if not box:
                break
            if box.box_type == "infe":
                self.item_infos.append(box)

    def __repr__(self):
        repl = ()
        repl += (f"entry_count: {str(len(self.item_infos))}",)
        for item in self.item_infos:
            repl += (repr(item),)
        return super().repr(repl)


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

    def __repr__(self):
        repl = ()
        if self.version == 0 or self.version == 1:
            repl += (f"item_id: {self.item_id}",)
            repl += (f"item_protection_index: {self.item_protection_index}",)
            repl += (f"item_name: {self.item_name}",)
            repl += (f"content_type: {self.content_type}",)
            repl += (f"content_encoding: {self.content_encoding}",)
        if self.version == 1:
            repl += (f"extension_type: {self.extension_type}",)
            repl += (f"item_info_extension: {self.item_info_extension}",)
        if self.version >= 2:
            repl += (f"item_id: {self.item_id}",)
            repl += (f"item_protection_index: {self.item_protection_index}",)
            repl += (f"item_type: {self.item_type}",)
            repl += (f"item_name: {self.item_name}",)
            if self.item_type == "mime":
                repl += (f"content_type: {self.content_type}",)
                repl += (f"content_encoding: {self.content_encoding}",)
            elif self.item_type == "uri ":
                repl += (f"uri_type: {self.uri_type}",)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.11.6.2
# Note that this object descends from ItemInfoExtension.
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

    def __repr__(self):
        repl = ()
        repl += (f"content_location: {self.content_location}",)
        repl += (f"content_md5: {self.content_md5}",)
        repl += (f"content_length: {self.content_length}",)
        repl += (f"transfer_length: {self.transfer_length}",)
        for idx, val in enumerate(self.group_ids):
            repl += (f"group_ids[{idx}]: {val}",)
        return super().repr(repl)
