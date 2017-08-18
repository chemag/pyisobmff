#!/usr/bin/env python
# -*- coding: utf-8 -*-
import isbmff

"""
ftyp
meta
  hdlr
  dinf
    dref
  iloc
  iinf
  pitm
"""


if __name__ == "__main__":
    #media_file = isbmff.MediaFile('autumn_1440x960.heic')
    media_file = isbmff.MediaFile()
    media_file.read('cheers_1440x960.heic')
    
    print(media_file.ftyp)
    print(media_file.meta)
    for mdat in media_file.mdats:
        print(mdat)
