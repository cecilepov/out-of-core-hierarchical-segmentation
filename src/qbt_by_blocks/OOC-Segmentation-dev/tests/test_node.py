# -*-coding:Latin-1 -*  #Evite les erreurs Ã  la CON de Spyder pour l'ESIEE
import pytest
from Code.Node import *


def test_init():
    node_1 = Node()
    assert node_1.name is None
    assert node_1.altitude is None
    assert node_1.parent is None
    assert node_1.left is None
    assert node_1.right is None

    node_2 = Node(name="NomTest")
    assert node_2.name is "NomTest"
    assert node_2.altitude is None
    assert node_2.parent is None
    assert node_2.left is None
    assert node_2.right is None

    node_3 = Node(name="NodeTrois", left=node_2)
    assert node_3.name is "NodeTrois"
    assert node_3.left is node_2
    #   Test binds corrects (node_3->node_2)
    assert node_3.left == node_2
    assert node_3.left.name == "NomTest"
    assert node_2.parent is node_3

    node_4 = Node(name="Node4", altitude=42100, parent=node_1, right=node_3)
    assert node_4.parent is node_1
    assert node_4.parent == node_1

    node_5 = Node(name="Node5", altitude=300)
    node_6 = Node(name="NodeSix", altitude=120)
    node_7 = Node(name="Node7ven", altitude=10)
    node_8 = Node(name="Node8", altitude=42, parent=node_5, left=node_6, right=node_7)
    assert node_8.right is node_7
    assert node_7.parent is node_8

    assert node_8.left is node_6
    assert node_6.parent is node_8

    assert node_8.parent is node_5
    assert  node_5.left is node_8
    assert node_5.is_leaf() is False and node_6.is_leaf() is True and node_7.is_leaf() is True


def test_str():
    node_1 = Node()
    assert str(node_1) == "[None, 'None', [None], {None, None}]"
    
    node_2 = Node(name="NomTest")
    assert str(node_2) == "[None, 'NomTest', [None], {None, None}]"

    node_3 = Node(name="NodeTrois", left=node_2)
    assert str(node_3) == "[None, 'NodeTrois', [None], {NomTest, None}]"

    node_4 = Node(name="Node4", altitude=42100, parent=node_1, right=node_3)
    assert str(node_4) == "[42100, 'Node4', [None], {NodeTrois, None}]"
    
    node_5 = Node(name="Node5", altitude=300)
    node_6 = Node(name="NodeSix", altitude=120)
    node_7 = Node(name="Node7ven", altitude=10)
    node_8 = Node(name="Node8", altitude=42, parent=node_5, left=node_6, right=node_7)
    assert str(node_8) == "[42, 'Node8', [Node5], {NodeSix, Node7ven}]"


def test_egality_and_is():
    a = Node()
    b = Node()
    assert a is not b
    assert a == b
    
    c = Node(name="lol", parent=a)
    d = Node(name="lol", parent=b)
    assert c is not d
    assert c == d
    assert c is not None


def test_root():
    #   5->6->7->8
    node_5 = Node(name="Node5", altitude=300)
    node_6 = Node(name="NodeSix", altitude=120, parent=node_5)
    node_7 = Node(name="Node7ven", altitude=10, parent=node_6)
    node_8 = Node(name="Node8", altitude=42, parent=node_7)
    root = node_8.root()
    #print(root)
    assert root is node_5
    assert root == node_5


def test_is_root():
    node_1 = Node(name="NodeI", altitude=300)
    node_2 = Node(name="NodeII", altitude=120, parent=node_1)
    node_3 = Node(name="NodeIII", altitude=10, parent=node_2)
    node_4 = Node(name="NodeIV", altitude=42, parent=node_3)
    assert node_1.is_root()
    assert node_2.is_root() or node_3.is_root() or node_4.is_root() is False


def test_rec_height():
    node_1 = Node(name="NodeI", altitude=300)
    node_2 = Node(name="NodeII", altitude=120, parent=node_1)
    node_3 = Node(name="Node3", altitude=10, parent=node_2)
    node_4 = Node(name="Node4", altitude=42, parent=node_3)
    #print(node_1)
    #print(node_2)
    #print(node_3)
    #print(node_4)
    assert node_1.rec_height(0) == 3
    assert node_2.rec_height(0) == 2
    assert node_3.rec_height(0) == 1
    assert node_4.rec_height(0) == 0
    assert node_1.rec_height(300) == 303
    with pytest.raises(AssertionError):
        assert node_1.rec_height(-1) == 2


def test_add_delete_child():
    node_5 = Node(name="Node5", altitude=300)
    node_6 = Node(name="NodeSix", altitude=120)
    node_7 = Node(name="Node7ven", altitude=10)
    node_7.add_child(node_5)
    assert node_7.right is None
    node_7.add_child(node_6)

    assert node_7.left is node_5
    assert node_7.left == node_5
    assert node_7.right is node_6
    assert node_7.right == node_6
    assert node_5.left is None and node_5.right is None
    assert node_6.left is None and node_6.right is None

    node_8 = Node(name="Node8", altitude=300)
    node_9 = Node(name="NodeNef", altitude=120)
    node_10 = Node(name="NodeDIXX", altitude=10)
    assert node_10.left is None and node_10.right is None

    node_10.add_child(node_9)

    #   Test the "overflow add
    node_10.delete_child(node_9)
    node_10.add_child(node_8)
    node_10.delete_child(node_9)    # Ne sert Ã  rien mais doit marcher
    node_10.delete_child(node_9)    # Ne sert Ã  rien mais doit marcher

    #   Test for the proper deletion (left then right) and the proper addition (left then right)
    assert node_10.left is node_8
    assert node_10.left == node_8
    assert node_10.right is None

    #   Try adding a child to a node wo already have two childs
    node_10.add_child(7)
    with pytest.raises(AssertionError):
        node_10.add_child(7)


def test_bind_parent():
    node_1 = Node(name="III", altitude=300)
    node_2 = Node(name="IV", altitude=400)
    node_3 = Node(name="V", altitude=500)

    node_3.bind_parent(node_2)
    assert node_3.parent == node_2
    assert node_2.left == node_3

    #   Try to bind a parent to a node who already have a parent
    with pytest.raises(AssertionError):
        node_3.bind_parent(node_1)

    node_4 = Node()
    with pytest.raises(AssertionError):
        node_4.bind_parent(node_4)


def test_unbind_parent():
    node_1 = Node(name="I", altitude=100)
    node_2 = Node(name="II", altitude=200)

    node_1.bind_parent(node_2)
    assert node_1.parent is node_2

    node_1.unbind_parent()
    assert node_1.parent is None
    assert node_2.left is None

    #   Try to unbind a parent to a node who don't hve a parent => work
    node_1.unbind_parent()
    node_2.unbind_parent()


def test_bind_child():
    node_1 = Node(name="I", altitude=100)
    node_2 = Node(name="II", altitude=200)
    node_3 = Node(name="III", altitude=300)

    node_1.bind_child(node_2)
    assert node_1.left == node_2
    assert node_2.parent is node_1

    node_1.bind_child(node_3)
    assert node_1.left == node_2
    assert node_2.parent is node_1
    assert node_1.left == node_2
    assert node_2.parent is node_1


def test_unbind_child():
    node_1 = Node(name="I", altitude=100)
    node_2 = Node(name="II", altitude=200)
    node_3 = Node(name="III", altitude=300)

    node_1.bind_child(node_2)
    node_1.bind_child(node_3)

    node_1.unbind_child(node_2)
    assert node_1.left is None
    assert node_2.parent is None

    node_1.unbind_child(node_3)
    assert node_1.right is None
    assert node_3.parent is None

    with pytest.raises(AssertionError):
        node_1.unbind_child(None)

    with pytest.raises(AssertionError):
        node_1.unbind_child(node_2)


def test_copy():
    node_1 = Node(name="I", altitude=100)
    node_2 = Node(name="II", altitude=13350, parent=node_1)
    copy_of_node_2 = node_2.copy()
    assert copy_of_node_2.name == "II"
    assert copy_of_node_2.altitude == 13350
    assert copy_of_node_2.parent is None
    assert copy_of_node_2.left is None and copy_of_node_2.right is None
        

def test_is_leaf():
    node_1 = Node(name="I", altitude=100)
    assert node_1.is_leaf() is True
    node_2 = Node(name="II", altitude=13350, left=node_1)
    assert node_2.is_leaf() is False
