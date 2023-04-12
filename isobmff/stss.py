# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_int


class SyncSampleBox(FullBox):
    box_type = "stss"
    is_mandatory = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.entries = []

    def read(self, file):
        entry_count = read_int(file, 4)
        for _ in range(entry_count):
            entry = {}
            entry["sample_number"] = read_int(file, 4)
            self.entries.append(entry)
