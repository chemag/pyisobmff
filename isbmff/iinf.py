# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import indent
from .box import read_int
from .box import read_string


class ItemInformationBox(FullBox):
    """Item Information Box
    """

    def __init__(self, box):
        super().__init__(box, box.version, box.flags)
        self.item_infos = []

    def __repr__(self):
        rep = 'entry_count: ' + str(len(self.item_infos)) + '\n'
        for item in self.item_infos:
            rep += item.__repr__()
        return super().__repr__() + indent(rep)

    def read(self, file):
        if self.version == 0:
            entry_count = read_int(file, 2)
        else:
            entry_count = read_int(file, 4)

        for _ in range(entry_count):
            box = Box()
            box.read(file)

            if box.size:
                if box.box_type == 'infe':
                    full_box = FullBox(box)
                    full_box.read(file)
                    infe = ItemInfomationEntry(full_box)
                    infe.read(file)
                    self.item_infos.append(infe)
                else:
                    box_size = box.size - 8
                    if box_size > 0:
                        file.read(box_size)

class ItemInfomationEntry(FullBox):
    """Item Infomation Entry
    """

    def __init__(self, box):
        super().__init__(box, box.version, box.flags)
        self.item_id = None
        self.item_protection_index = None
        self.item_name = None
        self.item_extension = None
        self.item_type = None
        self.content_type = None
        self.content_encoding = None
        self.uri_type = None

    def __repr__(self):
        rep =  'item_id: ' + str(self.item_id) + '\n'
        rep += 'item_protection_index: ' + str(self.item_protection_index) + '\n'
        rep += 'item_name: ' + self.item_name
        if self.version >= 2:
            rep += '\nitem_type: ' + str(self.item_type)
        return super().__repr__() + indent(rep)

    def read(self, file):
        if self.version == 0 or self.version == 1:
            self.item_id = read_int(file, 2)
            self.item_protection_index = read_int(file, 2)
            self.item_name = read_string(file)
            self.content_type = read_string(file)
            self.content_encoding = read_string(file)

            if self.version == 1:
                extension_type = read_string(file, 4)
                fdel = FDItemInfoExtension()
                fdel.read(file)
                self.item_extension = fdel
        elif self.version >= 2:
            if self.version == 2:
                self.item_id = read_int(file, 2)
            elif self.version == 3:
                self.item_id = read_int(file, 4)
            self.item_protection_index = read_int(file, 2)
            self.item_type = read_string(file, 4)
            self.item_name = read_string(file)
            
            if self.item_type == 'mime':
                self.content_type = read_string(file)
                self.content_encoding = read_string(file)
            elif self.item_type == 'uri ':
                self.uri_type = read_string(file)

class FDItemInfoExtension(object):
    """FDItemInfoExtension
    """
    def __init__(self):
        self.content_location = None
        self.content_md5 = None
        self.content_length = None
        self.transfer_length = None
        self.group_ids = []
    
    def read(self, file):
        """read"""
        self.content_location = read_string(file)
        self.content_md5 = read_string(file)
        self.content_length = read_int(file, 8)
        self.transfer_length = read_int(file, 8)
        entry_count = read_int(file, 1)
        for _ in range(entry_count):
            id = read_int(file, 4)
            self.group_ids.append(id)
