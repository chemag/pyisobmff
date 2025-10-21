# pyisobmff: Architecture and How It Works

## Overview

`pyisobmff` is a Python library for parsing ISO Base Media File Format (ISO BMFF) files, which includes MP4, QuickTime, HEIF/HEIC, and other multimedia container formats. The library provides a flexible, extensible framework for reading and understanding the hierarchical box structure of these files.

## Core Concepts

### What is ISO BMFF?

ISO Base Media File Format (ISO/IEC 14496-12) is a container file format that stores multimedia data in a hierarchical structure of "boxes" (also called "atoms" in QuickTime terminology). Each box has:

- **Size**: 4 bytes (or 8 bytes for large boxes)
- **Type**: 4-byte FourCC code (e.g., "moov", "ftyp", "hvcC")
- **Payload**: Variable-length data specific to the box type

Some boxes are "containers" that contain other boxes, creating a tree-like structure.

## Architecture

### Main Components

```
pyisobmff/
|-- isobmff/
|   |-- __init__.py          # Package initialization, imports all box types
|   |-- media_file.py        # MediaFile class - root container for parsing
|   |-- box.py               # Core box parsing framework
|   |-- utils.py             # Binary I/O utilities
|   |-- item.py              # Item-based metadata (HEIF)
|   |
|   |-- Container boxes:
|   |-- moov.py              # Movie metadata container
|   |-- trak.py              # Track container
|   |-- mdia.py              # Media information
|   |-- minf.py              # Media information
|   |-- stbl.py              # Sample table
|   |
|   |-- Codec configurations:
|   |-- hvc.py               # HEVC (H.265) codec
|   |-- avc.py               # AVC (H.264) codec
|   |-- vpx.py               # VP9 codec
|   |-- ac3.py               # AC-3/E-AC-3 audio
|   |-- ac4.py               # AC-4 audio
|   |-- opus.py              # Opus audio
|   |-- flac.py              # FLAC audio
|   |
|   |-- Image format boxes:
|   +-- heif.py              # 70+ HEIF-specific boxes
|
+-- scripts/
    +-- isobmff-parse.py     # Command-line tool for parsing files
```

### Entry Point: MediaFile

The `MediaFile` class (media_file.py) is the main entry point:

```python
import isobmff

# Parse a file
media_file = isobmff.MediaFile("video.mp4", debug=0)
media_file.read()

# Access parsed boxes
print(media_file.box_list)

# Find specific boxes by path
hvcC = media_file.find_subbox("/moov/trak/mdia/minf/stbl/stsd/hvc1/hvcC")
```

## Parsing Flow

### 1. File Reading

When `MediaFile.read()` is called:

1. Opens the file in binary read mode
2. Calls `read_box_list()` to parse all top-level boxes
3. Returns a list of `Box` objects

### 2. Box Header Parsing

The `read_box()` function (box.py:229-350) reads each box header:

```
+-----------------------------------------+
| Standard Box Header                     |
+-----------------------------------------+
| size (4 bytes)      | type (4 bytes)    |
+-----------------------------------------+
| Payload (size - 8 bytes)                |
+-----------------------------------------+

+-----------------------------------------+
| Large Box (size = 1)                    |
+-----------------------------------------+
| size=1 (4 bytes)    | type (4 bytes)    |
| largesize (8 bytes)                     |
+-----------------------------------------+
| Payload (largesize - 16 bytes)          |
+-----------------------------------------+

+-----------------------------------------+
| FullBox (extends Box)                   |
+-----------------------------------------+
| size (4 bytes)      | type (4 bytes)    |
| version (1 byte)    | flags (3 bytes)   |
+-----------------------------------------+
| Payload                                 |
+-----------------------------------------+
```

### 3. Box Class Lookup

After reading the header, the parser finds the appropriate box class:

1. Calls `get_class_list(Box, set())` to get all `Box` subclasses
2. Matches the FourCC type with each class's `box_type` attribute
3. Determines class type (Box, FullBox, or UnimplementedBox)
4. If no match found, uses `UnimplementedBox` to store raw bytes

### 4. Box Instantiation and Reading

```python
# From box.py (simplified)
def read_box(file, path, debug, parent=None, max_offset=None, box_class=None):
    # Read header
    size = read_uint(file, 4)
    box_type = file.read(4)

    # Find matching class
    for box_class in get_class_list(Box, set()):
        if box_class.box_type == box_type:
            break

    # Instantiate and read
    if class_type == "FullBox":
        version = read_uint(file, 1)
        flags = read_uint(file, 3)
        box = box_class(...)

    # Parse payload
    box.read(file)
    return box
```

## Box Base Classes

### Box (box.py:37-136)

The fundamental base class for all boxes:

```python
class Box:
    box_type = b"xxxx"  # FourCC identifier
    is_mandatory = False
    quantity = Quantity.ZERO_OR_ONE

    def __init__(self, offset, box_type, size, parent, debug, path, max_offset):
        # Initialize common fields

    def read(self, file):
        # Default: read payload as raw bytes
        self.read_as_bytes(file)

    def contents(self):
        # Return tuple representation of parsed data
        return (("offset", hex(self.offset)),
                ("box_type", self.box_type),
                ("size", self.size))
```

### FullBox (box.py:140-166)

Extends `Box` with version and flags fields:

```python
class FullBox(Box):
    def __init__(self, offset, box_type, size, parent, debug, path, max_offset, version, flags):
        super().__init__(offset, box_type, size, parent, debug, path, max_offset)
        self.version = version
        self.flags = flags

    def contents(self):
        tuples = super().contents()
        tuples += (("version", self.version),)
        tuples += (("flags", self.flags),)
        return tuples
```

### ContainerBox (box.py:170-180)

Extends `Box` with built-in support for nested boxes:

```python
class ContainerBox(Box):
    def read(self, file):
        self.box_list = self.read_box_list(file)

    def contents(self):
        # Returns nested box contents in tree structure
```

### UnimplementedBox (box.py:183-199)

Fallback for unknown box types - stores raw bytes:

```python
class UnimplementedBox(Box):
    def read(self, file):
        self.read_as_bytes(file)  # Store as raw bytes
```

## Box Type Registration

Box types are automatically discovered through Python's class introspection - no explicit registration required!

The `get_class_list()` function (utils.py:63-68) recursively finds all subclasses:

```python
def get_class_list(cls, res=set()):
    for subclass in cls.__subclasses__():
        if subclass not in res:
            res.add(subclass)
            get_class_list(subclass, res)
    return res
```

This means any class that inherits from `Box` is automatically recognized.

## Codec Configuration Boxes

### HEVC (H.265) - hvc.py

```python
class HEVCConfigurationBox(Box):
    box_type = b"hvcC"

    def read(self, file):
        self.hevc_config = HEVCDecoderConfigurationRecord(max_offset=self.max_offset)
        self.hevc_config.read(file)

class HEVCDecoderConfigurationRecord:
    def read(self, file):
        self.configuration_version = read_uint(file, 1)
        byte = read_uint(file, 1)
        self.general_profile_space = (byte >> 6) & 0b11
        self.general_tier_flag = (byte >> 5) & 0b1
        self.general_profile_idc = byte & 0b11111
        # ... parse SPS, PPS, VPS NAL units
```

Key features:
- Parses HEVC decoder configuration
- Extracts profile, tier, level information
- Reads NAL unit arrays (SPS, PPS, VPS)
- Supports both `hvc1` and `hev1` sample entries

### AVC (H.264) - avc.py

Similar structure to HEVC, but simpler:
- Parses profile indication, level
- Reads SPS and PPS parameter sets
- Supports `avc1`, `avc3`, `avc2`, `avc4` sample entries

### VP9 - vpx.py

```python
class VPCodecConfigurationBox(FullBox):
    box_type = b"vpcC"

    def read(self, file):
        self.vp_config = VPCodecConfigurationRecord(max_offset=self.max_offset)
        self.vp_config.read(file)

class VPCodecConfigurationRecord:
    def read(self, file):
        self.profile = read_uint(file, 1)
        self.level = read_uint(file, 1)
        byte = read_uint(file, 1)
        self.bit_depth = (byte >> 4) & 0x0F
        self.chroma_subsampling = (byte >> 1) & 0x07
        self.video_full_range_flag = byte & 0x01
        # ... read color information
```

Key features:
- Parses VP9 codec parameters
- Extracts profile, level, bit depth
- Reads color space information
- Supports optional codec initialization data

## Sample Entry Hierarchy

Sample entries describe how media samples are stored:

```
VisualSampleEntry (from stbl.py)
|-- AVCSampleEntry (b"avc1")
|-- HEVCSampleEntry (b"hvc1")
|-- VP09SampleEntry (b"vp09")
+-- ... other video codecs

AudioSampleEntry (from stbl.py)
|-- AC3SampleEntry (b"ac-3")
|-- OpusSampleEntry (b"Opus")
|-- FlacSampleEntry (b"fLaC")
+-- ... other audio codecs
```

Each sample entry can contain codec configuration boxes:
- `avc1` -> `avcC` (AVC configuration)
- `hvc1` -> `hvcC` (HEVC configuration)
- `vp09` -> `vpcC` (VP9 configuration)

## File Structure Example

A typical MP4 file structure:

```
/ftyp                    # File type and brand
/mdat                    # Media data (compressed video/audio)
/moov                    # Movie metadata container
  /mvhd                  # Movie header (timescale, duration)
  /trak                  # Video track
    /tkhd                # Track header
    /mdia                # Media
      /mdhd              # Media header
      /hdlr              # Handler (vide/soun/hint)
      /minf              # Media information
        /vmhd            # Video media header
        /dinf            # Data information
        /stbl            # Sample table
          /stsd          # Sample descriptions
            /hvc1        # HEVC sample entry
              /hvcC      # HEVC configuration
          /stts          # Time-to-sample
          /stsc          # Sample-to-chunk
          /stsz          # Sample sizes
          /stco          # Chunk offsets
  /trak                  # Audio track
    /mdia
      /minf
        /stbl
          /stsd
            /ac-3        # AC-3 sample entry
              /dac3      # AC-3 configuration
```

## Extending the Library

To add support for a new box type:

### Step 1: Create a new module

Create `isobmff/mybox.py`:

```python
from .box import Box  # or FullBox, ContainerBox
from .utils import read_uint

class MyCustomBox(Box):
    box_type = b"myxx"  # Your 4-byte FourCC
    is_mandatory = False

    def read(self, file):
        # Parse box-specific payload
        self.field1 = read_uint(file, 2)
        self.field2 = read_uint(file, 4)

    def contents(self):
        tuples = super().contents()
        tuples += (("field1", self.field1),)
        tuples += (("field2", self.field2),)
        return tuples
```

### Step 2: Add import to __init__.py

Edit `isobmff/__init__.py`:

```python
from . import mybox
```

### Step 3: That's it!

The box will be automatically discovered through `get_class_list()`.

## Utility Functions

### Binary I/O (utils.py)

```python
read_uint(file, n)        # Read n-byte unsigned integer (big-endian)
read_sint(file, n)        # Read n-byte signed integer (big-endian)
read_fourcc(file)         # Read 4-byte FourCC code
read_utf8string(file, n)  # Read n-byte UTF-8 string
```

### Box Navigation

```python
# Find box by path
box = media_file.find_subbox("/moov/trak/mdia/minf/stbl/stsd")

# Get all registered box types
atom_set = isobmff.get_atom_list()

# Get all Box subclasses
box_classes = isobmff.get_class_list(isobmff.Box, set())
```

## Command-Line Usage

```bash
# Parse and display all boxes
python3 scripts/isobmff-parse.py -i video.mp4

# Extract a specific box
python3 scripts/isobmff-parse.py --extract-box --path /moov/trak/mdia/minf/stbl/stsd/hvc1/hvcC -i video.mp4 -o output.hvcC

# Extract HEIF item
python3 scripts/isobmff-parse.py --extract-item --item-id 20001 -i image.heic -o output.hvc1

# List HEIF items
python3 scripts/isobmff-parse.py --list-items -i image.heic
```

## Key Design Principles

1. **Automatic Discovery**: Box types are discovered through class introspection, not manual registration
2. **Extensibility**: New box types can be added by simply creating a new class and importing it
3. **Separation of Concerns**: Generic parsing logic (box.py) is separate from codec-specific implementations
4. **Graceful Degradation**: Unknown boxes are stored as `UnimplementedBox` with raw bytes
5. **Hierarchical Navigation**: Box paths allow easy navigation of the tree structure

## Testing Your Implementation

After adding a new box type:

1. **Parse a test file**:
   ```bash
   python3 scripts/isobmff-parse.py -i test_file.mp4 | grep myxx
   ```

2. **Extract the box**:
   ```bash
   python3 scripts/isobmff-parse.py --extract-box --path /moov/.../myxx -i test_file.mp4 -o output.bin
   ```

3. **Verify with hex dump**:
   ```bash
   hexdump -C output.bin
   ```

4. **Use Python API**:
   ```python
   import isobmff
   mf = isobmff.MediaFile("test_file.mp4")
   mf.read()
   myxx = mf.find_subbox("/moov/.../myxx")
   print(myxx.contents())
   ```

## Advanced Topics

### Item-Based Files (HEIF/HEIC)

HEIF images use an item-based structure instead of tracks:

```python
# List items
items = media_file.get_item_list()

# Get item data
item_data = media_file.get_item_data(item_id=20001)
```

### Fragmented MP4 (DASH/HLS)

Fragmented files use `moof` (Movie Fragment) boxes:

```
/ftyp
/moov            # Minimal metadata
  /mvex          # Movie extends
/moof            # Fragment 1
  /mfhd          # Fragment header
  /traf          # Track fragment
/mdat            # Fragment 1 data
/moof            # Fragment 2
/mdat            # Fragment 2 data
```

### QuickTime Extensions

QuickTime-specific boxes are in `qtff.py`:
- `fiel` - Field/frame info
- `clap` - Clean aperture
- `pasp` - Pixel aspect ratio

## Debugging

Set `debug` level when creating `MediaFile`:

```python
# debug=0: No output
# debug=1: Basic box info
# debug=2: Detailed parsing info
media_file = isobmff.MediaFile("video.mp4", debug=2)
```

## References

- ISO/IEC 14496-12: ISO Base Media File Format
- ISO/IEC 14496-15: Carriage of NAL unit structured video in ISO BMFF
- HEIF Specification: ISO/IEC 23008-12
- VP9 Codec ISO Media File Format Binding: https://www.webmproject.org/vp9/mp4/
