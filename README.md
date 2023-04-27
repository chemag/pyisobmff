# isobmff

A python library for reading ISOBMFF (ISO base media file format) files.

Originally from [here](https://github.com/m-hiki/isobmff).



# 1. Introduction: The ISOBMFF Media File Format

ISOBMFF is a popular file format for encapsulating media content, including video, images, and audio. The format originated in Apple's QuickTime, but has been standardized (as ISO/IEC 14496-12:2022), and extended for different media content.

The ISOBMFF format is relatively simple: All data is organized in "boxes" (aka "atoms"), which are just TLV blobs: A blob with a type, a length (size), and a value. In the wire, a box starts with the size field (4 bytes), then the type field (which follows a well-known, registered fourcc structure -- 4 bytes), and then the value. The exact contents of the value field depends on the box type. Note that some of the boxes can have other boxes (they are sometimes defined as "containers"), which will follow the same TLB structure.

There are a couple of quirks on the TLV structure:
* Type and length are normally 4 bytes, but special values ("uuid" for types, and 1 for size) allows extended versions of them.
* Some boxes (known as "FullBox") also have an extra 4-byte field after the type, including a version number and a set of flags. This allows box definitions to evolve.

Let's show how an ISOBMFF stream looks like:

As an example, these are the the first few bytes of the test media file we include in this package:
```
$ xxd media/C001.heic
00000000: 0000 0024 6674 7970 6865 6963 0000 0000  ...$ftypheic....
00000010: 6d73 6631 6d69 6631 6865 6963 6865 7663  msf1mif1heichevc
00000020: 6973 6f38 0000 0131 6d65 7461 0000 0000  iso8...1meta....
00000030: 0000 0021 6864 6c72 0000 0000 0000 0000  ...!hdlr........
00000040: 7069 6374 0000 0000 0000 0000 0000 0000  pict............
...
```

Note the file starts with 4 bytes that indicate the size of the first box (0x00000024, or 36 bytes). The next 4 bytes include the type, which in this case is "ftyp". The "ftyp" box (aka `FileTypeBox`) is defined in ISO/IEC 23008-12:2022, Section 4.3.2).
```
aligned(8) class GeneralTypeBox(code) extends Box(code) {
    unsigned int(32) major_brand;
    unsigned int(32) minor_version;
    unsigned int(32) compatible_brands[]; // to end of the box
}
aligned(8) class FileTypeBox extends GeneralTypeBox ('ftyp')
{}
```

The value is the next 28 bytes (the "size" field includes itself, so the value is 36 - 8 = 28 bytes). It includes 3 fields:
* the "`major_brand`" field value is "heic". This field occupies 4 bytes.
* the "`minor_version`" field value is 0x00000000. This field occupies 4 bytes.
* the "`compatible_brands[]`" array contains the value ["msf1", "mif1", "heic", "hevc", "iso8"]. This field occupies the remaining of the box, which in this case is 20 bytes, or 5 fourcc types.

At offset 0x24 we can see the second box. Its size is 0x00000131 (305 bytes), and its type is "meta". The "meta" box (aka `MetaBox`) is defined in ISO/IEC 14496-12:2022, Section 8.11.1.1.
```
aligned(8) class MetaBox (handler_type)
        extends FullBox('meta', version = 0, 0) {
    HandlerBox(handler_type) theHandler;
    PrimaryItemBox primary_resource; // optional
    DataInformationBox file_locations; // optional
    ItemLocationBox item_locations; // optional
    ItemProtectionBox protections; // optional
    ItemInfoBox item_infos; // optional
    IPMPControlBox IPMP_control; // optional
    ItemReferenceBox item_refs; // optional
    ItemDataBox item_data; // optional
    Box other_boxes[]; // optional
}
```

Note that the "meta" box is a "`FullBox`", which means that the 4 bytes just after the fourcc tag (0x00000000) are the version and the flags fields (both 0). The next bytes are a "hdlr" (`HandlerBox`) box, defined in ISO/IEC 14496-12:2022, Section 8.4.3.


# 2. Why a New Parser?

The main goal of this tool is to have an ISOBMFF box parser that is easy to extend.

We considered several options before writing a new one:
* ffmpeg. Of course, if you do any media processing, ffmpeg should be the first option. We wanted a simple parser, while ffmpeg is a full demuxer.
* mp4dump from [bento4](https://github.com/axiomatic-systems/Bento4). The tool works relatively well (in fact the simple parser's output is inspired in that tool), but it is too chatty. For example, the implementation of the "stts" box includes 327 lines of C++ code. In comparison, the implementation in this package is only ~20 lines.
* other similar C++ tools, including [gpac](https://github.com/gpac/gpac), [AtomicParsley](https://github.com/wez/atomicparsley), and [mp4v2](https://mp4v2.org/). gpac in particular is the most promising tool: It seems active (as of 20230420), and it understands item IDs, which provides a nice extra extraction feature (e.g. to extract h265 key frames from heic files). Again, we find the cost of adding new parsers to be cumbersome.
* [pymp4](https://github.com/beardypig/pymp4) is similar to this package. It is based on the [construct python library](https://en.wikipedia.org/wiki/Construct_(python_library)), which is very appealing as it allows declarative definitions of new boxes. In our opinion, the structures of ISOBMFF are too generic to be easily captured by the `construct` package.

The closest thing to what we were looking for was [isobmff](https://github.com/m-hiki/isobmff). This package allows relatively simple definitions of new boxes. Note that a new box type just needs to define a class (`Box` or `FullBox`) with:
* (1) the actual fourcc, defined as the "`box_type`" class method,
* (2) a `read()` method that reads the actual bytes,
* (3) a `contents()` method that dump the contents in a series of tuples.

If you decide that the new box is independent enough that it deserves a new file, then you need to add a new entry in the `isobmff/__init__.py` file.

For example, the "pitm" box (defined in ISO/IEC 14496-12:2022, Section 8.11.4) just contains a single 2-byte unsigned integer (4 bytes in newer versions). Its definition in the standard is:

```
aligned(8) class PrimaryItemBox
  extends FullBox('pitm', version, 0) {
    if (version == 0) {
        unsigned int(16) item_ID;
    } else {
        unsigned int(32) item_ID;
    }
}
```

The whole code needed to parse it (see `isobmff/pitm.py`) is:
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
        self.item_id = read_uint(file, 2 if self.version == 0 else 4)

    def contents(self):
        tuples = super().contents()
        tuples += ((f"item_id", self.item_id),)
        return tuples
```


# 3. Use Cases

There are several use case:
* (1) what is inside an ISOBMFF file.
* (2) extract a given box from an ISOBMFF file.
* (3) understand items inside an ISOBMFF file.


## 3.1. Operation: What is in an ISOBMFF File

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

We have thoroughly tested the parser by using the testdir mode in a directory containing all the video sources mentioned in the References Section. There is only 1 file where our parser chokes. None of the other tools can either (gpac's mp4dump or ffmpeg).

```
$ ./scripts/isobmff-parse.py  --testdir ~/video/test
# BROKEN FILES
-> video/test/videolan/samples/A-codecs/DVAudio/00_Testfilm_fha1.mov
error: UNIMPLEMENTED size=0 BoxHeader (Section 4.2.2 Page 8)
```

## 3.2. Operation: Extract a Given Box From an ISOBMFF File

Check the full list of boxes:
```
$ ./scripts/isobmff-parse.py media/C001.heic  |grep -a path:
  path: /ftyp
  path: /meta
    path: /meta/hdlr
    path: /meta/pitm
    path: /meta/iloc
    path: /meta/iinf
      path: /meta/iinf/infe
    path: /meta/iprp
      path: /meta/iprp/ipco
        path: /meta/iprp/ipco/hvcC
        path: /meta/iprp/ipco/ispe
      path: /meta/iprp/ipma
  path: /moov
    path: /moov/mvhd
    path: /moov/trak
      path: /moov/trak/tkhd
      path: /moov/trak/mdia
        path: /moov/trak/mdia/mdhd
        path: /moov/trak/mdia/hdlr
        path: /moov/trak/mdia/minf
          path: /moov/trak/mdia/minf/vmhd
          path: /moov/trak/mdia/minf/dinf
            path: /moov/trak/mdia/minf/dinf/dref
              path: /moov/trak/mdia/minf/dinf/dref/url\x20
          path: /moov/trak/mdia/minf/stbl
            path: /moov/trak/mdia/minf/stbl/stsd
              path: /moov/trak/mdia/minf/stbl/stsd/hvc1
                path: /moov/trak/mdia/minf/stbl/stsd/hvc1/hvcC
                path: /moov/trak/mdia/minf/stbl/stsd/hvc1/ccst
            path: /moov/trak/mdia/minf/stbl/stts
            path: /moov/trak/mdia/minf/stbl/stsc
            path: /moov/trak/mdia/minf/stbl/stco
            path: /moov/trak/mdia/minf/stbl/stsz
            path: /moov/trak/mdia/minf/stbl/stss
  path: /mdat
  path: /mdat2
  path: /mdat3
```

Note that, when it detects 2+ boxes of the same type under the same container, it will append a consecutive number to them.

Extract a box from an ISOBMFF file:
```
$ ./scripts/isobmff-parse.py --extract-box --path /moov/trak/mdia/minf/stbl/stsd/hvc1/hvcC -o C001.heic.hvcC media/C001.heic
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

Note that we have extracted the full box, including the size, type (fourcc), and (for FullBox boxes) the version/flags bytes. If you only want the payload, you can use the "`--extract-value`" option instead.

Extract a box value (just the payload) from an ISOBMFF file:
```
$ ./scripts/isobmff-parse.py --extract-value --path /moov/trak/mdia/minf/stbl/stsd/hvc1/hvcC -o C001.heic.hvcC media/C001.heic
$ stat -c "%s" C001.heic.hvcC
100
$ xxd C001.heic.hvcC
00000000: 0101 6000 0000 0000 0000 0000 78f0 00fc  ..`.........x...
00000010: fdf8 f832 000f 0320 0001 0018 4001 0c01  ...2... ....@...
00000020: ffff 0160 0000 0300 0003 0000 0300 0003  ...`............
00000030: 0078 f024 2100 0100 1f42 0101 0160 0000  .x.$!....B...`..
00000040: 0300 0003 0000 0300 0003 0078 a002 8080  ...........x....
00000050: 2d1f e5f9 246d 9ed9 2200 0100 0744 01c1  -...$m.."....D..
00000060: 9095 8112                                ....
```

## 3.3. Operation: Understand Items Inside an ISOBMFF File

First, let's see which items are available in an ISOBMFF file.
```
$ ./scripts/isobmff-parse.py --list-items media/C001.heic
item_id,item_type,primary,offset,length
20001,hvc1,1,0,111612
```

Note the output is a CSV file containing items IDs, types, whether they are the primary item, the offset, and the length. In this case we only have 1 item, namely an "hvc1" one.

Second, let's extract  specific items.
```
$ ./scripts/isobmff-parse.py --extract-item -o /tmp/C001.heic.20001.hvc1 --item-id 20001 media/C001.heic
$ xxd /tmp/C001.heic.20001.hvc1
00000000: 0001 b3be 2601 af13 8077 57cf 9d5d 2930  ....&....wW..])0
00000010: e619 759f 1cd2 d841 0778 8d99 91b8 2065  ..u....A.x.... e
00000020: 85f6 2e5f cba3 1785 6275 cce4 ba2b dad9  ..._....bu...+..
00000030: 6394 59a5 8aa7 4724 7f69 edde 326d 4841  c.Y...G$.i..2mHA
00000040: dc01 c896 d3c2 8626 2140 24b2 6985 7b0c  .......&!@$.i.{.
00000050: f368 6bb1 4916 0a13 518a ff4d 1fbd 4d99  .hk.I...Q..M..M.
00000060: 1b35 b434 4d53 ab32 673c e08c 29e7 1234  .5.4MS.2g<..)..4
...
```

# 4. TODO

There are a couple of interesting use cases that we do not support yet:
* (1) extract processed items. Right now the tool can extract an item based on its exact location (`iloc` box). But sometimes we want to extend the box, for example adding a config frame to an HEVC key frame ("hvc1" item type). This is what gpac's MP4Box does.


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
* [Encapsulation of FLAC in ISO Base Media File Format](https://github.com/xiph/flac/blob/master/doc/isoflac.txt)


Video Sources:
* [videolan samples](https://streams.videolan.org/samples/)
* [videolan streams](https://streams.videolan.org/streams/)
* [Nokia Conformance Test](https://github.com/nokiatech/heif_conformance)
* [DECE CFF Test Files](https://www.uvcentral.com/cff/cff-test-files.html)


# Appendix 1. Requirements.

Python 3.4+


# Appendix 2. Installation

Not yet.
