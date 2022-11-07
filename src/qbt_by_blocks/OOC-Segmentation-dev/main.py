import sys
# from Code.Image import *
from Code.Server import *
from numpy import *
import time

# from pycallgraph import PyCallGraph
# from pycallgraph.output import GraphvizOutput

sys.setrecursionlimit(15000)
img_sizes = [10, 400, 500]
#img_sizes = [100, 200]
# Set the image size
for i in img_sizes:
    IMAGE.len_x = i
    IMAGE.len_y = i
    x = 2
    y = 1
    print("Test_" + str(i) + "_" + str(i) + "_" + str(x) + "_" + str(y))
    file_name = "Test_"+str(i)+"_"+str(i)+"_"+str(x)+"_"+str(y)
    directory = "Data/" + str(file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    f = open(directory + "/" + str(file_name) + ".txt", "w")
    measurement = open(directory + "/" + str(file_name) + "_time.txt", "w")
    f.write("\n TEST"+str(i)+"_"+str(i)+"_"+str(x)+"_"+str(y)+"\n\n")
    # Set the number of block by line and by columns
    server2 = Server(IMAGE.len_x, IMAGE.len_y, x, y, f, measurement)

    # The weights:
    # o--0--o--1--o
    # |     |     |
    # 2     3     4
    # |     |     |
    # o--5--o--6--o

    # weights = [2, 3, 4, 2, 5, 10, 3, 2, 7, 6, 8, 21, 12, 10, 4, 2, 7, 3, 4, 2, 5, 10, 8, 2]
    # Set the weights
    weights = random.randint(0, high=255, size=(IMAGE.len_x*IMAGE.len_y*2)-(IMAGE.len_x+IMAGE.len_y))

    server2.initiate(weights)

