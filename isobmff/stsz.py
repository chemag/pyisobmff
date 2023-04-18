# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_uint


# ISO/IEC 14496-12:2022, Section 8.7.3
class SampleSizeBox(FullBox):
    box_type = b"stsz"
    is_mandatory = False
    entries = []

    def read(self, file):
        self.sample_size = read_uint(file, 4)
        sample_count = read_uint(file, 4)
        if self.sample_size == 0:
            for _ in range(sample_count):
                entry = {}
                entry["entry_size"] = read_uint(file, 4)
                self.entries.append(entry)

    def contents(self):
        tuples = super().contents()
        tuples += (("sample_size", self.sample_size),)
        if self.debug > 2:
            for idx, val in enumerate(self.entries):
                tuples += ((f"entries[{idx}]", val),)
        return tuples
