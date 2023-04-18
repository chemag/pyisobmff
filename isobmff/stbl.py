# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import ContainerBox
from .box import Quantity
from .box import read_uint, read_sint
from .box import read_fixed_size_string
from .box import read_utf8string


# ISO/IEC 14496-12:2022, Section 8.5.1.1
class SampleTableBox(ContainerBox):
    box_type = b"stbl"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE


# ISO/IEC 14496-12:2022, Section 8.5.2.2
class SampleEntry(Box):
    reserved0 = []

    def read(self, file):
        for _ in range(6):
            reserved = read_uint(file, 1)
            self.reserved0.append(reserved)
        self.data_reference_index = read_uint(file, 2)

    def repr(self, repl=None):
        new_repl = ()
        for idx, val in enumerate(self.reserved0):
            new_repl += (f"reserved0[{idx}]: {val}",)
        new_repl += (f"data_reference_index: {self.data_reference_index}",)
        if repl is not None:
            new_repl += repl
        return super().repr(new_repl)

    def __repr__(self):
        return self.repr()


# ISO/IEC 14496-12:2022, Section 8.5.2.2
class BitRateBox(Box):
    box_type = b"btrt"

    def read(self, file):
        self.buffer_size_db = read_uint(file, 4)
        self.max_bitrate = read_uint(file, 4)
        self.avg_bitrate = read_uint(file, 4)

    def __repr__(self):
        repl = ()
        repl += (f"buffer_size_db: {self.buffer_size_db}",)
        repl += (f"max_bitrate: {self.max_bitrate}",)
        repl += (f"avg_bitrate: {self.avg_bitrate}",)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 8.5.2.2
class SampleDescriptionBox(FullBox):
    box_type = b"stsd"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE
    samples = []

    def read(self, file):
        entry_count = read_uint(file, 4)
        for _ in range(entry_count):
            box = self.read_box(file)
            if not box:
                break
            self.samples.append(box)

    def __repr__(self):
        repl = ()
        for box in self.samples:
            repl += (repr(box),)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 12.1.3.2
# ISO/IEC 14496-14:2020, Section 6.7.2
class VisualSampleEntry(SampleEntry):
    box_type = b"vide"
    box_list = []
    pre_defined2 = []

    def read(self, file):
        super().read(file)
        self.pre_defined1 = read_uint(file, 2)
        self.reserved1 = read_uint(file, 2)
        for _ in range(3):
            self.pre_defined2.append(read_uint(file, 4))
        self.width = read_uint(file, 2)
        self.height = read_uint(file, 2)
        self.horizresolution = read_uint(file, 4)
        self.vertresolution = read_uint(file, 4)
        self.reserved2 = read_uint(file, 4)
        self.frame_count = read_uint(file, 2)
        self.compressorname = read_fixed_size_string(file, 32)
        self.depth = read_uint(file, 2)
        self.pre_defined3 = read_sint(file, 2)
        self.box_list = self.read_box_list(file)

    def repr(self, repl=None):
        new_repl = ()
        new_repl += (f"pre_defined1: {self.pre_defined1}",)
        new_repl += (f"reserved1: {self.reserved1}",)
        for idx, val in enumerate(self.pre_defined2):
            new_repl += (f"pre_defined2[{idx}]: {val}",)
        new_repl += (f"width: {self.width}",)
        new_repl += (f"height: {self.height}",)
        new_repl += (f"horizresolution: 0x{self.horizresolution:08x}",)
        new_repl += (f"vertresolution: 0x{self.vertresolution:08x}",)
        new_repl += (f"reserved2: {self.reserved2}",)
        new_repl += (f"frame_count: {self.frame_count}",)
        new_repl += (f'compressorname: "{self.compressorname.strip()}"',)
        new_repl += (f"depth: 0x{self.depth:04x}",)
        new_repl += (f"pre_defined3: {self.pre_defined3}",)
        for box in self.box_list:
            new_repl += (repr(box),)
        if repl is not None:
            new_repl += repl
        return super().repr(new_repl)

    def __repr__(self):
        return self.repr()


# ISO/IEC 14496-12:2022, Section 12.2.3.2
# ISO/IEC 14496-14:2020, Section 6.7.2
class AudioSampleEntry(SampleEntry):
    box_type = b"soun"
    box_list = []
    reserved1 = []

    def read(self, file):
        super().read(file)
        for _ in range(2):
            self.reserved1.append(read_uint(file, 4))
        self.channelcount = read_uint(file, 2)
        self.samplesize = read_uint(file, 2)
        self.pre_defined = read_uint(file, 2)
        self.reserved2 = read_uint(file, 2)
        self.samplerate = read_uint(file, 4)
        # parse the boxes
        self.box_list = self.read_box_list(file)

    def repr(self, repl=None):
        new_repl = ()
        for idx, val in enumerate(self.reserved1):
            new_repl += (f"reserved1[{idx}]: {val}",)
        new_repl += (f"channelcount: {self.channelcount}",)
        new_repl += (f"samplesize: {self.samplesize}",)
        new_repl += (f"pre_defined: {self.pre_defined}",)
        new_repl += (f"reserved2: {self.reserved2}",)
        new_repl += (f"samplerate: {self.samplerate >> 16}",)
        for box in self.box_list:
            new_repl += (repr(box),)
        if repl is not None:
            new_repl += repl
        return super().repr(new_repl)

    def __repr__(self):
        return self.repr()


# ISO/IEC 14496-12:2022, Section 8.5.2.2
class BitRateBox(Box):
    box_type = b"btrt"

    def read(self, file):
        self.buffer_size_db = read_uint(file, 4)
        self.max_bitrate = read_uint(file, 4)
        self.avg_bitrate = read_uint(file, 4)

    def __repr__(self):
        repl = ()
        repl += (f"buffer_size_db: {self.buffer_size_db}",)
        repl += (f"max_bitrate: {self.max_bitrate}",)
        repl += (f"avg_bitrate: {self.avg_bitrate}",)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 12.6
class SubtitleSampleEntry(SampleEntry):
    pass


# ISO/IEC 14496-12:2022, Section 12.6
class XMLSubtitleSampleEntry(SubtitleSampleEntry):
    box_type = b"stpp"

    def read(self, file):
        super().read(file)
        max_len = self.get_max_offset() - file.tell()
        self.namespace = read_utf8string(file, max_len)
        max_len = self.get_max_offset() - file.tell()
        self.schema_location = read_utf8string(file, max_len)
        max_len = self.get_max_offset() - file.tell()
        self.auxiliary_mime_types = read_utf8string(file, max_len)

    def repr(self, repl=None):
        new_repl = ()
        new_repl += (f"namespace: {self.namespace}",)
        new_repl += (f"schema_location: {self.schema_location}",)
        new_repl += (f"auxiliary_mime_types: {self.auxiliary_mime_types}",)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 12.3.3.2
class TextConfigBox(SubtitleSampleEntry):
    box_type = b"txtC"

    def read(self, file):
        super().read(file)
        max_len = self.get_max_offset() - file.tell()
        self.text_config = read_utf8string(file, max_len)

    def repr(self, repl=None):
        new_repl = ()
        new_repl += (f"text_config: {self.text_config}",)
        return super().repr(repl)


# ISO/IEC 14496-12:2022, Section 12.5.3.2
class PlainTextSampleEntry(SampleEntry):
    pass


# ISO/IEC 14496-12:2022, Section 12.5.3.2
class SimpleTextSampleEntry(PlainTextSampleEntry):
    box_type = b"stxt"
    text_config_box = None

    def read(self, file):
        super().read(file)
        max_len = self.get_max_offset() - file.tell()
        self.content_encoding = read_utf8string(file, max_len)
        max_len = self.get_max_offset() - file.tell()
        self.mime_format = read_utf8string(file, max_len)
        if file.tell() < self.get_max_offset():
            self.text_config_box = self.read_box(file)

    def repr(self, repl=None):
        new_repl = ()
        new_repl += (f"content_encoding: {self.content_encoding}",)
        new_repl += (f"mime_format: {self.mime_format}",)
        if self.text_config_box is not None:
            repl += (f"text_config_box: {self.text_config_box}",)
        return super().repr(repl)
