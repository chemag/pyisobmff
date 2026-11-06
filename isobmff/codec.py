# -*- coding: utf-8 -*-
"""Bounded reads for bit-packed codec configuration records."""


class DecoderConfigurationRecord:
    def __init__(self, max_offset):
        self.max_offset = max_offset

    def _start(self, file):
        length = self.max_offset - file.tell()
        if length < 0:
            raise ValueError("configuration starts beyond its box boundary")
        self._data = file.read(length)
        if len(self._data) != length:
            raise EOFError("truncated codec configuration box")
        self._bit_offset = 0
        self._fields = {}

    def _bits(self, count):
        if count < 0 or self._bit_offset + count > len(self._data) * 8:
            raise EOFError("truncated codec configuration record")
        if count == 0:
            return 0
        first = self._bit_offset // 8
        end = self._bit_offset + count
        last = (end + 7) // 8
        value = int.from_bytes(self._data[first:last], "big")
        value = (value >> (last * 8 - end)) & ((1 << count) - 1)
        self._bit_offset = end
        return value

    def _field(self, name, count):
        value = self._bits(count)
        return self._store(name, value)

    def _store(self, name, value):
        setattr(self, name, value)
        self._fields[name] = value
        return value

    def _bytes(self, count):
        if self._bit_offset % 8:
            raise ValueError("unaligned codec configuration byte read")
        first = self._bit_offset // 8
        if count < 0 or first + count > len(self._data):
            raise EOFError("truncated codec configuration payload")
        self._bit_offset += count * 8
        return self._data[first : first + count]

    def _remaining(self):
        return self._bytes(len(self._data) - self._bit_offset // 8)

    def contents(self):
        return tuple(self._fields.items())
