# isobmff

A python library for reading ISOBMFF (ISO base media file format) files.

Originally from [here](https://github.com/m-hiki/isobmff).


# Operation

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


# References

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


# Requirements.

Python 3.4+


# Installation

Not yet.


