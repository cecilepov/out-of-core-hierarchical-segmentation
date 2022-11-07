import Tree
from Image import *


def generate_leafs(boundary, IMSIZE):
    """
    IS = b = ImageSize(4,2)
    b = Boundary(0,0,1,1)
    
    generate_leafs(b, IS) will return:
        0
        1
        3
        4
    """
    return [Tree.Node(name=int_coords_ibloc_to_iimage(i, IMSIZE, boundary), altitude=0) for i in index(boundary)]


def index(bound):
    """
    Used in addition to generate_leafs when i are required to name nodes
    index(Boundary(0,0,1,1)) will yield:
        0
        1
        2
        3
    and so on, it 
    """
    img_len = boundary_to_image_size(bound)
    for i in range(img_len.len_x * img_len.len_y):
        yield i


def do_QBT(graph, IMSIZE):
    graph.sort()
    nodes = generate_leafs(graph.boundary, IMSIZE)

    for i, edge in enumerate(graph):
        e1 = int_coords_ibloc_to_iimage(edge[0], IMSIZE, graph.boundary)
        e2 = int_coords_ibloc_to_iimage(edge[1], IMSIZE, graph.boundary)

        if nodes[edge[0]].root() is nodes[edge[1]].root():
            continue

        nodes.append(Tree.Node(name=(e1, e2),
                               altitude=graph.weights[i],
                               childs=(nodes[edge[0]].root(), nodes[edge[1]].root())))
        nodes[edge[0]].root().parent = nodes[-1]
        nodes[edge[1]].root().parent = nodes[-1]
    res = Tree.Tree(nodes)
    return res


def coords_ibloc_to_iimage(node, IMSIZE, boundary):
    """
    Require the IMSIZE and the boundary
    Convert i0', i1', ... to i0, i1, ...

    i' represent the index in the boundary
    i' is the name of the node
    i represent the index of a node in the image
    
    return i
    """
    x1, y1 = coords_i_to_xy(int(node.name), boundary_to_image_size(boundary))
    x1 += boundary.x1
    y1 += boundary.y1
    node.name = y1 * IMSIZE.len_x + x1


def int_coords_ibloc_to_iimage(int_name, IMSIZE, boundary):
    """
    Require the IMSIZE and the boundary
    Convert i0', i1', ... to i0, i1, ...

    i' is the index of int_name in the boundary
    i' is int_name
    i represent the index of a node in the image

    return i
    """
    x1, y1 = coords_i_to_xy(int(int_name), boundary_to_image_size(boundary))
    x1 += boundary.x1
    y1 += boundary.y1
    return y1 * IMSIZE.len_x + x1


def coords_i_to_xy(i, imsize):
    """
    Require the IMSIZE and the boundary
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

    return (x, y)


def merge(nodes1, nodes2, edge):
    pass
