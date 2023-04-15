# -*- coding: utf-8 -*-
from .box import Box
from .box import read_bytes


# ISO/IEC 14496-12:2022, Section 8.1.2
class FreeBox(Box):
    box_type = b"free"
    is_mandatory = False

    def read(self, file):
        max_len = self.get_max_offset() - file.tell()
        self.contents = read_bytes(file, max_len)

    def __repr__(self):
        repl = ()
        if self.debug > 2:
            repl += (f'contents: "{self.contents}"',)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.1.2
class SkipBox(FreeBox):
    box_type = b"skip"
