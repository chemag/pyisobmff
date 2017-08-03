# -*- coding: utf-8 -*-


class Box(object):  # pylint: disable=too-few-public-methods
    """box
    """
    def __init__(self):
        self.size = None
        self.box_type = None

    def __repr__(self):
        return self.box_type + '(' + str(self.size) + ')\n'
