# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_box


class MetaBox(FullBox):
    """Meta box
    """
    box_type = 'meta'
    is_mandatory = False
    
    def read(self, file):
        read_size = self.get_box_size()
        #print(file.read(read_size))
        while read_size > 0:
            box = read_box(file)
            if not box:
                break
            setattr(self, box.box_type, box)
            read_size -= box.size
