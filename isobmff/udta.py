# -*- coding: utf-8 -*-
from .box import ContainerBox


# ISO/IEC 14496-12:2022, Section 8.10
class UserDataBox(ContainerBox):
    box_type = "udta"
