# -*- coding: utf-8 -*-


class Box(object):  # pylint: disable=too-few-public-methods
    """box
    """

    def __init__(self, size=None, box_type=None):
        self.size = size
        self.box_type = box_type

    def __repr__(self):
        return self.box_type + '(' + str(self.size) + ')\n'


    def read(self, file):
        """
        """
        self.size = int.from_bytes(file.read(4), 'big')
        self.box_type = file.read(4).decode()

    def write(self, file):
        pass