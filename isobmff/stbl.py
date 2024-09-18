# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import ContainerBox
from .box import Quantity
from .utils import read_uint, read_sint
from .utils import read_fixed_size_string
from .utils import read_utf8string


# ISO/IEC 14496-12:2022, Section 8.5.1.1
class SampleTableBox(ContainerBox):
    box_type = b"stbl"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE


# ISO/IEC 14496-12:2022, Section 8.5.2.2
class SampleEntry(Box):
    def read(self, file):
        self.reserved0 = []
        for _ in range(6):
            reserved = read_uint(file, 1)
            self.reserved0.append(reserved)
        self.data_reference_index = read_uint(file, 2)

    def contents(self):
        tuples = super().contents()
        for idx, val in enumerate(self.reserved0):
            tuples += ((f"reserved0[{idx}]", val),)
        tuples += (("data_reference_index", self.data_reference_index),)
        return tuples


# ISO/IEC 14496-12:2022, Section 8.5.2.2
class BitRateBox(Box):
    box_type = b"btrt"

    def read(self, file):
        self.buffer_size_db = read_uint(file, 4)
        self.max_bitrate = read_uint(file, 4)
        self.avg_bitrate = read_uint(file, 4)

    def contents(self):
        tuples = super().contents()
        tuples += (("buffer_size_db", self.buffer_size_db),)
        tuples += (("max_bitrate", self.max_bitrate),)
        tuples += (("avg_bitrate", self.avg_bitrate),)
        return tuples


# ISO/IEC 14496-12:2022, Section 8.5.2.2
class SampleDescriptionBox(FullBox):
    box_type = b"stsd"
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE

    def read(self, file):
        entry_count = read_uint(file, 4)
        self.samples = []
        for _ in range(entry_count):
            box = self.read_box(file)
            if not box:
                break
            self.samples.append(box)

    def contents(self):
        tuples = super().contents()
        for idx, box in enumerate(self.samples):
            tuples += ((f"box[{idx}]", box.contents()),)
        return tuples


# ISO/IEC 14496-12:2022, Section 12.1.3.2
# ISO/IEC 14496-14:2020, Section 6.7.2
class VisualSampleEntry(SampleEntry):
    def read(self, file):
        super().read(file)
        self.pre_defined1 = read_uint(file, 2)
        self.reserved1 = read_uint(file, 2)
        self.pre_defined2 = []
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

    def contents(self):
        tuples = super().contents()
        tuples += (("pre_defined1", self.pre_defined1),)
        tuples += (("reserved1", self.reserved1),)
        for idx, val in enumerate(self.pre_defined2):
            tuples += ((f"pre_defined2[{idx}]", val),)
        tuples += (("width", self.width),)
        tuples += (("height", self.height),)
        tuples += (("horizresolution", f"0x{self.horizresolution:08x}"),)
        tuples += (("vertresolution", f"0x{self.vertresolution:08x}"),)
        tuples += (("reserved2", self.reserved2),)
        tuples += (("frame_count", self.frame_count),)
        tuples += (("compressorname", self.compressorname.strip()),)
        tuples += (("depth", f"0x{self.depth:04x}"),)
        tuples += (("pre_defined3", self.pre_defined3),)
        for idx, box in enumerate(self.box_list):
            tuples += ((f"box[{idx}]", box.contents()),)
        return tuples


# ISO/IEC 14496-12:2022, Section 12.2.3.2
# ISO/IEC 14496-14:2020, Section 6.7.2
class AudioSampleEntry(SampleEntry):
    def read(self, file):
        super().read(file)
        self.reserved1 = []
        for _ in range(2):
            self.reserved1.append(read_uint(file, 4))
        self.channelcount = read_uint(file, 2)
        self.samplesize = read_uint(file, 2)
        self.pre_defined = read_uint(file, 2)
        self.reserved2 = read_uint(file, 2)
        self.samplerate = read_uint(file, 4)
        # parse the boxes
        self.box_list = self.read_box_list(file)

    def contents(self):
        tuples = super().contents()
        for idx, val in enumerate(self.reserved1):
            tuples += ((f"reserved1[{idx}]", val),)
        tuples += (("channelcount", self.channelcount),)
        tuples += (("samplesize", self.samplesize),)
        tuples += (("pre_defined", self.pre_defined),)
        tuples += (("reserved2", self.reserved2),)
        tuples += (("samplerate", self.samplerate >> 16),)
        for idx, box in enumerate(self.box_list):
            tuples += ((f"box[{idx}]", box.contents()),)
        return tuples


# ISO/IEC 14496-12:2022, Section 12.3.3.2
class MetaDataSampleEntry(SampleEntry):
    pass


# ISO/IEC 14496-12:2022, Section 12.3.3.2
class XMLMetaDataSampleEntry(MetaDataSampleEntry):
    box_type = b"metx"

    def read(self, file):
        super().read(file)
        max_len = self.max_offset - file.tell()
        self.content_encoding = read_utf8string(file, max_len)
        # TODO(chema): utf8list here
        max_len = self.max_offset - file.tell()
        self.namespace = read_utf8string(file, max_len)
        # TODO(chema): utf8list here
        max_len = self.max_offset - file.tell()
        self.schema_location = read_utf8string(file, max_len)

    def contents(self):
        tuples = super().contents()
        tuples += (("content_encoding", self.content_encoding),)
        tuples += (("namespace", self.namespace),)
        tuples += (("schema_location", self.schema_location),)
        return tuples


# ISO/IEC 14496-12:2022, Section 12.3.3.2
class TextConfigBox(FullBox):
    box_type = b"txtC"

    def read(self, file):
        super().read(file)
        max_len = self.max_offset - file.tell()
        self.text_config = read_utf8string(file, max_len)

    def contents(self):
        tuples = super().contents()
        tuples += (("text_config", self.text_config_box.contents()),)
        return tuples


# ISO/IEC 14496-12:2022, Section 12.3.3.2
class TextMetaDataSampleEntry(MetaDataSampleEntry):
    box_type = b"mett"

    def read(self, file):
        super().read(file)
        max_len = self.max_offset - file.tell()
        self.content_encoding = read_utf8string(file, max_len)
        max_len = self.max_offset - file.tell()
        self.mime_format = read_utf8string(file, max_len)
        self.box_list = self.read_box_list(file)

    def contents(self):
        tuples = super().contents()
        tuples += (("content_encoding", self.content_encoding),)
        tuples += (("mime_format", self.mime_format),)
        for idx, box in enumerate(self.box_list):
            tuples += ((f"box[{idx}]", box.contents()),)
        return tuples


# ISO/IEC 14496-12:2022, Section 12.3.3.2
class MimeBox(FullBox):
    box_type = b"mime"

    def read(self, file):
        super().read(file)
        max_len = self.max_offset - file.tell()
        self.content_type = read_utf8string(file, max_len)

    def contents(self):
        tuples = super().contents()
        tuples += (("content_type", self.content_type),)
        return tuples


# ISO/IEC 14496-12:2022, Section 12.3.3.2
class URIBox(FullBox):
    box_type = b"uri "

    def __init__(self, max_offset):
        self.max_offset = max_offset

    def read(self, file):
        super().read(file)
        max_len = self.max_offset - file.tell()
        self.the_uri = read_utf8string(file, max_len)

    def contents(self):
        tuples = super().contents()
        tuples += (("the_uri", self.the_uri),)
        return tuples


# ISO/IEC 14496-12:2022, Section 12.3.3.2
class URIInitBox(FullBox):
    box_type = b"uriI"

    def __init__(self, max_offset):
        self.max_offset = max_offset

    def read(self, file):
        super().read(file)
        max_len = self.max_offset - file.tell()
        self.uri_initialization_data = self.read_as_bytes(file)

    def contents(self):
        tuples = super().contents()
        tuples += (("uri_initialization_data", self.uri_initialization_data),)
        return tuples


# ISO/IEC 14496-12:2022, Section 12.3.3.2
class URIMetaSampleEntry(MetaDataSampleEntry):
    box_type = b"urim"

    def read(self, file):
        super().read(file)
        self.uri_box = URIBox(max_offset=self.max_offset)
        self.uri_box.read(file)
        self.init = URIInitBox(max_offset=self.max_offset)
        self.init.read(file)

    def contents(self):
        tuples = super().contents()
        tuples += (("uri_box", self.uri_box),)
        tuples += (("init", self.init),)
        return tuples


# ISO/IEC 14496-12:2022, Section 12.4.4.2
# ISO/IEC 14496-14:2020, Section 6.7.2
class HintSampleEntry(SampleEntry):
    pass


# ISO/IEC 14496-12:2022, Section 12.5.3.2
class PlainTextSampleEntry(SampleEntry):
    pass


# ISO/IEC 14496-12:2022, Section 12.5.3.2
class SimpleTextSampleEntry(PlainTextSampleEntry):
    box_type = b"stxt"
    text_config_box = None

    def read(self, file):
        super().read(file)
        max_len = self.max_offset - file.tell()
        self.content_encoding = read_utf8string(file, max_len)
        max_len = self.max_offset - file.tell()
        self.mime_format = read_utf8string(file, max_len)
        if file.tell() < self.max_offset:
            self.text_config_box = self.read_box(file)

    def contents(self):
        tuples = super().contents()
        tuples += (("content_encoding", self.content_encoding),)
        tuples += (("mime_format", self.mime_format),)
        if self.text_config_box is not None:
            tuples += (("text_config_box", self.text_config_box.contents()),)
        return tuples


# ISO/IEC 14496-12:2022, Section 12.6.3.2
class SubtitleSampleEntry(SampleEntry):
    pass


# ISO/IEC 14496-12:2022, Section 12.6.3.2
class XMLSubtitleSampleEntry(SubtitleSampleEntry):
    box_type = b"stpp"

    def read(self, file):
        super().read(file)
        # TODO(chema): utf8list here
        max_len = self.max_offset - file.tell()
        self.namespace = read_utf8string(file, max_len)
        # TODO(chema): utf8list here
        max_len = self.max_offset - file.tell()
        self.schema_location = read_utf8string(file, max_len)
        # TODO(chema): utf8list here
        max_len = self.max_offset - file.tell()
        self.auxiliary_mime_types = read_utf8string(file, max_len)

    def contents(self):
        tuples = super().contents()
        tuples += (("namespace", self.namespace),)
        tuples += (("schema_location", self.schema_location),)
        tuples += (("auxiliary_mime_types", self.auxiliary_mime_types),)
        return tuples


# ISO/IEC 14496-12:2022, Section 12.6.3.2
class TextSubtitleSampleEntry(SubtitleSampleEntry):
    box_type = b"sbtt"

    def read(self, file):
        super().read(file)
        max_len = self.max_offset - file.tell()
        self.content_encoding = read_utf8string(file, max_len)
        max_len = self.max_offset - file.tell()
        self.mime_format = read_utf8string(file, max_len)
        if file.tell() < self.max_offset:
            self.text_config_box = self.read_box(file)

    def contents(self):
        tuples = super().contents()
        tuples += (("content_encoding", self.content_encoding),)
        tuples += (("mime_format", self.mime_format),)
        if self.text_config_box is not None:
            tuples += (("text_config_box", self.text_config_box.contents()),)
        return tuples
