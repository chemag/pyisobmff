"""Small, in-memory ISOBMFF fixtures; no encoded media dependency."""

import io
import struct

from isobmff.box import read_box


def box(fourcc, payload):
    return struct.pack(">I4s", len(payload) + 8, fourcc) + payload


def parse(data):
    stream = io.BytesIO(data)
    parsed = read_box(stream, "", 0, max_offset=len(data))
    return parsed, stream


def bits(*fields):
    value, count = 0, 0
    for width, field in fields:
        if not 0 <= field < (1 << width):
            raise ValueError("fixture field does not fit")
        value = (value << width) | field
        count += width
    if count % 8:
        raise ValueError("fixture is not byte aligned")
    return value.to_bytes(count // 8, "big")


def visual_sample_entry(fourcc, config, width=640, height=480):
    header = struct.pack(
        ">6sH16sHHIIIH32sHh",
        bytes(6),
        1,
        bytes(16),
        width,
        height,
        0x00480000,
        0x00480000,
        0,
        1,
        bytes(32),
        24,
        -1,
    )
    return box(fourcc, header + config)


def movie(fourcc, config):
    sample = visual_sample_entry(fourcc, config)
    data = box(b"stsd", bytes(4) + struct.pack(">I", 1) + sample)
    for fourcc in (b"stbl", b"minf", b"mdia", b"trak", b"moov"):
        data = box(fourcc, data)
    return data
