# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_int


class TimeToSampleBox(FullBox):
    box_type = "stts"
    is_mandatory = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.entry_count = None
        self.entries = []

    def read(self, file):
        self.entry_count = read_int(file, 4)
        for _ in range(self.entry_count):
            entry = {}
            entry["sample_count"] = read_int(file, 4)
            entry["sample_delta"] = read_int(file, 4)
            self.entries.append(entry)
