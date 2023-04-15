# -*- coding: utf-8 -*-
from .box import ContainerBox


# ISO/IEC 14496-12:2022, Section 8.3.3
class TrackReferenceBox(ContainerBox):
    box_type = "tref"
