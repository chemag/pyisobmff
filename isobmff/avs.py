# -*- coding: utf-8 -*-
from .box import Box
from .box import read_box
from .box import read_uint
from .box import read_bytes
from .stbl import VisualSampleEntry


# IEEE 1857.3-2013, Section 4.2.3.3.1
class AvsSampleEntry(VisualSampleEntry):
    box_type = b"avs2"

    def read(self, file):
        super().read(file)
        self.config = read_box(file, self.debug)

    def __repr__(self):
        repl = ()
        repl += (f"config: {self.config}",)
        return super().repr(repl)


# IEEE 1857.3-2013, Section 4.2.3.3.1
class AvsSequenceInfoBox(Box):
    box_type = b"avss"

    def read(self, file):
        self.avs_config = AVSDecoderConfigurationRecord(
            max_offset=self.get_max_offset()
        )
        self.avs_config.read(file)

    def __repr__(self):
        repl = ()
        repl += (f"avs_config: {self.avs_config}",)
        return super().repr(repl)


# IEEE 1857.3-2013, Section 4.2.3.3.1
class AVSDecoderConfigurationRecord(object):
    sequence_header_nal_units = []

    def __init__(self, max_offset):
        self.max_offset = max_offset

    def read(self, file):
        if file.tell() >= self.max_offset:
            # out of data in the box: let's punt here
            self.reserved1 = None
            return
        self.configurationVersion = read_uint(file, 1)
        self.AVSProfileIndication = read_uint(file, 1)
        self.AVSLevelIndication = read_uint(file, 1)
        byte3 = read_uint(file, 1)
        self.reserved1 = (byte3 >> 2) & 0x3F
        self.lengthSizeMinusOne = byte3 & 0x03
        byte4 = read_uint(file, 1)
        self.reserved2 = (byte4 >> 5) & 0x07
        numOfSequenceHeader = byte4 & 0x1F
        for _ in range(numOfSequenceHeader):
            # ensure there are enough bytes for a next reading
            if file.tell() >= self.max_offset:
                # TODO(chema): early stop
                break
            sequenceHeaderLength = read_uint(file, 2)
            self.sequence_header_nal_units.append(
                read_bytes(file, sequenceHeaderLength)
            )

    def __repr__(self):
        repl = ()
        if self.reserved1 is None:
            return "\n".join(repl)
        repl += (f"configurationVersion: {self.configurationVersion}",)
        repl += (f"AVSProfileIndication: {self.AVSProfileIndication}",)
        repl += (f"AVSLevelIndication: {self.AVSLevelIndication}",)
        repl += (f"reserved1: {bin(self.reserved1)}",)
        repl += (f"lengthSizeMinusOne: {self.lengthSizeMinusOne}",)
        repl += (f"reserved2: {bin(self.reserved2)}",)
        for idx, val in enumerate(self.sequence_header_nal_units):
            repl += (f'sequence_header_nal_unit[{idx}]: "{val}"',)
        return "\n".join(repl)


# IEEE 1857.3-2013, Section 6.2.3.3.1
# class Av31ConfigurationBox(Box):
# box_type = b"av3c"
# IEEE 1857.3-2013, Section 6.2.3.3.1
# class Av31SampleEntry(AudioSampleEntry):
# box_type = b"av31"