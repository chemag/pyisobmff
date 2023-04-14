# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_uint


# ISO/IEC 14496-12:2022, Section 8.16.3
class SegmentIndexBox(FullBox):
    box_type = "sidx"
    references = []

    def read(self, file):
        count_size = 4 if self.version == 0 else 8
        self.earliest_presentation_time = read_uint(file, count_size)
        self.first_offset = read_uint(file, count_size)
        self.reserved = read_uint(file, 2)
        reference_count = read_uint(file, 2)
        for _ in range(reference_count):
            reference = {}
            word = read_uint(file, 4)
            reference.reference_type = word >> 31
            reference.reference_size = word & 0x7FFFFFFF
            word = read_uint(file, 4)
            reference.starts_with_SAP = word >> 31
            reference.SAP_type = (word >> 28) & 0x7
            reference.SAP_delta_time = word & 0x0FFFFFFF
            self.references.append(reference)

    def __repr__(self):
        repl = ()
        repl += (f"earliest_presentation_time: {self.earliest_presentation_time}",)
        repl += (f"first_offset: {self.first_offset}",)
        repl += (f"reserved: {self.reserved}",)
        for idx, val in self.references:
            repl += (f"reference[{idx}].reference_type: {val.reference_type}",)
            repl += (f"reference[{idx}].reference_size: {val.reference_size}",)
            repl += (f"reference[{idx}].starts_with_SAP: {val.starts_with_SAP}",)
            repl += (f"reference[{idx}].SAP_type: {val.SAP_type}",)
            repl += (f"reference[{idx}].SAP_delta_time: {val.SAP_delta_time}",)
        return super().repr(repl)
