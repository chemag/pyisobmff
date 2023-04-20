# -*- coding: utf-8 -*-
import os

from .box import Box
from .box import find_subbox


class MediaFile(Box):
    def __init__(self, filename, debug):
        self.filename = filename
        offset = 0
        payload_offset = 0
        path = ""
        size = os.path.getsize(self.filename)
        largesize = None
        super().__init__(offset, payload_offset, path, size, largesize, debug)
        self.debug = debug

    def contents(self):
        # no super() here as the box header data is false
        tuples = ()
        for box in self.box_list:
            tuples += (("box", box.contents()),)
        return tuples

    def read(self):
        with open(self.filename, "rb") as file:
            self.box_list = self.read_box_list(file)

    def find_subbox(self, full_path):
        return find_subbox(self, full_path)
