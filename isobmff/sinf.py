# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_uint
from .box import read_utf8string


# ISO/IEC 14496-12:2022, Section 8.12.2
class ProtectionSchemeInfoBox(Box):
    box_type = "sinf"
    is_mandatory = False
    quantity = Quantity.ONE_OR_MORE


# ISO/IEC 14496-12:2022, Section 8.12.3
class OriginalFormatBox(Box):
    box_type = "frma"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE

    def read(self, file):
        self.data_format = read_uint(file, 4)

    def __repr__(self):
        repl = ()
        repl += (f"data_format: {self.data_format}",)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.12.6
class SchemeTypeBox(FullBox):
    box_type = "schm"
    is_mandatory = False
    quantity = Quantity.ZERO_OR_ONE

    def read(self, file):
        self.scheme_type = read_uint(file, 4)
        self.scheme_version = read_uint(file, 4)
        if self.flags & 0b1:
            max_len = self.get_max_offset() - file.tell()
            self.scheme_uri = read_utf8string(file, max_len)

    def __repr__(self):
        repl = ()
        repl += (f"scheme_type: {self.scheme_type}",)
        repl += (f"scheme_version: {self.scheme_version}",)
        repl += (f'scheme_uri: "{self.scheme_uri}"',)
        return super().repr(repl)


class SchemeInformationBox(Box):
    box_type = "schi"
    is_mandatory = False
    quantity = Quantity.ZERO_OR_ONE
