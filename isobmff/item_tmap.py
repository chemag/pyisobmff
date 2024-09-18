# -*- coding: utf-8 -*-
from .item import Item
from .utils import read_sint
from .utils import read_uint


# ISO/IEC 23008-12:2024 ???
# found definition in https://github.com/AOMediaCodec/libavif/commit/d142df6ca38e242239dbc2d972875bb6f92f41c5
class TmapItem(Item):
    item_type = b"tmap"

    def parse(self, fd):
        # just store the payload
        # unsigned int(8) version = 0;
        self.version = read_uint(fd, 1)
        # unsigned int(16) minimum_version = 0;
        self.minimum_version = read_uint(fd, 2)
        # unsigned int(16) writer_version;
        self.writer_version = read_uint(fd, 2)
        # unsigned int(1) is_multichannel;
        byte = read_uint(fd, 1)
        self.is_multichannel = byte >> 7
        # const uint8_t channelCount = is_multichannel ? 3 : 1;
        channelCount = 3 if (self.is_multichannel == 1) else 1
        # unsigned int(1) use_base_colour_space;
        self.use_base_colour_space = (byte >> 6) & 0x01
        # unsigned int(6) reserved;
        self.reserved = byte & 0x3F
        # unsigned int(32) base_hdr_headroom_numerator;
        self.base_hdr_headroom_numerator = read_uint(fd, 4)
        # unsigned int(32) base_hdr_headroom_denominator;
        self.base_hdr_headroom_denominator = read_uint(fd, 4)
        # unsigned int(32) alternate_hdr_headroom_numerator;
        self.alternate_hdr_headroom_numerator = read_uint(fd, 4)
        # unsigned int(32) alternate_hdr_headroom_denominator;
        self.alternate_hdr_headroom_denominator = read_uint(fd, 4)
        # per-channel info
        self.gain_map_min_numerator = []
        self.gain_map_min_denominator = []
        self.gain_map_max_numerator = []
        self.gain_map_max_denominator = []
        self.gamma_numerator = []
        self.gamma_denominator = []
        self.base_offset_numerator = []
        self.base_offset_denominator = []
        self.alternate_offset_numerator = []
        self.alternate_offset_denominator = []
        for c in range(channelCount):
            # int(32) gain_map_min_numerator;
            self.gain_map_min_numerator.append(read_sint(fd, 4))
            # unsigned int(32) gain_map_min_denominator;
            self.gain_map_min_denominator.append(read_uint(fd, 4))
            # int(32) gain_map_max_numerator;
            self.gain_map_max_numerator.append(read_sint(fd, 4))
            # unsigned int(32) gain_map_max_denominator;
            self.gain_map_max_denominator.append(read_uint(fd, 4))
            # unsigned int(32) gamma_numerator;
            self.gamma_numerator.append(read_uint(fd, 4))
            # unsigned int(32) gamma_denominator;
            self.gamma_denominator.append(read_uint(fd, 4))
            # int(32) base_offset_numerator;
            self.base_offset_numerator.append(read_sint(fd, 4))
            # unsigned int(32) base_offset_denominator;
            self.base_offset_denominator.append(read_uint(fd, 4))
            # int(32) alternate_offset_numerator;
            self.alternate_offset_numerator.append(read_sint(fd, 4))
            # unsigned int(32) alternate_offset_denominator;
            self.alternate_offset_denominator.append(read_uint(fd, 4))

    def contents(self):
        tuples = super().contents()
        tuples += (("version", self.version),)
        tuples += (("minimum_version", self.minimum_version),)
        tuples += (("writer_version", self.writer_version),)
        tuples += (("is_multichannel", self.is_multichannel),)
        tuples += (("use_base_colour_space", self.use_base_colour_space),)
        tuples += (("reserved", self.reserved),)
        tuples += (("base_hdr_headroom_numerator", self.base_hdr_headroom_numerator),)
        tuples += (
            ("base_hdr_headroom_denominator", self.base_hdr_headroom_denominator),
        )
        tuples += (
            ("alternate_hdr_headroom_numerator", self.alternate_hdr_headroom_numerator),
        )
        tuples += (
            (
                "alternate_hdr_headroom_denominator",
                self.alternate_hdr_headroom_denominator,
            ),
        )
        # per-channel info
        tuples += (
            (
                "gain_map_min_numerator",
                ",".join(str(v) for v in self.gain_map_min_numerator),
            ),
        )
        tuples += (
            (
                "gain_map_min_denominator",
                ",".join(str(v) for v in self.gain_map_min_denominator),
            ),
        )
        tuples += (
            (
                "gain_map_max_numerator",
                ",".join(str(v) for v in self.gain_map_max_numerator),
            ),
        )
        tuples += (
            (
                "gain_map_max_denominator",
                ",".join(str(v) for v in self.gain_map_max_denominator),
            ),
        )
        tuples += (("gamma_numerator", ",".join(str(v) for v in self.gamma_numerator)),)
        tuples += (
            ("gamma_denominator", ",".join(str(v) for v in self.gamma_denominator)),
        )
        tuples += (
            (
                "base_offset_numerator",
                ",".join(str(v) for v in self.base_offset_numerator),
            ),
        )
        tuples += (
            (
                "base_offset_denominator",
                ",".join(str(v) for v in self.base_offset_denominator),
            ),
        )
        tuples += (
            (
                "alternate_offset_numerator",
                ",".join(str(v) for v in self.alternate_offset_numerator),
            ),
        )
        tuples += (
            (
                "alternate_offset_denominator",
                ",".join(str(v) for v in self.alternate_offset_denominator),
            ),
        )
        return tuples
