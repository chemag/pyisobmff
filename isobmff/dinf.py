# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_box
from .box import read_int
from .box import read_string


# ISO/IEC 14496-12:2022, Section 8.7.1.2
class DataInformationBox(Box):
    box_type = "dinf"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE
    box_list = []

    def read(self, file):
        offset = file.tell()
        max_offset = offset + self.get_payload_size()
        while file.tell() < max_offset:
            box = read_box(file)
            self.box_list.append(box)

    def __repr__(self):
        repl = ()
        for box in self.box_list:
            repl += (repr(box),)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.7.2.2
class DataReferenceBox(FullBox):
    box_type = "dref"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE
    data_entry = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def read(self, file):
        entry_count = read_int(file, 4)
        for _ in range(entry_count):
            box = read_box(file)
            if not box:
                break
            self.data_entry.append(box)

    def __repr__(self):
        repl = ()
        for box in self.data_entry:
            repl += (repr(box),)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.7.2.2
class DataEntryUrlBox(FullBox):
    box_type = "url "
    is_mandatory = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.location = None

    def read(self, file):
        offset = file.tell()
        max_offset = offset + self.get_payload_size()
        max_length = max_offset - offset
        self.location = read_string(file, max_length)

    def __repr__(self):
        repl = ()
        repl += (f'location: "{self.location}"',)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.7.2.2
class DataEntryUrnBox(FullBox):
    box_type = "urn "
    is_mandatory = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = None
        self.location = None

    def read(self, file):
        self.name = read_string(file)
        self.location = read_string(file)

    def __repr__(self):
        repl = ()
        repl += (f'name: "{self.name}"',)
        repl += (f'location: "{self.location}"',)
        return super().repr(repl)
