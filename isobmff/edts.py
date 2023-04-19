# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import read_uint, read_sint


# ISO/IEC 14496-12:2022, Section 8.6.5
class EditBox(Box):
    box_type = b"edts"

    def read(self, file):
        self.box_list = self.read_box_list(file)

    def contents(self):
        tuples = super().contents()
        for idx, box in enumerate(self.box_list):
            tuples += ((f"box[{idx}]", box.contents()),)
        return tuples


# ISO/IEC 14496-12:2022, Section 8.6.6
class EditListBox(FullBox):
    box_type = b"elst"

    def read(self, file):
        entry_count = read_uint(file, 4)
        self.entries = []
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

    def contents(self):
        tuples = super().contents()
        for idx, val in enumerate(self.entries):
            tuples += ((f'entries[{idx}]["edit_duration"]', val["edit_duration"]),)
            tuples += ((f'entries[{idx}]["media_time"]', val["media_time"]),)
            tuples += (
                (f'entries[{idx}]["media_rate_integer"]', val["media_rate_integer"]),
            )
            tuples += (
                (f'entries[{idx}]["media_rate_fraction"]', val["media_rate_fraction"]),
            )
        return tuples
