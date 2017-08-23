# isobmff
The isobmff is an open source software library for reading/writing ISO base media file format.

## Requirements.

Python 3.4+

## Installation

## Getting Started
### Reading a media file
```python
    media_file = isobmff.MediaFile()
    media_file.read('cheers_1440x960.heic')
    print(media_file)
```
### Writing a media file

## References
- confermance test : https://github.com/nokiatech/heif_conformance
- [ISO/IEC 14496-12:2015 ISO Base Media File Format](http://mpeg.chiariglione.org/standards/mpeg-4/iso-base-media-file-format/text-isoiec-14496-12-5th-edition)
- ISO/IEC 14496-15 Carriage of network abstraction layer (NAL) unit structured video in the ISO base media file format
    - box types: 'hvc1', 'hev1', 'hvcC'
- [ISO/IEC CD 23008-12 HEVC Still Image File Format](http://mpeg.chiariglione.org/standards/mpeg-h/image-file-format/text-isoiec-cd-23008-12-image-file-format)
    - box types: 'iprp', 'ispe', 'ipma'
- [ITU-T Rec. H.265](http://www.itu.int/rec/T-REC-H.265)

## Author
Minoru Hiki