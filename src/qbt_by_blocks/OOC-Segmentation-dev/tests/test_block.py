import pytest
import sys
from Code.Graph import *
from Code.Image import *
from Code.Block import *
from Code.Server import *


sys.setrecursionlimit(15000)


def test_update_tree():
    IMAGE.len_x = 6
    IMAGE.len_y = 1

    boundary_1 = Border(0, 0, 2, 0)
    boundary_2 = Border(3, 0, 5, 0)

    graph_1 = Graph(n_vertices=3, edges=[(0, 1), (1, 2)], weights=[3, 7])
    graph_2 = Graph(n_vertices=3, edges=[(0, 1), (1, 2)], weights=[6, 8])


    block_1 = Block(graph_1, boundary_1)
    block_2 = Block(graph_2, boundary_2)

    server = Server(block_1, block_2, (1, 4), 4)
    block_1.get_border_tree([0, 1])
    pass
    #server.merging()


