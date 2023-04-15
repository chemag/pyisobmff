# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_uint


# ISO/IEC 14496-12:2022, Section 8.16.3
class SegmentIndexBox(FullBox):
    box_type = "sidx"
    references = []

    def read(self, file):
        self.reference_ID = read_uint(file, 4)
        self.timescale = read_uint(file, 4)
        count_size = 4 if self.version == 0 else 8
        self.earliest_presentation_time = read_uint(file, count_size)
        self.first_offset = read_uint(file, count_size)
        self.reserved = read_uint(file, 2)
        reference_count = read_uint(file, 2)
        for _ in range(reference_count):
            reference = {}
            word1 = read_uint(file, 4)
            reference["reference_type"] = word1 >> 31
            reference["reference_size"] = word1 & 0x7FFFFFFF
            word2 = read_uint(file, 4)
            reference["starts_with_SAP"] = word2 >> 31
            reference["SAP_type"] = (word2 >> 28) & 0x7
            reference["SAP_delta_time"] = word2 & 0x0FFFFFFF
            self.references.append(reference)
        # skip the remaining data
        max_offset = self.get_max_offset()
        file.seek(max_offset)

    def __repr__(self):
        repl = ()
        repl += (f"reference_ID: {self.reference_ID}",)
        repl += (f"timescale: {self.timescale}",)
        repl += (f"earliest_presentation_time: {self.earliest_presentation_time}",)
        repl += (f"first_offset: {self.first_offset}",)
        repl += (f"reserved: {self.reserved}",)
        for idx, val in enumerate(self.references):
            repl += (f'reference[{idx}].reference_type: {val["reference_type"]}',)
            repl += (f'reference[{idx}].reference_size: {val["reference_size"]}',)
            repl += (f'reference[{idx}].starts_with_SAP: {val["starts_with_SAP"]}',)
            repl += (f'reference[{idx}].SAP_type: {val["SAP_type"]}',)
            repl += (f'reference[{idx}].SAP_delta_time: {val["SAP_delta_time"]}',)
        return super().repr(repl)
