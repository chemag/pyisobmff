# -*- coding: utf-8 -*-
from .box import Box


# ISO/IEC 14496-12:2022, Section 8.10
class UserDataBox(Box):
    box_type = b"udta"
