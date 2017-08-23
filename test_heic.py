#!/usr/bin/env python
# -*- coding: utf-8 -*-
import isobmff


if __name__ == "__main__":
    media_file = isobmff.MediaFile()
    media_file.read('C001.heic')
    #print(media_file)
