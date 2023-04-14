# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_box
from .box import read_uint


# ISO/IEC 14496-12:2022, Section 8.8.6
class TrackFragmentBox(Box):
    box_type = "traf"
    box_list = []

    def read(self, file):
        while file.tell() < self.get_max_offset():
            box = read_box(file, self.debug)
            self.box_list.append(box)

    def __repr__(self):
        repl = ()
        for box in self.box_list:
            repl += (repr(box),)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.8.7
class TrackFragmentHeaderBox(FullBox):
    box_type = "tfhd"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE
    FLAGS = {
        "base-data-offset-present": 0x000001,
        "sample-description-index-present": 0x000002,
        "default-sample-duration-present": 0x000008,
        "default-sample-size-present": 0x000010,
        "default-sample-flags-present": 0x000020,
        "duration-is-empty": 0x010000,
    }

    def read(self, file):
        self.track_id = read_uint(file, 4)
        if (self.flags & self.FLAGS["base-data-offset-present"]) == self.FLAGS[
            "base-data-offset-present"
        ]:
            self.base_data_offset = read_uint(file, 8)
        if (self.flags & self.FLAGS["sample-description-index-present"]) == self.FLAGS[
            "sample-description-index-present"
        ]:
            self.sample_description_index = read_uint(file, 4)
        if (self.flags & self.FLAGS["default-sample-duration-present"]) == self.FLAGS[
            "default-sample-duration-present"
        ]:
            self.default_sample_duration = read_uint(file, 4)
        if (self.flags & self.FLAGS["default-sample-size-present"]) == self.FLAGS[
            "default-sample-size-present"
        ]:
            self.default_sample_size = read_uint(file, 4)
        if (self.flags & self.FLAGS["default-sample-flags-present"]) == self.FLAGS[
            "default-sample-flags-present"
        ]:
            self.default_sample_flags = read_uint(file, 4)

    def __repr__(self):
        repl = ()
        repl += (f"track_id: {self.track_id}",)
        if (self.flags & self.FLAGS["base-data-offset-present"]) == self.FLAGS[
            "base-data-offset-present"
        ]:
            repl += (f"base_data_offset: {self.base_data_offset}",)
        if (self.flags & self.FLAGS["sample-description-index-present"]) == self.FLAGS[
            "sample-description-index-present"
        ]:
            repl += (f"sample_description_index: {self.sample_description_index}",)
        if (self.flags & self.FLAGS["default-sample-duration-present"]) == self.FLAGS[
            "default-sample-duration-present"
        ]:
            repl += (f"default_sample_duration: {self.default_sample_duration}",)
        if (self.flags & self.FLAGS["default-sample-size-present"]) == self.FLAGS[
            "default-sample-size-present"
        ]:
            repl += (f"default_sample_size: {self.default_sample_size}",)
        if (self.flags & self.FLAGS["default-sample-flags-present"]) == self.FLAGS[
            "default-sample-flags-present"
        ]:
            repl += (f"default_sample_flags: {self.default_sample_flags}",)
        return super().repr(repl)
