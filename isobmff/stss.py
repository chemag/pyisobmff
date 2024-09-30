# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_uint


# ISO/IEC 14496-12:2022, Section 8.6.2
class SyncSampleBox(FullBox):
    box_type = b"stss"
    is_mandatory = False

    def read(self, file):
        entry_count = read_uint(file, 4)
        self.entries = []
        for _ in range(entry_count):
            entry = {}
            entry["sample_number"] = read_uint(file, 4)
            self.entries.append(entry)

    def contents(self):
        tuples = super().contents()
        if self.debug > 2:
            for idx, entry in enumerate(self.entries):
                tuples += ((f'entry[{idx}]["sample_number"]', entry["sample_number"]),)
        return tuples
