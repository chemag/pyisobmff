
from .box import Box


class Ftyp(Box):

    def __init__(self, file):
        super().__init__(file)
        self.majar_brand = file.read(4).decode()
        self.minor_version = int.from_bytes(file.read(4), 'big')
        num_compatible_brands = int((self.size - 16) / 4)
        self.compatible_brands = []
        for _ in range(num_compatible_brands):
             self.compatible_brands.append(file.read(4).decode())

    def __repr__(self):
        rep = super().__repr__()
        rep += '  ' + self.majar_brand + '\n'
        rep += '  ' + str(self.minor_version) + '\n'
        rep += '  '
        for brand in self.compatible_brands:
            rep += brand + ','
        return rep