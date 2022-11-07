class Node:
    """
    A Node object represent a QBT node.
    :param name: Name of the node
    :type name: str
    
    :param altitude: Represent the QBT altitude (see QBT)
    :type altitude: int
    
    :param parent: The parent of the current Node
    :type parent: Node

    :param left: The left child of the current Node
    :type left: Node

    :param right: The right child of the current Node
    :type right: Node
    """
    def __init__(self, name=None, altitude=None, parent=None, left=None, right=None):
        """
        During the initialisation of a Node, if parent, left or right is not None, then
        the current node is binded with them. If parent is not none, bind_parent(parent)
        is used. Otherwise, bind_child(child) is used for both of the parents
        """
        self.name = name
        self.altitude = altitude

        self.parent = None
        if parent is not None:
            self.bind_parent(parent)

        self.left = None
        if left is not None:
            self.bind_child(left)

        self.right = None
        if right is not None:
            self.bind_child(right)

        self.aire = None
        self.hauteur = None
        self.volume = None

        # watershed
        self.minima = -1
        self.color = 0

    def is_leaf(self):
        """True if the Node is a is_leaf => childs are None"""
        return self.left is None and self.right is None

    def rec_height(self, i):
        assert i >= 0, "Rec_height canno be below zero"
        """Recursively get the height from the node to the childs"""
        if self.is_leaf():
            return i
        #   To avoid None comparisons, -1 better than None
        left = -1
        right = -1
        if self.left is not None:
            left = self.left.rec_height(i)
        if self.right is not None:
            right = self.right.rec_height(i)
        return max(left, right) + 1

    def add_child(self, node):
        """Add the Node node as a child of self if one of the children of self is
        None. It will assign the left child first, and the right child if the
        left child already exists"""
        assert self.can_add_child() is True

        if self.left is None:
            self.left = node
        elif self.right is None:
            self.right = node

    def other_child(self, child):
        if child is not None:
            if self.left is not None:
                if self.left.name == child.name:
                    return self.right
            if self.right is not None:
                if self.right.name == child.name:
                    return self.left
        else:
            return -1

    def child_exist(self, other):
        if other is not None:
            if self.left == other or self.right == other:
                return True
        else:
            return False

    def delete_child(self, node):
        if self.left == node:
            self.left = None
        elif self.right == node:
            self.right = None

    def can_add_child(self):
        if self.left is None or self.right is None:
            return True
        else:
            return False

    def bind_parent(self, node):
        # assert self.parent is None, "The parent must exist"
        assert node is not self, "The parent must not be the current node"
        self.parent = node
        self.parent.add_child(self)

    def unbind_parent(self):
        #assert self.parent is not None, "parent must not be None"
        if self.is_root():
            return
        assert self.parent.child_exist(self)
        self.parent.delete_child(self)
        self.parent = None

    def bind_child(self, node):
        assert node is not self, "The child must not be the current node"
        node.bind_parent(self)

    def unbind_child(self, child):
        assert child is not None, "Cannot unbind a unbinded link"
        assert self.child_exist(child) is True, "The child to delete must exist"
        assert child.parent is self, "The child must be linked to the parent"

        self.delete_child(child)
        child.parent = None

    def root(self):
        """Recursively return the root of the Node self"""
        if self.is_root():
            return self
        else:
            node = self
            while node.parent is not None:
                node = node.parent
            return node

    def is_root(self):
        if self.parent is None:
            return True
        else:
            return False

    def subtree(self):
        list_ = []
        node = self
        while node is not None:
            list_.append(node)
            node = node.parent
        return list_

    def __eq__(self, other):
        if other is None:
            return False
        if self.name == other.name and self.altitude == other.altitude:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.altitude < other.altitude:
            return True
        else:
            return False

    def is_(self, other):
        return self.name == other.name

    def __str__(self):
        """
        Print a Node with the following template:
            parent name, "name", [altitude], {child 1 name, child 2 name}
        """
        res = "["
        res += "Altitude : " + str(self.altitude) + ", "

        res += "Nom de la Node : '" + str(self.name) + "'" + ", Node parent : "
        if self.parent is not None:
            res += "[" + str(self.parent.name) + "], "
        else:
            res += "[None], "

        # A and not B
        if self.left is not None and self.right is None:
            res += "Nodes enfants : {" + str(self.left.name) + ", None}"
        # A and B
        elif self.left is not None and self.right is not None:
            res += "Nodes enfants : {" + str(self.left.name) + ", " + str(self.right.name) + "}"
        # not A and B
        elif self.left is None and self.right is not None:
            res += "Nodes enfants : {None, " + str(self.right.name) + "}"
        # not A and not B
        else:
            res += "Nodes enfants : {None, None}"
        if self.hauteur is not None:
            res += "Hauteur : " + str(self.hauteur) + ","
        else:
            res += "Hauteur : None,"
        if self.aire is not None:
            res += "Aire : " + str(self.aire)
        else:
            res += "Aire : None"
        if self.volume != None:
            res += "Volume : " + str(self.volume)
        else:
            res += "Volume : None"
        res += "]"
        return res

    def is_child(self, child):
        if self.left == child:
            return self.left
        elif self.right == child:
            return self.right
        return None

    def copy(self):
        n = Node(name=self.name, altitude=self.altitude)
        n.aire = self.aire
        n.hauteur = self.hauteur
        n.volume = self.volume
        return n

    def G_node(self):
        n = Node(name=self.name, altitude=min(self.left.altitude, self.right.altitude), left=self.left, right=self.right,
                 parent=self.parent)
        n.aire = min(self.left.aire, self.right.aire)
        n.hauteur = min(self.left.hauteur, self.right.hauteur)
        n.volume = min(self.left.volume, self.right.volume)
        return n

    def copy_all(self):
        n = Node(name=self.name, altitude=self.altitude, left=self.left,)

    def copy_names(self):
        parent = None
        left = None
        right = None
        if not self.is_root():
            parent = self.parent.name
        if self.left is not None:
            left = self.left.name
        if self.right is not None:
            right = self.right.name

        return [self.altitude, self.name, parent, left, right]

    def set_Surface(self):
        if self.left is not None:
            if self.right is not None:
                self.aire = self.left.set_Surface() + self.right.set_Surface()
            else:
                self.aire = self.left.set_Surface()
        else:
            if self.right is not None:
                self.aire = self.right.set_Surface()
            else:
                self.aire = 1
        return self.aire

    def set_Hauteur(self):
        if self.left is not None:
            if self.right is not None:
                self.hauteur = max(self.left.set_Hauteur(), self.right.set_Hauteur()) + 1
            else:
                self.hauteur = self.left.set_Hauteur() + 1
        else:
            if self.right is not None:
                self.hauteur = self.right.set_Hauteur() + 1
            else:
                self.hauteur = 1
        return self.hauteur

    def set_volume(self):
        if self.aire is not None and self.hauteur is not None:
            self.volume = self.aire * self.hauteur
        if self.left is not None:
            self.left.set_volume()
        if self.right is not None:
            self.right.set_volume()
        return self.volume

    def update_hauteur(self):
        if self.hauteur is not None:
            self.hauteur = -1
        if self.left is not None:
            if self.right is not None:
                self.hauteur = max(self.hauteur, max(self.left.update_hauteur(), self.right.update_hauteur()) + 1)
            else:
                self.hauteur = max(self.hauteur, self.left.update_hauteur() + 1)
        else:
            if self.right is not None:
                self.hauteur = max(self.hauteur, self.right.update_hauteur() + 1)
            else:
                self.hauteur = 1
        return self.hauteur
    
    def call_all_attribute_update(self):
        s = self.set_Surface()
        h = self.set_Hauteur()
        v = self.set_volume()
        return [s, h, v]
    
    def get_attribute(self):
        if self.is_root() or self.parent.altitude is not self.altitude:
            if self.left is not None:
                self.left.get_attribute()
            if self.right is not None:
                self.right.get_attribute()
            v = self.call_all_attribute_update()
            self.aire = v[0]
            self.hauteur = v[1]
            self.volume = v[2]
        else:
            maxi = [0, 0, 0]
            if self.left is not None:
                v = self.get_attribute()
                maxi = [max(v[i], maxi[i]) for i in range(len(v))]
            if self.right is not None:
                maxi = [max(v[i], maxi[i]) for i in range(len(v))]
                if v > maxi:
                    maxi = v
            self.aire = maxi[0]
            self.hauteur = maxi[1]
            self.volume = maxi[2]

        return self.call_all_attribute_update()