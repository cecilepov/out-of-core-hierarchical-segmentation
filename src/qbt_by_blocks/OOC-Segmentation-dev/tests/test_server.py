import pytest
import sys
from Code.Graph import *
from Code.Image import *
from Code.Block import *
from Code.Server import *


sys.setrecursionlimit(15000)


def test_compute():
    IMAGE.len_x = 6
    IMAGE.len_y = 1

    boundary_1 = Border(0, 0, 2, 0)
    boundary_2 = Border(3, 0, 5, 0)

    graph_1 = Graph(n_vertices=3, edges=[(0, 1), (1, 2)], weights=[3, 7])
    graph_2 = Graph(n_vertices=3, edges=[(0, 1), (1, 2)], weights=[6, 8])

    block_1 = Block(graph_1, boundary_1)
    block_2 = Block(graph_2, boundary_2)

    server = Server(block_1, block_2, (1, 4), 4)
    server.compute()
    assert server.selector_1_up == server.selector_2_up
    assert server.selector_1_up == Node(name=(4, 5), altitude=8)

    assert server.selector_1_up.left == Node(name=(1, 2), altitude=7)
    assert server.selector_1_up.right is None

    assert server.selector_1_up.left.left == Node(name=(3, 4), altitude=6)
    assert server.selector_1_up.left.right is None

    assert server.selector_1_up.left.left.left == Node(name="NewNode", altitude=4)
    assert server.selector_1_up.left.left.right is None

    assert server.selector_1_up.left.left.left.left == Node(name=(0, 1), altitude=3)
    assert server.selector_1_up.left.left.left.right == Node(name=4, altitude=0)

    assert server.selector_1_up.left.left.left.left.left == Node(name=1, altitude=0)
    assert server.selector_1_up.left.left.left.left.right is None

