from Code.Node import *
from Code.Tree import *
from Code.GraphPrinter import *
import time

class Block:

    def __init__(self, graph, border, index, file_name):
        self.border = border
        self.index = index
        self.file_name = file_name
        self.tree = graph.do_QBT(self.border)
        self.tree.root.call_all_attribute_update()
        self.time_update_tree = 0
        self.ws = []

    def update_tree(self, new_subtree, leaves):
        start = time.time()
        new_list = self.tree.nodes
        for leaf in leaves:
            # search the leaf
            # selector_new goes up the new subtree as selector down and up work together at the original one
            selector_new = new_subtree.find_node(leaf)
            selector_down = self.tree.find_node(leaf)
            selector_up = selector_down

            # while we did not reach the root
            while selector_new is not None:
                # while they are reaching the same node the selectors go up the tree
                while selector_up == selector_new and selector_up is not None:
                    selector_up.aire = selector_new.aire
                    selector_up.hauteur = selector_new.hauteur
                    selector_up.volume = selector_new.volume
                    selector_new = selector_new.parent
                    # selector down has to always be the new child and selector up the new parent
                    selector_down = selector_up
                    selector_up = selector_up.parent

                if selector_new is not None:
                    # unbind the selector_down's parent so that a new node with the characteristics of new node can
                    # become it's new parent
                    selector_down.unbind_parent()
                    # create a new node while binding it as a child of the selector_up and becoming parent of
                    # selector_down
                    n = Node(name=selector_new.name, parent=selector_up, altitude=selector_new.altitude)
                    n.hauteur = selector_new.hauteur
                    n.volume = selector_new.volume
                    n.aire = selector_new.aire
                    selector_down.bind_parent(n)

                    # selector down now becomes the new node and its values are appended on the new nodes list
                    selector_down = selector_down.parent
                    new_list.append(selector_down)

                    # update selector new
                    selector_new = selector_new.parent

        new_list.sort()
        self.tree = Tree(new_list)
        end = time.time()
        self.time_update_tree = self.time_update_tree + (end - start)

    def watershed(self, attribute='hauteur'):
        for node in self.tree.nodes:
            if node.is_leaf():
                node.minima = 0
        for node in self.tree.nodes:
            nb = 0
            flag = True
            if node.left is not None:
                m = node.left.minima
                nb = nb + m
                if m == 0:
                    flag = False
            if node.right is not None:
                m = node.left.minima
                nb = nb + m
                if m == 0:
                    flag = False
            if flag:
                self.ws.append(node)
            if nb != 0:
                node.minima = nb
            else:
                if node.is_root():
                    node.minima = 1
                else:
                    if attribute == 'altitude':
                        if node.altitude < node.parent.altitude:
                            node.minima = 0
                        else:
                            node.minima = 1
                    elif attribute == 'hauteur':
                        if node.hauteur < node.parent.hauteur:
                            node.minima = 0
                        else:
                            node.minima = 1

                    elif attribute == 'aire':
                        if node.aire < node.parent.aire:
                            node.minima = 0
                        else:
                            node.minima = 1

    def remove_node(self, nodes):
        new_list = self.tree.nodes
        for node in nodes:
            selector_down = self.tree.find_node(node)
            if selector_down is not None:
                selector_up = selector_down.parent
                selector_down.unbind_parent()
                if selector_up is not None:
                    if selector_down.left is not None:
                            selector_down.left.bind_parent(selector_up)

                    else:
                            selector_down.right.bind_parent(selector_up)
                else:
                    if selector_down.left is not None:
                        selector_down.unbind_child(selector_down.left)
                    if selector_down.right is not None:
                        selector_down.unbind_child(selector_down.right)
                new_list.remove(selector_down)

        # new_list = self.tree.nodes
        new_list.sort()
        self.tree = Tree(new_list)

    def get_border_tree(self, list_border):
        return self.tree.boundary_tree(list_border)