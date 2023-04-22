# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_uint


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
            sample_group_description_entry = self.read_box(file)
            if not sample_group_description_entry:
                break
            self.sample_group_description_entries.append(sample_group_description_entry)

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
        for idx, box in enumerate(self.sample_group_description_entries):
            tuples += ((f"sample_group_description_entry[{idx}]", box.contents()),)
        return tuples
