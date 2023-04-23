# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_uint


# ISO/IEC 14496-12:2022, Section 8.9.2
class SampleToGroupBox(FullBox):
    box_type = b"sbgp"

    def read(self, file):
        self.grouping_type = read_uint(file, 4)
        if self.version >= 1:
            self.grouping_type_parameter = read_uint(file, 4)
        entry_count = read_uint(file, 4)
        self.sample_counts = []
        self.group_description_indices = []
        for _ in range(entry_count):
            self.sample_counts.append(read_uint(file, 4))
            self.group_description_indices.append(read_uint(file, 4))

    def contents(self):
        tuples = super().contents()
        tuples += (("grouping_type", self.grouping_type),)
        for idx, val in enumerate(self.sample_counts):
            tuples += ((f"sample_count[{idx}]", val),)
        for idx, val in enumerate(self.group_description_indices):
            tuples += ((f"group_description_index[{idx}]", val),)
        return tuples


# ISO/IEC 14496-12:2022, Section 8.9.3.2
class SampleGroupDescriptionEntry:
    pass


# ISO/IEC 14496-12:2022, Section 8.9.3.2
class VisualSampleGroupEntry(SampleGroupDescriptionEntry):
    pass


# ISO/IEC 14496-12:2022, Section 8.9.3.2
class AudioSampleGroupEntry(SampleGroupDescriptionEntry):
    pass


# ISO/IEC 14496-12:2022, Section 8.9.3.2
class HintSampleGroupEntry(SampleGroupDescriptionEntry):
    pass


# ISO/IEC 14496-12:2022, Section 8.9.3.2
class SubtitleSampleGroupEntry(SampleGroupDescriptionEntry):
    pass


# ISO/IEC 14496-12:2022, Section 8.9.3.2
class TextSampleGroupEntry(SampleGroupDescriptionEntry):
    pass


# ISO/IEC 14496-12:2022, Section 8.9.3.2
class HapticSampleGroupEntry(SampleGroupDescriptionEntry):
    pass


# ISO/IEC 14496-12:2022, Section 8.9.3.2
class VolumetricVisualSampleGroupEntry(SampleGroupDescriptionEntry):
    pass


# ISO/IEC 14496-12:2022, Section 8.9.3
class SampleGroupDescriptionBox(FullBox):
    box_type = b"sgpd"

    def read(self, file):
        self.grouping_type = read_uint(file, 4)
        if self.version >= 1:
            self.default_length = read_uint(file, 4)
        if self.version >= 2:
            self.default_group_description_index = read_uint(file, 4)
        entry_count = read_uint(file, 4)
        self.description_lengths = []
        self.sample_group_description_entries = []
        for _ in range(entry_count):
            if self.version >= 1:
                if self.default_length == 0:
                    self.description_lengths.append(read_uint(file, 4))
            # TODO: must be of SampleGroupDescriptionEntry type
            sample_group_description_entry_length = (
                self.default_length
                if self.default_length != 0
                else self.description_lengths[-1]
            )
            self.sample_group_description_entries.append(
                read_uint(file, sample_group_description_entry_length)
            )
        # skip the remaining data
        # TODO: this should be centralized
        file.seek(self.max_offset)

    def contents(self):
        tuples = super().contents()
        tuples += (("grouping_type", self.grouping_type),)
        if self.version >= 1:
            tuples += (("default_length", self.default_length),)
        if self.version >= 2:
            tuples += (
                (
                    "default_group_description_index",
                    self.default_group_description_index,
                ),
            )
        for idx, val in enumerate(self.description_lengths):
            tuples += ((f"description_length[{idx}]", val),)
        for idx, val in enumerate(self.sample_group_description_entries):
            tuples += ((f"sample_group_description_entry[{idx}]", val),)
        return tuples
