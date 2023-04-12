#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

dirname = os.path.dirname(sys.modules[__name__].__file__)
this_dir = os.path.abspath(dirname)
rootdir = os.path.join(this_dir, "..")
sys.path.append(rootdir)

import isobmff


TESTFILE = os.path.join(rootdir, "media/C001.heic")
if __name__ == "__main__":
    media_file = isobmff.MediaFile()
    media_file.read(TESTFILE)
    # print(media_file)
