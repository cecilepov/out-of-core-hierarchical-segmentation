from Code.Tree import *
from Code.Node import *


def test_init():
    node_root = Node()
    nodes = [Node(), Node(), Node(), node_root]
    tree_1 = Tree(nodes)
    
    assert tree_1.nodes is nodes
    assert tree_1.root is node_root


def test_sub_graph():
    node_1 = Node(name="Node1")
    node_2 = Node(name="NodeD2", parent=node_1)
    node_3 = Node(name="NodeIII", parent=node_2)
    node_4 = Node(name="NodeKAT", parent=node_3)
    
    tree_1 = Tree([node_4, node_3, node_2, node_1])
    assert tree_1.root is node_1
    assert tree_1.root is not node_3
    