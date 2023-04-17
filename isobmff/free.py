# -*- coding: utf-8 -*-
from .box import Box


# ISO/IEC 14496-12:2022, Section 8.1.2
class FreeBox(Box):
    box_type = b"free"
    is_mandatory = False

    def read(self, file):
        self.read_as_bytes(file)

    def __repr__(self):
        repl = ()
        if self.debug > 2:
            repl += (f'contents: "{self.contents}"',)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.1.2
class SkipBox(FreeBox):
    box_type = b"skip"
