# -*- coding: utf-8 -*-
from .box import read_box


class MediaFile(object):
    box_list = []

    def __init__(self, debug):
        self.debug = debug

    def __repr__(self):
        rep = ""
        for box in self.box_list:
            rep += f"{repr(box)}\n"
        return rep

    def contents(self):
        tuples = ()
        for box in self.box_list:
            tuples += (("box", box.contents()),)
        return tuples

    @classmethod
    def print(cls, tuples, indent):
        tab_size = 2
        for key, val in tuples:
            if key == "box":
                cls.print(val, indent + 1)
            else:
                tab = " " * tab_size * (indent if key != "path" else (indent - 1))
                print(f"{tab}{key}: {val}")

    def read(self, file_name):
        with open(file_name, "rb") as file:
            while True:
                box = read_box(file, "", self.debug)
                if box is None:
                    break
                self.box_list.append(box)
