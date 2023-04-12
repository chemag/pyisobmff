
# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_int


class SampleSizeBox(FullBox):
    box_type = 'stsz'
    is_mandatory = False

    def __init__(self, size, version, flags):
        super().__init__(size=size, version=version, flags=flags)
        self.sample_size = None
        self.entries = []

    def read(self, file):
        self.sample_size = read_int(file, 4)
        sample_count = read_int(file, 4)

        if self.sample_size == 0:
            for _ in range(sample_count):
                entry = {}
                entry['entry_size'] = read_int(file, 4)
                self.entries.append(entry)
