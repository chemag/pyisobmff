# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_uint


# ISO/IEC 14496-12:2022, Section 8.6.1.2
class TimeToSampleBox(FullBox):
    box_type = "stts"
    is_mandatory = True
    entries = []

    def read(self, file):
        self.entry_count = read_uint(file, 4)
        for _ in range(self.entry_count):
            entry = {}
            entry["sample_count"] = read_uint(file, 4)
            entry["sample_delta"] = read_uint(file, 4)
            self.entries.append(entry)
