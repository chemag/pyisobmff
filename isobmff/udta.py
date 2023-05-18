# -*- coding: utf-8 -*-
from .box import ContainerBox


# ISO/IEC 14496-12:2022, Section 8.10
# "The User Data Box is a container box for informative user-data.
# This user data is formatted as a set of boxes with more specific
# box types, which declare more precisely their content. The
# contained boxes are normal boxes, using a defined, registered,
# or UUID extension box type."
class UserDataBox(ContainerBox):
    box_type = b"udta"
