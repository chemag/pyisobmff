# -*- coding: utf-8 -*-
from .box import ContainerBox
from .box import FullBox
from .utils import read_uint
from .utils import read_utf8string


# ISO/IEC 14496-12:2022, Section 8.10
# "The User Data Box is a container box for informative user-data.
# This user data is formatted as a set of boxes with more specific
# box types, which declare more precisely their content. The
# contained boxes are normal boxes, using a defined, registered,
# or UUID extension box type."
class UserDataBox(ContainerBox):
    box_type = b"udta"


# ISO/IEC 14496-12:2022, Section 8.10.2
class CopyrightBox(FullBox):
    box_type = b"cprt"

    def read(self, file):
        first_word = read_uint(file, 2)
        # unsigned int(5)[3] language; // ISO-639-2/T language code
        # "Each character is packed as the difference between its
        # ASCII value and 0x60."
        self.language = (
            chr(0x60 + ((first_word >> 10) & 0x1F))
            + chr(0x60 + ((first_word >> 5) & 0x1F))
            + chr(0x60 + ((first_word >> 0) & 0x1F))
        )
        # utfstring notice;
        max_len = self.max_offset - file.tell()
        self.notice = read_utf8string(file, max_len)

    def contents(self):
        tuples = super().contents()
        tuples += (("language", self.language),)
        tuples += (("notice", self.notice),)
        return tuples
