#!/usr/bin/env python
# -*- coding: utf-8 -*-
import struct
from isbmff.ftyp import Ftyp


def read_box(f):
    box_len = int.from_bytes(f.read(4), 'big')
    box_type = f.read(4).decode()
    print('length : ' + str(box_len))
    print('box    : ' + box_type)
    box_data = f.read(box_len - 8)
    #print(box_data)

if __name__ == "__main__":
    f = open('autumn_1440x960.heic', 'rb')
    #b = f.read(4)
    #v = struct.unpack('L', b)
    ftype = Ftyp(f)
    print(ftype)

    f.close()