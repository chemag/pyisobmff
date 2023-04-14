# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import read_box
from .box import read_uint, read_sint


# ISO/IEC 14496-12:2022, Section 8.6.5
class EditBox(Box):
    box_type = "edts"
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


# ISO/IEC 14496-12:2022, Section 8.6.6
class EditListBox(FullBox):
    box_type = "elst"
    entries = []

    def read(self, file):
        entry_count = read_uint(file, 4)
        for _ in range(entry_count):
            entry = {}
            if self.version == 1:
                entry["edit_duration"] = read_uint(file, 8)
                entry["media_time"] = read_sint(file, 8)
            else:
                entry["edit_duration"] = read_uint(file, 4)
                entry["media_time"] = read_sint(file, 4)
            entry["media_rate_integer"] = read_uint(file, 2)
            entry["media_rate_fraction"] = read_uint(file, 2)
            self.entries.append(entry)

    def __repr__(self):
        repl = ()
        for idx, val in enumerate(self.entries):
            repl += (f'entries[{idx}]["edit_duration"]: {val["edit_duration"]}',)
            repl += (f'entries[{idx}]["media_time"]: {val["media_time"]}',)
            repl += (
                f'entries[{idx}]["media_rate_integer"]: {val["media_rate_integer"]}',
            )
            repl += (
                f'entries[{idx}]["media_rate_fraction"]: {val["media_rate_fraction"]}',
            )
        return super().repr(repl)
