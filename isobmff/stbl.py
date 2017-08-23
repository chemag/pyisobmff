# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_box
from .box import read_int
from .box import read_string


class SampleTableBox(Box):
    """Movie Box
    """
    box_type = 'stbl'
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE

class SampleDescriptionBox(FullBox):
    """Sample Description Box
    """
    box_type = 'stsd'
    is_mandatory = True
    quantity = Quantity.EXACTLY_ONE    
    
    def __init__(self, size, version, flags):
        super().__init__(size=size, version=version, flags=flags)
        #self.handler_type = handler_type
        self.samples = []

    def read(self, file):
        entry_count = read_int(file, 4)
        for _ in range(entry_count):
            box = read_box(file)
            if not box:
                break
            self.samples.append(box)

class SampleEntry(Box):
    """Sample Entry
    """

    def __init__(self, size):
        super().__init__(size=size)
        self.reserveds = []
        self.data_reference_index = None

    def __repr__(self):
        rep = super().__repr__()
        return rep

    def get_box_size(self):
        """get box size excluding header"""
        return super().get_box_size() - 6 + 2    

    def read(self, file):
        for _ in range(6):
            reserved = read_int(file, 1)
            self.reserveds.append(reserved)
        self.data_reference_index = read_int(file, 2)


class HintSampleEntry(SampleEntry):
    """Hint Sample Entry
    """
    box_type = 'hint'

    def __init__(self, size):
        super().__init__(size=size)
        self.data = []

    def read(self, file):
        box_size = self.get_box_size()
        self.data = file.read(box_size)

class VisualSampleEntry(SampleEntry):
    """Visual Sample Entry
    """
    box_type = 'vide'

    def __init__(self, size):
        super().__init__(size=size)
        self.pre_defined1 = None
        self.reserved1 = None
        self.pre_defined2 = []
        self.width = None
        self.height = None
        self.horizresolution = None
        self.vertresolution = None
        self.reserved2 = None
        self.frame_count = None
        self.compressorname = None
        self.depth = None
        self.pre_defined3 = None
    
    def read(self, file):
        super().read(file)
        self.pre_defined1 = read_int(file, 2)
        self.reserved1 = read_int(file, 2)
        for _ in range(3):
            self.pre_defined2.append(read_int(file, 4))
        self.width = read_int(file, 2)
        self.height = read_int(file, 2)
        self.horizresolution = read_int(file, 4)
        self.vertresolution = read_int(file, 4)
        self.reserved2 = read_int(file, 4)
        self.frame_count = read_int(file, 2)
        self.compressorname = read_string(file, 32)
        self.depth = read_int(file, 2)
        self.pre_defined3 = read_int(file, 2)

class AudioSampleEntry(SampleEntry):
    """Audio Sample Entry"""
    box_type = 'soun'

    def __init__(self, size):
        super().__init__(size=size)
        self.reserved1 = []
        self.channelcount = None
        self.samplesize = None
        self.pre_defined = None
        self.reserved2 = []
        self.samperate = None
    
    def read(self, file):
        super().read(file)
        for _ in range(2):
            self.reserved1.append(read_int(file, 4))
        self.channelcount = read_int(file, 2)
        self.samplesize = read_int(file, 2)
        self.pre_defined = read_int(file, 2)
        for _ in range(2):
            self.reserved2.append(read_int(file, 2))
        self.samperate = read_int(file, 4)


class BitRateBox(Box):
    """Bit Rate Box"""
    box_type = 'btrt'

    def __init__(self, size):
        super().__init__(size=size)
        self.buffer_size_db = None
        self.max_bitrate = None
        self.avg_bitrate = None

    def read(self, file):
        self.buffer_size_db = read_int(file, 4)
        self.max_bitrate = read_int(file, 4)
        self.avg_bitrate = read_int(file, 4)
