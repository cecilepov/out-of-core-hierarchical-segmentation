from Code.Graph import *
from Code.Merge import *
import random
import time
import os
# New Server


class Server:
    # New definition for the server
    # +image
    def __init__(self, img_x, img_y, x_blocks, y_blocks, file_name, measurement):
        # Number of blocks by column and by row
        self.num_x_blocks = x_blocks
        self.num_y_blocks = y_blocks

        # Size of the image x and y
        self.img_x = img_x
        self.img_y = img_y

        # Number of blocks
        self.n_blocks = x_blocks * y_blocks

        # Size x and y of each block
        self.x_length = round(img_x / self.num_x_blocks)
        self.y_length = round(img_y / self.num_y_blocks)

        # Area of the block
        self.block_size = (self.x_length * self.y_length)

        # Initiate all_edges
        self.all_edges = []

        # Beging output file
        self.f = file_name
        self.measurement = measurement
        # Time class
        self.time = 0
        # Initiate all_blocks
        self.all_blocks = []
        self.ws = []

    def initiate(self, weights):
        start = time.time()
        assert len(weights) == (self.img_x*self.img_y*2)-(self.img_x+self.img_y)
        self.f.write("\nInitiating graph...")
        self.generate_all_edges()
        self.f.write("\nInitiating blocks...")
        self.generate_all_blocks(weights)
        self.f.write("\nMerging blocks...")
        merge = Merge(self.all_blocks, weights, self.img_x, self.img_y, self.num_x_blocks, self.num_y_blocks,
                      self.x_length, self.y_length, self.f, self.measurement)
        t = time.time()
        merge.merge_all()
        t = time.time() - t
        self.measurement.write("\nMerging total time: " + str(t))
        end = time.time()
        self.calcule_LPE()
        self.f.close()
        self.time = end - start
        self.measurement.write("\n--------------------------------------------\n")
        self.measurement.write("Total time: " + str(self.time))
        self.measurement.write("\n\nUPDATE TREE\n")
        for b in self.all_blocks:
            self.measurement.write("\nBlock " + str(b.index) + ": " + str(b.time_update_tree))

        self.measurement.close()

    def generate_all_edges(self):
        # 4-connected edges
        t = time.time()
        for i in range(self.block_size - 1):
            if i % self.x_length < self.x_length - 1:
                self.all_edges.append((i, i + 1))
            if i + self.x_length < self.block_size:
                self.all_edges.append((i, i + self.x_length))
        t = time.time() - t
        self.measurement.write("\nGenerate all edges: " + str(t) + "\n")

    def generate_block(self, x, y, weights):
        t = time.time()
        self.f.write("\nBlock %d," % x)
        self.f.write("%d (Original)\n" % y)
        block = self.define_block(x, y, weights)
        self.all_blocks.append(block)

        t = time.time() - t
        self.measurement.write("\nGenerate Block(" + str(y) + "," + str(y) + "): " + str(t))

    def generate_all_blocks(self, weights):
        t = time.time()
        for y in range(self.num_y_blocks):
            for x in range(self.num_x_blocks):
                self.f.write("\nBlock ("+str(x)+","+str(y)+")")
                weights_of_block = []
                # Where the block begins
                initial = (x * self.x_length) + (y * self.y_length) * self.img_x
                self.f.write("\nInitial node: " + str(initial))
                for j in range(self.y_length):
                    # first indexes on the horizontal
                    i = 0
                    w = initial + (2*self.img_x-1)*j + y*(self.img_x-1)
                    while i < self.x_length-1:
                        weights_of_block.append(weights[w])
                        i = i + 1
                        w = w + 1
                    # then indexes on the vertical
                    w = w + self.img_x-self.x_length
                    i = 0
                    if j < self.y_length-1:
                        while i < self.x_length:
                            weights_of_block.append(weights[w])
                            i = i + 1
                            w = w + 1

                self.f.write("\nNº of weights"+str(len(weights_of_block)))
                self.generate_block(x, y, weights_of_block)
        t = time.time() - t
        self.measurement.write("\nGenerate All Blocks:" + str(t) + "\n")

    def define_border(self, index_x, index_y):
        start_x = index_x*self.x_length
        start_y = index_y*self.y_length
        end_x = ((index_x+1) * self.x_length) - 1
        end_y = ((index_y+1) * self.y_length) - 1
        return Border(start_x, start_y, end_x, end_y)

    def random_weights(self, index_x):
        weights = []
        for i in range(self.block_size - 1):
            if i % self.x_length < self.x_length - 1:
                shift = index_x * self.x_length
                # pixel position in the image
                # 0 - 1 - 2 - 3
                # |   | | |   |
                # 4 - 5 - 6 - 7
                # if x_lenght = 2 then block 1
                # 0 - 1                         0 - 1
                # |   |  - but in the block ->  |   |
                # 4 - 5                         2 - 3
                # and block 2:
                # 2 - 3                         0 - 1
                # |   |  - but in the block ->  |   |
                # 6 - 7                         2 - 3
                # to find the real weights on the image we need the real values
                # THESE ARE NOT REAL NUMBERS!
                # random weights
                weights.append(random.randint(0, 255))
            if i + self.x_length < self.block_size:
                weights.append(random.randint(0, 255))

        return weights

    def define_graph(self, index_x, index_y, weights=[]):
        if weights is None:
            weights = self.random_weights(index_x)
        return Graph(n_vertices=self.block_size, edges=self.all_edges, weights=weights)

    def define_block(self, index_x, index_y, weight=[]):
        # define the edges of each block depending on its index
        # the blocks are defined by their position (x,y) in the image
        #
        border = self.define_border(index_x, index_y)
        graph = self.define_graph(index_x, index_y, weight)
        return Block(graph, border, (index_y*self.num_x_blocks+index_x), self.f)

    def calcule_LPE(self, ):
        color = 0
        double =[]
        for b in self.all_blocks:
            b.watershed()
            for node in b.ws:
                if node not in self.ws:
                    self.ws.append(node)
                    leaves = b.tree.get_leaves(node)
                    for l in leaves:
                        l.color = color
                    node.color = color
                else:
                    index = self.ws.index(node)
                    c = self.ws[index].color
                    leaves = b.tree.get_leaves(node)
                    for l in leaves:
                        l.color = c
                    node.color = c
            color = color+1

