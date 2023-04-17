# -*- coding: utf-8 -*-
from .box import FullBox
from .box import Quantity


# ISO/IEC 14496-12:2022, Section 8.11.1.1
# Page 80: "The MetaBox is unusual in that it is a container box
# yet extends FullBox, not Box."
class MetaBox(FullBox):
    box_type = b"meta"
    is_mandatory = False
    quantity = Quantity.ZERO_OR_ONE
    box_list = []

    def read(self, file):
        while file.tell() < self.get_max_offset():
            if not self.box_list:
                if file.peek()[:4] == b"hdlr":
                    # This is a relatively common issue on isobmff streams
                    # where the MetaBox is actually a Box, not a FullBox.
                    # This means we read the FullBox flags and version
                    # fields incorrectly (from the hdlr box size field).
                    # We need to:
                    # (1) reset the flags and version fields.
                    self.version = 0
                    self.flags = 0
                    # (2) seek back the wrongly-read 4x bytes.
                    file.seek(file.tell() - 4)
                    # example: videolan/samples/mov/editlist/20210910_114302.mp4
                else:
                    # Well-defined stream: keep reading
                    pass
            box = self.read_box(file)
            if box is None:
                break
            self.box_list.append(box)

    def __repr__(self):
        repl = ()
        for box in self.box_list:
            repl += (repr(box),)
        return super().repr(repl)
