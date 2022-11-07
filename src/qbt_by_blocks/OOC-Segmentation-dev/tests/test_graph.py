from Code.Graph import *
from Code.Border import *
from Code.Image import *


def test_init():
    edges = [(0, 1), (1, 2), (2, 3)]
    weights = [1, 6, 12]
    graph_1 = Graph(3, edges, weights)
    
    #print(edges)
    #print(graph_1.edges)
    #   TODO !: POURQUOI ?????????????????????? 
    #   assert graph_1.edges == edges
    #   assert graph_1.weights is weights
    assert graph_1.it_size is 3
    assert graph_1.n_vertices is 3


def test_do_QBT():
    IMAGE.len_x = 4
    IMAGE.len_y = 1

    border = Border(0, 0, 3, 0)
    edges = [(0, 1), (1, 2), (2, 3)]
    weights = [1, 6, 12]
    graph_1 = Graph(3, edges, weights)
    qbt_1 = graph_1.do_QBT(border)
    #print(qbt_1)
    assert qbt_1.root.is_root() is True
    assert len(qbt_1.nodes) == 7
    assert qbt_1.nodes[0].is_leaf() is True and \
           qbt_1.nodes[1].is_leaf() is True and \
           qbt_1.nodes[2].is_leaf() is True and \
           qbt_1.nodes[3].is_leaf() is True and \
           qbt_1.nodes[4].is_leaf() is False and \
           qbt_1.nodes[5].is_leaf() is False and \
           qbt_1.nodes[6].is_leaf() is False

    assert qbt_1.nodes[0] == Node(altitude=0, name=0)
    assert qbt_1.nodes[1] == Node(altitude=0, name=1)
    assert qbt_1.nodes[2] == Node(altitude=0, name=2)
    assert qbt_1.nodes[3] == Node(altitude=0, name=3)
    assert qbt_1.nodes[4] == Node(altitude=1, name=(0, 1))
    assert qbt_1.nodes[5] == Node(altitude=6, name=(1, 2))
    assert qbt_1.nodes[6] == Node(altitude=12, name=(2, 3))

    assert qbt_1.nodes[6].left == Node(altitude=6, name=(1, 2))
    assert qbt_1.nodes[6].right == Node(altitude=0, name=3)

    assert qbt_1.nodes[5].parent == Node(altitude=12, name=(2, 3))
    assert qbt_1.nodes[5].left == Node(altitude=1, name=(0, 1))
    assert qbt_1.nodes[5].right == Node(altitude=0, name=2)

    assert qbt_1.nodes[4].parent == Node(altitude=6, name=(1, 2))
    assert qbt_1.nodes[4].left == Node(altitude=0, name=0)
    assert qbt_1.nodes[4].right == Node(altitude=0, name=1)

    assert qbt_1.nodes[3].parent == Node(altitude=12, name=(2, 3))
    assert qbt_1.nodes[2].parent == Node(altitude=6, name=(1, 2))
    assert qbt_1.nodes[1].parent == Node(altitude=1, name=(0, 1))
    assert qbt_1.nodes[0].parent == Node(altitude=1, name=(0, 1))
