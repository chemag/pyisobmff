

HEADER_SIZE = 8


class Box(object):
    def __init__(self, file):
        self.size = int.from_bytes(file.read(4), 'big')
        self.box_type = file.read(4).decode()

    def __repr__(self):
        return self.box_type + '(' + str(self.size) + ')\n'
