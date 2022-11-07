from Code.Block import *
import time
# New Server


class Merge:
    # New definition for the server
    # +image
    def __init__(self, all_blocks, weights, img_x, img_y, x_blocks, y_blocks, x_length, y_length, file, measurement):
        # Number of blocks by column and by row
        self.num_x_blocks = x_blocks
        self.num_y_blocks = y_blocks
        self.delta = self.delta1 = self.delta2 = 0
        # Size of the image x and y
        self.img_x = img_x
        self.img_y = img_y

        self.x_length = x_length
        self.y_length = y_length

        # Nodes that are being merged
        self.current_merge_name_1 = None
        self.current_merge_name_2 = None

        # Output file
        self.f = file

        # Initiate all_blocks
        self.all_blocks = all_blocks
        self.weights = weights

        self.measurement = measurement

    def merge_all(self):
        self.f.write("\n-------------------------------------------")
        for y in range(self.num_y_blocks):
            for x in range(self.num_x_blocks):

                self.f.write("\nBlock %d," % x)
                self.f.write("%d (Final)\n" % y)

                index = y * self.num_x_blocks + x
                block_1 = self.all_blocks[index]

                # First merge horizontally
                if x < self.num_x_blocks-1:
                    block_2 = self.all_blocks[index+1]
                    self.f.write(" Block " + str(index) + " and Block " + str(index+1))
                    # define border
                    edges = []
                    for j in range(self.y_length):
                        left = ((x+1)*self.x_length-1) + (y*self.y_length + j)*self.img_x
                        w = left + (j*(self.img_x-1))
                        right = left + 1
                        edges.append((left, right, self.weights[w]))

                    self.merging(block_1, block_2, edges)

                # Second merge vertically

                if y < self.num_y_blocks-1:
                    block_2 = self.all_blocks[index + self.num_x_blocks]
                    self.f.write(" Block " + str(index) + " and Block " + str(index + self.num_x_blocks))
                    # define border
                    edges = []
                    for i in range(self.x_length):
                        above = i + (((y+1)*self.y_length)-1)*self.img_x + (x*self.x_length)
                        below = above + self.img_x
                        w = above + (self.img_x - 1)

                        edges.append((above, below, self.weights[w]))

                    self.merging(block_1, block_2, edges)

    def refactoring(self, block_1, block_2, nodes_1, nodes_2):
        self.f.write("\nRefactoring")
        t = time.time()
        wrong_nodes = []
        copy_wrong_nodes = []
        subtree_1 = block_1.tree.subtree(nodes_1)
        subtree_2 = block_1.tree.subtree(nodes_2)
        print(len(subtree_1))
        for node1 in subtree_1:
            n = node1.name
            if n not in wrong_nodes:
                if node1.left is None or node1.right is None:
                    wrong_nodes.append(n)
                    copy_wrong_nodes.append(node1.copy_names())

        for node2 in subtree_2:
            n = node2.name
            if node2.left is None or node2.right is None:
                if n not in wrong_nodes:
                    wrong_nodes.append(n)
                    copy_wrong_nodes.append(node2.copy_names())
                else:
                    i = wrong_nodes.index(n)
                    if node2.left is not copy_wrong_nodes[i][3] and node2.left is not copy_wrong_nodes[i][4]:
                        if copy_wrong_nodes[i][3] is None:
                            copy_wrong_nodes[i][3] = node2.left
                        else:
                            copy_wrong_nodes[i][4] = node2.left
                    if node2.right is not copy_wrong_nodes[i][3] and node2.right is not copy_wrong_nodes[i][4]:
                        if copy_wrong_nodes[i][3] is None:
                            copy_wrong_nodes[i][3] = node2.right
                        else:
                            copy_wrong_nodes[i][4] = node2.right
        self.f.write("\tRemoving all nodes")

        w1 = []
        for w in copy_wrong_nodes:
            if w[3] is None and w[4] is None:
                w1.append(w)
            if w[3] != w[4] and w[3] is not None and w[4] is not None:
                w1.append(w)
        for w in w1:
            wrong_nodes.remove(w[1])
            copy_wrong_nodes.remove(w)

        block_1.remove_node(wrong_nodes)
        block_2.remove_node(wrong_nodes)

        t = time.time() - t
        self.measurement.write("\n\tRefactoring time: " + str(t))

    def merging(self, block_1, block_2, edges):

        edges.sort(key=lambda edges: edges[2])

        nodes_1 = [edge[0] for edge in edges]
        nodes_2 = [edge[1] for edge in edges]
        altitudes = [edge[2] for edge in edges]

        # edges belonging to block 1
        subtree_1 = block_1.get_border_tree(nodes_1)
        # edges belonging to block 2
        subtree_2 = block_2.get_border_tree(nodes_2)

        for i, edge in enumerate(edges):
            # names of the merging nodes in order to create the name of the new node
            self.current_merge_name_1 = str(edge[0])
            self.current_merge_name_2 = str(edge[1])

            self.f.write("\n\tNode " + str(self.current_merge_name_1) + " and Node " + str(self.current_merge_name_2))
            self.f.write("\n\t\tAt altitude " + str(altitudes[i]))

            # Initiating selectors up and down
            selector_1_down = subtree_1.find_node(edge[0])
            selector_2_down = subtree_2.find_node(edge[1])

            selector_1_up = selector_1_down.parent
            selector_2_up = selector_2_down.parent

            # Computing the border tree
            new_tree_nodes = self.compute(altitudes[i], selector_1_down, selector_2_down, selector_1_up, selector_2_up)

            # Updating Hauter
            new_tree_nodes.root.update_hauteur()

            # Updating blocks with their respective boundary trees
            # update_block_1 = new_tree_nodes.leaves_subtree(nodes_1)
            block_1.update_tree(new_tree_nodes, nodes_1)

            # update_block_2 = new_tree_nodes.leaves_subtree(nodes_2)
            block_2.update_tree(new_tree_nodes, nodes_2)
        self.refactoring(block_1, block_2, nodes_1, nodes_2)

    def compute(self, altitude, selector_1_down, selector_2_down, selector_1_up, selector_2_up):
        # Initializing variables
        new_tree_nodes = []
        node_created = False
        self.delta = self.delta_1 = self.delta_2 = 0
        current_node = None
        # do the merging while both selectors are not the same (the root)
        while (selector_1_up is not None and selector_2_up is not None) and not node_created:
            #  If the node is not created yet we go up in both trees until we find an altitude that is higher then what
            # we are merging
            if node_created is False:
                if selector_1_down not in new_tree_nodes:
                    new_tree_nodes.append(selector_1_down)
                if selector_2_down not in new_tree_nodes:
                    new_tree_nodes.append(selector_2_down)
                #  If both selectors up are roots of they respective trees or the altitudes are higher
                # , we create the node
                if (selector_1_up.is_root() or selector_1_up.altitude >= altitude) and (selector_2_up.is_root() or
                                                                                        selector_2_up.altitude >=
                                                                                        altitude):
                    [current_node, selector_1_down, selector_2_down, selector_1_up, selector_2_up] = self.create_node(
                                                                                        altitude, selector_1_down,
                                                                                        selector_2_down, selector_1_up,
                                                                                        selector_2_up)
                    new_tree_nodes.append(current_node)
                    current_node = current_node.parent
                    node_created = True
                    # STEP 3) Update the good selector
                    if selector_1_up is current_node:
                        [selector_1_down, selector_1_up] = self.update_selector(node_created,
                                                                                selector_1_down, selector_1_up,
                                                                                altitude)
                    elif selector_2_up is current_node:
                        [selector_2_down, selector_2_up] = self.update_selector(node_created,
                                                                                selector_2_down, selector_2_up,
                                                                                altitude)

                else:
                    [selector_1_down, selector_1_up] = self.update_selector(node_created, selector_1_down,
                                                                            selector_1_up, altitude)
                    [selector_2_down, selector_2_up] = self.update_selector(node_created, selector_2_down,
                                                                            selector_2_up, altitude)

                # In case the two nodes are already in each others trees
                while (selector_1_down is selector_2_down) and (selector_1_up is not None and selector_2_up is not None):
                    # if the selectors up are the same and are the root
                    if (selector_1_up.is_root() and selector_2_up.is_root()) and (selector_2_up is selector_1_up):
                        node_created = True

                    # while the selectors are not in the root
                    selector_1_down = selector_1_up
                    selector_1_up = selector_1_up.parent

                    selector_2_down = selector_2_up
                    selector_2_up = selector_2_up.parent
                    # add the nodes that are the same
                    if selector_1_down not in new_tree_nodes:
                        new_tree_nodes.append(selector_1_down)





            #  When the node was created but is not the root
            if selector_1_up is not selector_2_up:
                if node_created is True:
                    current_node.unbind_parent()
                    current_node.bind_parent(self.min_selectors_up(node_created, selector_1_up, selector_2_up,
                                                                   selector_1_down, selector_2_down, current_node))

                    # Updating Surface
                    # print(current_node.parent)
                    # get_subtreeprint(self.delta)
                    current_node.parent.aire = current_node.parent.aire+self.delta

                    new_tree_nodes.append(current_node)

                    [selector_1_down, selector_1_up] = self.update_selector(node_created, selector_1_down,
                                                                            selector_1_up, altitude)
                    [selector_2_down, selector_2_up] = self.update_selector(node_created, selector_2_down,
                                                                            selector_2_up, altitude)
                    if current_node.is_root() is False:
                        current_node = current_node.parent
                        if current_node.is_root():
                            new_tree_nodes.append(current_node)

        return Tree(new_tree_nodes)

    def create_node(self, altitude, selector_1_down, selector_2_down, selector_1_up, selector_2_up):
        # Define the parent of the new node by choosing the one with the lower altitude
        parent = self.min_selectors_up(False, selector_1_up, selector_2_up, selector_1_down, selector_2_down, None)

        # If the minimum selector has an altitude less than what we are looking for, this new node is a root, and the
        # parent is None
        if parent.altitude < altitude:
            parent = None
            selector_1_down = selector_1_up
            selector_2_down = selector_2_up

        # Create the node and link the node to his parent and to his childs
        if not selector_1_down.is_root():
            selector_1_down.unbind_parent()
        if not selector_2_down.is_root():
            selector_2_down.unbind_parent()

        # Create the new Node
        current_node = Node(name="("+self.current_merge_name_1+","+self.current_merge_name_2+")*",
                                 altitude=altitude,
                                 parent=parent,
                                 left=selector_1_down,
                                 right=selector_2_down)
        current_node.set_Surface()
        current_node.hauteur = max(selector_1_down.hauteur,selector_2_down.hauteur)+1
        self.delta1 = current_node.aire - selector_1_down.aire
        self.delta2 = current_node.aire - selector_2_down.aire

        if parent is None:
            selector_1_up = selector_2_up = current_node

        return list((current_node, selector_1_down, selector_2_down, selector_1_up, selector_2_up))

    def min_selectors_up(self, node_created, selector_1_up, selector_2_up, selector_1_down, selector_2_down, current_node):

        if node_created is False:
            #  If both are root => root is the next selector
            if selector_1_up.altitude == selector_2_up.altitude:
                s1 = str(selector_1_up.name)
                s2 = str(selector_2_up.name)
                s1 = int(s1[s1.find("(")+1: s1.find(",")])
                s2 = int(s2[s2.find("(")+1: s2.find(",")])
                if s1 > s2:
                    return selector_1_up
                else:
                    return selector_2_up
            elif selector_1_up.altitude > selector_2_up.altitude:
                return selector_2_up
            else:
                return selector_1_up
        else:
            if current_node.is_root() and current_node is selector_1_up:
                self.delta = self.delta2
                return selector_2_up

            if current_node.is_root() and current_node is selector_2_up:
                self.delta = self.delta1
                return selector_1_up

            if selector_1_up.altitude > selector_2_up.altitude:
                self.delta = self.delta2
                return selector_2_up
            else:

                self.delta = self.delta1
                return selector_1_up

    def update_selector(self, node_created, selector_down, selector_up, altitude):
        # If the altitude of the selector up is lower than the altitude of the edge, we increment the selector
        if node_created is False:
            if selector_up.altitude < altitude:
                selector_down = selector_up
                if selector_up.parent is not None:
                    selector_up = selector_up.parent
        else:
            selector_down = selector_up
            if selector_up.parent is not None:
                selector_up = selector_up.parent
        return selector_down, selector_up

