
from .box import Box
from .hdlr import Hdlr
from .dinf import Dinf

class Meta(Box):
    def __init__(self, file, size):
        super().__init__()
        self.size = size
        self.box_type = 'meta'
        self.hdlr = None
        self.dinf = None
        
        read_size = size - 8
        print(read_size)
        print(file.read(read_size))
        while read_size > 0:
            size = int.from_bytes(file.read(4), 'big')
            if not size:
                break            
            self.__read_box(file, size)


    def __read_box(self, file, size):
        box_type = file.read(4).decode()
        box_size = size - 8
        print(box_type)
        if box_type == 'hdlr':
            self.hdlr = Hdlr(file, size)
        elif box_type == 'dinf':
            self.dinf = Dinf(file, size)
        elif box_type == 'ipmc':
            pass
        elif box_type == 'iloc':
            pass
        elif box_type == 'ipro':
            pass
        elif box_type == 'iinf':
            pass
        elif box_type == 'xml ':
            pass
        elif box_type == 'bxml':
            pass
        elif box_type == 'pitm':
            pass
        else:
            if box_size > 0:
                file.read(box_size)

        return box_size

    def __repr__(self):
        rep = super().__repr__()
        rep += self.hdlr.__repr__()
        rep += self.dinf.__repr__()
        return rep
