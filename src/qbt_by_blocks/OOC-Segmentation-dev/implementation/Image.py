import collections

ImageSize = collections.namedtuple('ImageSize', ['len_x', 'len_y'])


class IMAGE:
    def __init__(self, x, y):
        self.len_x = x
        self.len_y = y


IMAGE = IMAGE(-1, -1)
