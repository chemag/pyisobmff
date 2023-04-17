# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import read_uint
from .box import read_bytes
from .box import read_utf8string
from .stbl import VisualSampleEntry


# ETSI TS 103 190-2 v1.2.1, Section E.4
class AC4SampleEntry(Box):
    box_type = b"ac-4"
    box_list = []

    def read(self, file):
        self.reserved1 = read_uint(file, 6)
        self.data_reference_index = read_uint(file, 2)
        self.reserved2 = read_uint(file, 8)
        self.channel_count = read_uint(file, 2)
        self.sample_size = read_uint(file, 2)
        self.reserved3 = read_uint(file, 4)
        self.sampling_frequency = read_uint(file, 2)
        self.reserved4 = read_uint(file, 2)
        self.box_list = self.read_box_list(file)

    def __repr__(self):
        repl = ()
        repl += (f"reserved1: {self.reserved1}",)
        repl += (f"data_reference_index: {self.data_reference_index}",)
        repl += (f"reserved2: {self.reserved2}",)
        repl += (f"channel_count: {self.channel_count}",)
        repl += (f"sample_size: {self.sample_size}",)
        repl += (f"reserved3: {self.reserved3}",)
        repl += (f"sampling_frequency: {self.sampling_frequency}",)
        repl += (f"reserved4: {self.reserved4}",)
        for box in self.box_list:
            repl += (repr(box),)
        return super().repr(repl)


# ETSI TS 102 366 v1.4.1, Section E.6.1
class AC4DsiV1(object):
    presentations = []

    def __init__(self, max_offset):
        self.max_offset = max_offset

    def read(self, file):
        total_bytes = read_uint(file, 3)
        self.ac4_dsi_version = total_bytes >> 21
        self.bitstream_version = (total_bytes >> 14) & 0x7F
        self.fs_index = (total_bytes >> 13) & 0x01
        self.frame_rate_index = (total_bytes >> 9) & 0x0F
        self.n_presentations = total_bytes & 0x01FF
        # TODO(chema): Starting here, the reading is not
        # byte-aligned across classes. For example, if
        # bitstream_version > 1, then the next block is
        # either 1, 18, or 146-bit long
        offset = file.tell()
        self.remaining = read_bytes(file, self.max_offset - offset)

    def __repr__(self):
        repl = ()
        repl += (f"ac4_dsi_version: {self.ac4_dsi_version}",)
        repl += (f"bitstream_version: {self.bitstream_version}",)
        repl += (f"fs_index: {self.fs_index}",)
        repl += (f"frame_rate_index: {self.frame_rate_index}",)
        repl += (f"n_presentations: {self.n_presentations}",)
        repl += (f"remaining: {self.remaining}",)
        return "\n".join(repl)


# ETSI TS 102 366 v1.4.1, Section E.5
class AC4SpecificBox(Box):
    box_type = b"dac4"

    def read(self, file):
        self.ac4_dsi_v1 = AC4DsiV1(max_offset=self.get_max_offset())
        self.ac4_dsi_v1.read(file)

    def __repr__(self):
        repl = ()
        repl += (f"ac4_dsi_v1: {self.ac4_dsi_v1}",)
        return super().repr(repl)


# ETSI TS 102 366 v1.4.1, Section E.5a
class AC4PresentationLabelBox(FullBox):
    box_type = b"lac4"
    presentations = []

    def read(self, file):
        half = read_uint(file, 2)
        self.reserved = half >> 9
        num_presentation_labels = half & 0x01FF
        for _ in range(num_presentation_labels):
            presentation = {}
            half = read_uint(file, 2)
            presentation["reserved"] = half >> 9
            presentation["presentation_id"] = half & 0x01FF
            max_len = self.get_max_offset() - file.tell()
            presentation["presentation_label"] = read_utf8string(file, max_len)
            self.presentations.append(presentation)

    def __repr__(self):
        repl = ()
        repl += (f"reserved: {self.reserved}",)
        for idx, val in enumerate(self.presentations):
            repl += (f'presentation[{idx}]["reserved"]: {val["reserved"]}',)
            repl += (
                f'presentation[{idx}]["presentation_id"]: {val["presentation_id"]}',
            )
            repl += (
                f'presentation[{idx}]["presentation_label"]: {val["presentation_label"]}',
            )
        return super().repr(repl)
