# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .utils import read_uint
from .utils import read_sint


# ISO/IEC 14496-12:2022, Section 8.8.6
class TrackFragmentBox(Box):
    box_type = b"traf"

    def read(self, file):
        self.box_list = self.read_box_list(file)

    def contents(self):
        tuples = super().contents()
        for idx, box in enumerate(self.box_list):
            tuples += ((f"box[{idx}]", box.contents()),)
        return tuples


# ISO/IEC 14496-12:2022, Section 8.8.7
class TrackFragmentHeaderBox(FullBox):
    box_type = b"tfhd"
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

    def contents(self):
        tuples = super().contents()
        tuples += (("track_id", self.track_id),)
        if (self.flags & self.FLAGS["base-data-offset-present"]) == self.FLAGS[
            "base-data-offset-present"
        ]:
            tuples += (("base_data_offset", self.base_data_offset),)
        if (self.flags & self.FLAGS["sample-description-index-present"]) == self.FLAGS[
            "sample-description-index-present"
        ]:
            tuples += (("sample_description_index", self.sample_description_index),)
        if (self.flags & self.FLAGS["default-sample-duration-present"]) == self.FLAGS[
            "default-sample-duration-present"
        ]:
            tuples += (("default_sample_duration", self.default_sample_duration),)
        if (self.flags & self.FLAGS["default-sample-size-present"]) == self.FLAGS[
            "default-sample-size-present"
        ]:
            tuples += (("default_sample_size", self.default_sample_size),)
        if (self.flags & self.FLAGS["default-sample-flags-present"]) == self.FLAGS[
            "default-sample-flags-present"
        ]:
            tuples += (("default_sample_flags", self.default_sample_flags),)
        return tuples


# ISO/IEC 14496-12:2022, Section 8.8.8
class TrackRunBox(FullBox):
    box_type = b"trun"
    FLAGS = {
        "data-offset-present": 0x000001,
        "first-sample-flags-present": 0x000004,
        "sample-duration-present": 0x000100,
        "sample-size-present": 0x000200,
        "sample-flags-present": 0x000400,
        "sample-composition-time-offsets-present": 0x000800,
    }

    def read(self, file):
        sample_count = read_uint(file, 4)
        if (self.flags & self.FLAGS["data-offset-present"]) == self.FLAGS[
            "data-offset-present"
        ]:
            self.data_offset = read_sint(file, 8)
        if (self.flags & self.FLAGS["first-sample-flags-present"]) == self.FLAGS[
            "first-sample-flags-present"
        ]:
            self.first_sample_flags = read_uint(file, 4)
        self.samples = []
        for _ in range(sample_count):
            sample = {}
            if (self.flags & self.FLAGS["sample-duration-present"]) == self.FLAGS[
                "sample-duration-present"
            ]:
                sample["sample_duration"] = read_uint(file, 4)
            if (self.flags & self.FLAGS["sample-size-present"]) == self.FLAGS[
                "sample-size-present"
            ]:
                sample["sample_size"] = read_uint(file, 4)
            if (self.flags & self.FLAGS["sample-flags-present"]) == self.FLAGS[
                "sample-flags-present"
            ]:
                sample["sample_flags"] = read_uint(file, 4)
            if (
                self.flags & self.FLAGS["sample-composition-time-offsets-present"]
            ) == self.FLAGS["sample-composition-time-offsets-present"]:
                if self.version == 0:
                    sample["sample_composition_time_offset"] = read_uint(file, 4)
                else:
                    sample["sample_composition_time_offset"] = read_sint(file, 4)
            self.samples.append(sample)
        # skip the remaining data
        # TODO: this should be centralized
        file.seek(self.max_offset)

    def contents(self):
        tuples = super().contents()
        if (self.flags & self.FLAGS["data-offset-present"]) == self.FLAGS[
            "data-offset-present"
        ]:
            tuples += (("data_offset", self.data_offset),)
        if (self.flags & self.FLAGS["first-sample-flags-present"]) == self.FLAGS[
            "first-sample-flags-present"
        ]:
            tuples += (("first_sample_flags", self.first_sample_flags),)
        if self.debug > 2:
            for idx, val in enumerate(self.samples):
                if (self.flags & self.FLAGS["sample-duration-present"]) == self.FLAGS[
                    "sample-duration-present"
                ]:
                    tuples += (
                        (f'samples[{idx}]["sample_duration"]', val["sample_duration"]),
                    )
                if (self.flags & self.FLAGS["sample-size-present"]) == self.FLAGS[
                    "sample-size-present"
                ]:
                    tuples += ((f'samples[{idx}]["sample_size"]', val["sample_size"]),)
                if (self.flags & self.FLAGS["sample-flags-present"]) == self.FLAGS[
                    "sample-flags-present"
                ]:
                    tuples += (
                        (f'samples[{idx}]["sample_flags"]', val["sample_flags"]),
                    )
                if (
                    self.flags & self.FLAGS["sample-composition-time-offsets-present"]
                ) == self.FLAGS["sample-composition-time-offsets-present"]:
                    tuples += (
                        (
                            f'samples[{idx}]["sample_composition_time_offset"]',
                            val["sample_composition_time_offset"],
                        ),
                    )
        return tuples


# ISO/IEC 14496-12:2022, Section 8.8.12
class TrackFragmentBaseMediaDecodeTimeBox(FullBox):
    box_type = b"tfdt"

    def read(self, file):
        if self.version == 1:
            self.baseMediaDecodeTime = read_uint(file, 8)
        else:
            self.baseMediaDecodeTime = read_uint(file, 4)

    def contents(self):
        tuples = super().contents()
        tuples += (("baseMediaDecodeTime", self.baseMediaDecodeTime),)
        return tuples
