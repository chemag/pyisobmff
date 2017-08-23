# -*- coding: utf-8 -*-
from .box import FullBox
from .box import Quantity


class MetaBox(FullBox):
    """Meta Box"""
    box_type = 'meta'
    is_mandatory = False
    quntity = Quantity.ZERO_OR_ONE
