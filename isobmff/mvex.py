# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import read_uint


# ISO/IEC 14496-12:2022, Section 8.8.1
class MovieExtendsBox(Box):
    box_type = b"mvex"

    def read(self, file):
        # optional MovieExtendsHeaderBox
        # other boxes
        self.box_list = self.read_box_list(file)

    def contents(self):
        tuples = super().contents()
        for idx, box in enumerate(self.box_list):
            tuples += ((f"box[{idx}]", box.contents()),)
        return tuples


# ISO/IEC 14496-12:2022, Section 8.8.2
class MovieExtendsHeaderBox(FullBox):
    box_type = b"mehd"

    def read(self, file):
        if self.version == 1:
            self.fragment_duration = read_uint(file, 8)
        else:
            self.fragment_duration = read_uint(file, 4)

    def contents(self):
        tuples = super().contents()
        tuples += (("fragment_duration", self.fragment_duration),)
        return tuples


# ISO/IEC 14496-12:2022, Section 8.8.3
class TrackExtendsBox(FullBox):
    box_type = b"trex"

    def read(self, file):
        self.track_ID = read_uint(file, 4)
        self.default_sample_description_index = read_uint(file, 4)
        self.default_sample_duration = read_uint(file, 4)
        self.default_sample_size = read_uint(file, 4)
        self.default_sample_flags = read_uint(file, 4)

    def contents(self):
        tuples = super().contents()
        tuples += (("track_ID", self.track_ID),)
        tuples += (
            ("default_sample_description_index", self.default_sample_description_index),
        )
        tuples += (("default_sample_duration", self.default_sample_duration),)
        tuples += (("default_sample_size", self.default_sample_size),)
        tuples += (("default_sample_flags", self.default_sample_flags),)
        return tuples
