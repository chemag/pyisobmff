# -*- coding: utf-8 -*-
from .box import read_box


class MediaFile(object):
    box_list = []

    def __init__(self, debug):
        self.debug = debug

    def __repr__(self):
        out = ""
        for box in self.box_list:
            out += str(box)
        return out

    def contents(self):
        tuples = ()
        for box in self.box_list:
            tuples += (("box", box.contents()),)
        return tuples

    def read(self, file_name):
        with open(file_name, "rb") as file:
            while True:
                box = read_box(file, "", self.debug)
                if box is None:
                    break
                self.box_list.append(box)
