# -*- coding: utf-8 -*-
from .box import Box
from .box import read_uint
from .box import read_sint
from .box import ntohl
from .box import ntohs
from .stbl import AudioSampleEntry


# https://github.com/xiph/flac/blob/master/doc/isoflac.txt, Section 3.3.2
class FlacMetadataBlock(object):
    block_data = []

    def __init__(self, max_offset):
        self.max_offset = max_offset

    def read(self, file):
        byte = read_uint(file, 1)
        self.last_metadata_block_flag = byte >> 7
        self.block_type = byte & 0x7F
        length = read_uint(file, 3)
        for _ in range(length):
            self.block_data.append(read_uint(file, 1))

    def contents(self):
        tuples = ()
        tuples += (("last_metadata_block_flag", self.last_metadata_block_flag),)
        tuples += (("block_type", self.block_type),)
        for idx, val in enumerate(self.block_data):
            tuples += ((f"block[{idx}]", val),)
        return tuples


class FlacSpecificBox(Box):
    box_type = b"dfLa"
    metadata_blocks = []

    def read(self, file):
        while file.tell() < self.get_max_offset():
            metadata_block = FlacMetadataBlock(max_offset=self.get_max_offset())
            metadata_block.read(file)
            self.metadata_blocks.append(metadata_block)

    def contents(self):
        tuples = super().contents()
        for idx, val in enumerate(self.metadata_blocks):
            tuples += ((f"metadata_block[{idx}]", val.contents()),)
        return tuples


# https://github.com/xiph/flac/blob/master/doc/isoflac.txt, Section 3.3.1
class FlacSampleEntry(AudioSampleEntry):
    box_type = b"fLaC"
