# -*- coding: utf-8 -*-
from .box import Box
from .box import read_int


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
