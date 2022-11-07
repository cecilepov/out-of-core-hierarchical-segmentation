from Code.Tree import *

class Tree:
    """
    Tree object. A tree object is composed by a list of nodes and a root node
    :param list_of_nodes: The list of Nodes of the tree
    """
    def __init__(self, list_of_nodes):
        self.nodes = list_of_nodes
        self.root = self.nodes[-1]

    def height(self):
        """
        Return the height of the graph from the root node
        """
        return self.root.rec_height(0)

    def find_node(self, leaf_name):
        for node in self.nodes:
            if node.name == leaf_name:
                return node
        return None

    def get_leaves(self, root):
        if root.is_leaf():
            return [root]
        all_nodes = list()
        all_nodes.append(self.get_leaves(root.left))
        all_nodes.append(self.get_leaves(root.right))
        return all_nodes



    def subtree(self, leaves_name):
        sub_tree = []
        for l in leaves_name:
            ref = self.find_node(l)
            while ref is not None and ref not in sub_tree:
                sub_tree.append(ref)
                ref = ref.parent
        sub_tree.sort()
        return sub_tree
        
    def boundary_tree(self, leaves_name):
        boundary = []
        for l in leaves_name:
            # ref node
            ref = self.find_node(l)
            # child
            ref_o = None
            # for all
            while ref is not None and ref.copy() not in boundary:
                n = ref.copy()
                if ref_o is not None:
                    n.bind_child(ref_o)
                boundary.append(n)
                ref_o = n
                ref = ref.parent
            if ref is not None:
                parent = boundary.index(ref.copy())
                boundary[parent].bind_child(ref_o)
        boundary.sort()
        return Tree(boundary)

    def computeMergeAttributeMST(self):
        list_edge = []
        for node in self.nodes:
            if not node.is_leaf():
                list_edge.append(node.G_node())
        # creer graphe soucis
        return Tree(list_edge)

    def __str__(self):
        """
        Print the Tree in the form:
            Leaf 1
            Leaf 2
            ...
            Leaf n-1
            Leaf n
            <BLANKLINE>
        """
        res = ""
        for node in self.nodes:
            res += str(node) + "\n"
        return res