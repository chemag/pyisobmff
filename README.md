# isobmff

A python library for reading ISOBMFF (ISO base media file format) files.

Originally from [here](https://github.com/m-hiki/isobmff).



# 1. Introduction

Goal: A tool to parse ISOBMFF files that is easy to extend.

Note that a new box type a reader, a contents dumper, and (maybe) an entry in the `isobmff/__init__.py` file.

For example, the "pitm" box (defined in ISO/IEC 14496-12:2022, Section 8.11.4) just contains a single 2-byte unsigned integer. The whole code needed to parse it (see `isobmff/pitm.py`) is:

```
$ cat isobmff/pitm.py
# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_uint


# ISO/IEC 14496-12:2022, Section 8.11.4
class PrimaryItemBox(FullBox):
    box_type = b"pitm"
    is_mandatory = False

    def read(self, file):
        self.item_id = read_uint(file, 2)

    def contents(self):
        tuples = super().contents()
        tuples += ((f"item_id", self.item_id),)
        return tuples
```


# 2. Use Cases

There are several use case:
* (1) what is inside an ISOBMFF file.
* (2) extract a given box from an ISOBMFF file [WIP].


# 3. Operation: What is in an ISOBMFF File

Parse an ISOBMFF file:
```
$ ./scripts/isobmff-parse.py media/C001.heic
path: /ftyp
  offset: 0x00000000
  box_type: b'ftyp'
  size: 36
  major_brand: b'heic'
  minor_version: 0
  compatible_brand: b'msf1'
  compatible_brand: b'mif1'
  compatible_brand: b'heic'
  compatible_brand: b'hevc'
  compatible_brand: b'iso8'
path: /meta
  offset: 0x00000024
  box_type: b'meta'
  size: 305
  version: 0
  ...
              path: /moov/trak/mdia/minf/stbl/stsd/hvc1/hvcC
                offset: 0x00000324
                box_type: b'hvcC'
                size: 108
                  configuration_version: 1
                  general_profile_space: 0
                  general_tier_flag: 0b0
                  general_profile_idc: 1
                  general_profile_compat_flags: 0b1100000000000000000000000000000
                  general_const_indicator_flags: 0b0
                  general_level_idc: 120
                  min_spatial_segmentation_idc: 0
                  parallelism_type: 0
                  chroma_format: 1
                  bit_depth_luma_minus_8: 0
                  bit_depth_chroma_minus_8: 0
                  avg_frame_rate: 12800
                  constant_frame_rate: 0
                  num_temporal_layers: 1
                  temporal_id_nested: 1
                  length_size_minus_1: 3
  ...
path: /mdat
  offset: 0x00000430
  box_type: b'mdat'
  size: 111620
path: /mdat
  offset: 0x0001b834
  box_type: b'mdat'
  size: 893103
path: /mdat
  offset: 0x000f58e3
  box_type: b'mdat'
  size: 16
```


# 4. Operation: Extract a Given Box From an ISOBMFF File

WIP: Not working yet!

Extract a box from an ISOBMFF file:
```
$ ./scripts/isobmff-parse.py --extract /moov/trak/mdia/minf/stbl/stsd/hvc1/hvcC -o C001.heic.hvcC media/C001.heic
$ stat -c "%s" C001.heic.hvcC
108
$ xxd C001.heic.hvcC
00000000: 0000 006c 6876 6343 0101 6000 0000 0000  ...lhvcC..`.....
00000010: 0000 0000 78f0 00fc fdf8 f832 000f 0320  ....x......2... 
00000020: 0001 0018 4001 0c01 ffff 0160 0000 0300  ....@......`....
00000030: 0003 0000 0300 0003 0078 f024 2100 0100  .........x.$!...
00000040: 1f42 0101 0160 0000 0300 0003 0000 0300  .B...`..........
00000050: 0003 0078 a002 8080 2d1f e5f9 246d 9ed9  ...x....-...$m..
00000060: 2200 0100 0744 01c1 9095 8112            "....D......
```


# 5. References

Standards:
* ISO/IEC 14496-12:2022, ISO base media file format
* ISO/IEC 14496-1:2014, Systems
* ISO/IEC 14496-14:2020, MP4 file format
* ISO/IEC 14496-15:2022, Carriage of network abstraction layer (NAL) unit structured video in ISO base media file format
* ISO/IEC 23008-12:2022, Image File Format
* ISO/IEC 23008-3:2015-Amd-2, 3D audio (AMENDMENT 2: MPEG-H 3D Audio File Format Support)
* ETSI TS 102 366 v1.4.1, Digital Audio Compression AC3 Enhanced AC3 Standard
* ETSI TS 103 190-2 v1.2.1, Digital Audio Compression AC4 Immersive and Personalized Audio
* IEEE 1857.3-2013, IEEE Standard for Systems of Advanced Audio and Video Coding
* [Opus in ISOBMFF Specification](https://opus-codec.org/docs/opus_in_isobmff.html)
* [Flac2 in ISOBMFF Specification](https://github.com/xiph/flac/blob/master/doc/isoflac.txt)


Video Sources:
* [videolan samples](https://streams.videolan.org/samples/)
* [videolan streams](https://streams.videolan.org/streams/)
* [Nokia Conformance Test](https://github.com/nokiatech/heif_conformance)


# Appendix 1. Requirements.

Python 3.4+


# Appendix 2. Installation

Not yet.
