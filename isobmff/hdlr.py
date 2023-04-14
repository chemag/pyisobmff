# -*- coding: utf-8 -*-
from .box import FullBox
from .box import Quantity
from .box import read_uint
from .box import read_fixed_size_string
from .box import read_utf8string


# ISO/IEC 14496-12:2022, Section 8.4.3
class HandlerReferenceBox(FullBox):
    box_type = "hdlr"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pre_defined = None
        self.handler_type = None
        self.reserved = []
        self.name = None

    def __repr__(self):
        repl = ()
        repl += (f"handler_type: {self.handler_type}",)
        repl += (f'name: "{self.name}"',)
        return super().repr(repl)

    def read(self, file):
        self.pre_defined = read_uint(file, 4)
        self.handler_type = read_fixed_size_string(file, 4)
        for _ in range(3):  # 3*4=12bytes
            self.reserved.append(read_uint(file, 4))
        max_len = self.get_max_offset() - file.tell()
        self.name = read_utf8string(file, max_len)
