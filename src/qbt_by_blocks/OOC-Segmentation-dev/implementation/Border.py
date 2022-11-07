from Code.Image import *
from Code.Node import Node


class Border:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        assert self.x1 >= 0 and self.y1 >= 0 and self.x2 < IMAGE.len_x and self.y2 < IMAGE.len_y, \
            "The border must remain inside the image"
        assert self.x1 <= self.x2 and self.y1 <= self.y2, "X1 must be lower or equal than X2 and the same goes for Y"

    def to_im_size(self):
        """Convert self object to a ImageSize one

        :return: The size of the border
        """
        return ImageSize(self.x2 - self.x1 + 1, self.y2 - self.y1 + 1)

    def int_coords_ibloc_to_iimage(self, int_name):
        img_size = self.to_im_size()
        n = img_size.len_x*img_size.len_y
        assert n > int_name >= 0
        """
        Require the IMSIZE and the border
        Convert i0', i1', ... to i0, i1, ...

        i' is the index of int_name in the border
        i' is int_name
        i represent the index of a node in the image

        return i
        """
        x1, y1 = coords_i_to_xy(int(int_name), self.to_im_size())
        x1 += self.x1
        y1 += self.y1
        return y1 * IMAGE.len_x + x1

    def generate_leafs(self):
        """
        IS = b = ImageSize(4,2)
        b = Boundary(0,0,1,1)

        generate_leafs(b, IS) will return:
            0
            1
            3
            4
        """
        img_len = self.to_im_size()
        return [Node(name=self.int_coords_ibloc_to_iimage(i), altitude=0) for i in range(img_len.len_x * img_len.len_y)]


def coords_i_to_xy(i, imsize):
    """
    Require the IMSIZE and the border
    Referential change from i0, i1, i2, ... to (x0, y0), (y2, y2), ...

    0123 => | 0 : (x=0, y=0) | 4 : (x=0, y=1)
    4567 => | 1 : (x=1, y=0) |

    >>> print(coords_i_to_xy(2, ImageSize(2,2)))
    (0, 1)
    >>> print(coords_i_to_xy(2, ImageSize(2,4)))
    (0, 1)
    >>> print(coords_i_to_xy(0, ImageSize(1,1)))
    (0, 0)
    """
    x = i % imsize.len_x
    y = i // imsize.len_x

    return x, y


def int_coords_ibloc_to_iimage(int_name, border):
    """
    Require the IMSIZE and the border
    Convert i0', i1', ... to i0, i1, ...

    i' is the index of int_name in the border
    i' is int_name
    i represent the index of a node in the image

    return i
    """
    x1, y1 = coords_i_to_xy(int(int_name), border.to_im_size())
    x1 += border.x1
    y1 += border.y1
    return y1 * IMAGE.len_x + x1


def coords_ibloc_to_iimage(node, border):
    """
    Require the IMSIZE and the border
    Convert i0', i1', ... to i0, i1, ...

    i' represent the index in the border
    i' is the name of the node
    i represent the index of a node in the image

    return i
    """
    x1, y1 = coords_i_to_xy(int(node.name), border.to_im_size())
    x1 += border.x1
    y1 += border.y1
    node.name = y1 * IMAGE.len_x + x1
