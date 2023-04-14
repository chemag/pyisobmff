# -*- coding: utf-8 -*-
from .box import read_box


class MediaFile(object):
    def __init__(self):
        self.box_list = []

    def __repr__(self):
        rep = ""
        for box in self.box_list:
            rep += f"{repr(box)}\n"
        return rep

    def read(self, file_name):
        with open(file_name, "rb") as file:
            while True:
                box = read_box(file)
                if not box:
                    break
                setattr(self, box.box_type, box)
                self.box_list.append(box)
