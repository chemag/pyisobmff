# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_uint
from .box import read_sint


# ISO/IEC 14496-12:2022, Section 8.6.1.2
class TimeToSampleBox(FullBox):
    box_type = b"stts"
    is_mandatory = True
    entries = []

    def read(self, file):
        entry_count = read_uint(file, 4)
        for _ in range(entry_count):
            entry = {}
            entry["sample_count"] = read_uint(file, 4)
            entry["sample_delta"] = read_uint(file, 4)
            self.entries.append(entry)

    def __repr__(self):
        repl = ()
        if self.debug > 2:
            for idx, val in enumerate(self.entries):
                repl += (f'entry[{idx}]["sample_count"]: {val["sample_count"]}',)
                repl += (f'entry[{idx}]["sample_delta"]: {val["sample_delta"]}',)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.6.1.3
class CompositionOffsetBox(FullBox):
    box_type = b"ctts"
    entries = []

    def read(self, file):
        entry_count = read_uint(file, 4)
        for _ in range(entry_count):
            entry = {}
            entry["sample_count"] = read_uint(file, 4)
            if self.version == 0:
                entry["sample_offset"] = read_uint(file, 4)
            elif self.version == 1:
                entry["sample_offset"] = read_sint(file, 4)
            self.entries.append(entry)

    def __repr__(self):
        repl = ()
        if self.debug > 2:
            for idx, val in enumerate(self.entries):
                repl += (f'entry[{idx}]["sample_count"]: {val["sample_count"]}',)
                repl += (f'entry[{idx}]["sample_offset"]: {val["sample_offset"]}',)
        return super().repr(repl)
