
from .box import Box
from .hdlr import Hdlr
from .dinf import Dinf

class Meta(Box):
    def __init__(self, box):
        super().__init__(box.size, box.box_type)
        self.hdlr = None
        self.dinf = None        

    def read(self, file):
        read_size = self.size - 8
        print(read_size)
        print(file.read(read_size))
        while read_size > 0:
            box = Box()
            box.read(file)
            if not box.size:
                break
            self.__read_box(file, box)
            read_size -= box.size

    def __read_box(self, file, box):
        box_size = box.size - 8
        print(box.box_type)
        if box.box_type == 'hdlr':
            hdlr = Hdlr(box)
            hdlr.read(file)
            self.hdlr = hdlr
        elif box.box_type == 'dinf':
            dinf = Dinf(box)
            dinf.read(file)
            self.dinf = dinf
        elif box.box_type == 'ipmc':
            pass
        elif box.box_type == 'iloc':
            pass
        elif box.box_type == 'ipro':
            pass
        elif box.box_type == 'iinf':
            pass
        elif box.box_type == 'xml ':
            pass
        elif box.box_type == 'bxml':
            pass
        elif box.box_type == 'pitm':
            pass
        else:
            if box_size > 0:
                file.read(box_size)

    def __repr__(self):
        rep = super().__repr__()
        rep += self.hdlr.__repr__()
        rep += self.dinf.__repr__()
        return rep
