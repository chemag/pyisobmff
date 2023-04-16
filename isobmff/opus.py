# -*- coding: utf-8 -*-
from .box import Box
from .box import read_uint
from .box import read_sint
from .box import ntohl
from .box import ntohs


# https://opus-codec.org/docs/opus_in_isobmff.html, Section 4.3.2
class OpusSpecificBox(Box):
    box_type = b"dOps"
    channel_mappings = []

    def read(self, file):
        self.version = read_uint(file, 1)
        self.output_channel_count = read_uint(file, 1)
        self.preskip = read_uint(file, 2)
        self.input_sample_rate = read_uint(file, 4)
        self.output_gain = read_sint(file, 2)
        self.channel_mapping_family = read_uint(file, 1)
        if self.channel_mapping_family != 0:
            channel_mapping = {}
            channel_mapping["stream_count"] = read_uint(file, 1)
            channel_mapping["coupled_count"] = read_uint(file, 1)
            channel_mapping["channel_mapping"] = read_uint(
                file, self.output_channel_count
            )

    def __repr__(self):
        repl = ()
        repl += (f"version: {self.version}",)
        repl += (f"output_channel_count: {self.output_channel_count}",)
        repl += (f"preskip: {ntohs(self.preskip)}",)
        repl += (f"input_sample_rate: {ntohl(self.input_sample_rate)}",)
        repl += (f"output_gain: {self.output_gain}",)
        repl += (f"channel_mapping_family: {self.channel_mapping_family}",)
        for idx, val in enumerate(self.channel_mappings):
            repl += (f'channel_mapping[{idx}]["stream_count"]: {val["stream_count"]}',)
            repl += (
                f'channel_mapping[{idx}]["coupled_count"]: {val["coupled_count"]}',
            )
            repl += (
                f'channel_mapping[{idx}]["channel_mapping"]: {val["channel_mapping"]}',
            )
        return super().repr(repl)
