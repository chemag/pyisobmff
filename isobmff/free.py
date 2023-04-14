# -*- coding: utf-8 -*-
from .box import Box

# ISO/IEC 14496-12:2022, Section 8.1.2
class FreeBox(Box):
    box_type = "free"
    is_mandatory = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.contents = None

    def __repr__(self):
        repl = ()
        repl += (f'contents: "{self.contents}"',)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.1.2
class SkipBox(FreeBox):
    box_type = "skip"
