
from .box import Box
from .box import FullBox
from .box import indent
from .dinf import DataInformationBox
from .hdlr import HandlerReferenceBox
from .iinf import ItemInformationBox
from .iloc import ItemLocationBox
from .iprp import ItemPropertiesBox
from .pitm import PrimaryItemBox


class MetaBox(FullBox):
    """Meta box
    """
    is_mandatory = False

    def __init__(self, box):
        super().__init__(box=box, version=box.version, flags=box.flags)
        self.hdlr = None
        self.dinf = None
        self.pitm = None
        self.iloc = None
        self.iinf = None
        self.iprp = None

    def __repr__(self):
        rep = self.hdlr.__repr__() + '\n'
        rep += self.pitm.__repr__() + '\n'
        rep += self.iloc.__repr__() + '\n'
        rep += self.iinf.__repr__() + '\n'
        rep += self.iprp.__repr__()
        return super().__repr__() + indent(rep)

    def read(self, file):
        read_size = self.size - 12
        #print(file.read(read_size))
        while read_size > 0:
            print('read_size : ' + str(read_size))
            box = Box()
            box.read(file)
            if not box.size:
                break
            self.__read_box(file, box)
            read_size -= box.size

    def __read_box(self, file, box):
        print(box.box_type + ' ' + str(box.size))
        full_box = FullBox(box)
        full_box.read(file)

        if box.box_type == 'hdlr':
            self.hdlr = HandlerReferenceBox(full_box)
            self.hdlr.read(file)
        elif box.box_type == 'dinf':
            self.dinf = DataInformationBox(full_box)
            self.dinf.read(file)
        elif box.box_type == 'iinf':
            self.iinf = ItemInformationBox(full_box)
            self.iinf.read(file)
        elif box.box_type == 'iloc':
            self.iloc = ItemLocationBox(full_box)
            self.iloc.read(file)
        elif box.box_type == 'ipmc':
            pass
        elif box.box_type == 'ipro':
            pass
        elif box.box_type == 'iprp':
            self.iprp = ItemPropertiesBox(full_box)
            self.iprp.read(file)
        elif box.box_type == 'xml ':
            pass
        elif box.box_type == 'bxml':
            pass
        elif box.box_type == 'pitm':
            self.pitm = PrimaryItemBox(full_box)
            self.pitm.read(file)
        else:
            pass
            #box_size = box.size - 8
            #if box_size > 0:
            #    print(file.read(box_size))
