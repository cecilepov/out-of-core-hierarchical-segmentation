# Out-of-core hierarchical watershed algorithm 

One-year research project at ESIEE Paris during academic year 2018-2019.

Supervisor: 
- Prof. Jean Cousty

Team members (4th year students)
- Carneiro Espíndola Stela
- Durrmeyer Alexandre
- Neghnagh-Chenavas Jules
- Mailharro Erwan
- Paris Édouard
- Paulin Florian
- Pov Cécile


## Motivation

2-min video presentation:
- https://drive.google.com/file/d/15PIrmB2qP4STvN3RqTBwlnvRwXnBuXy0/view?usp=sharing


Today, with the constant improvement in image acquisition systems , images resolution increased dramatically, producing 2D/3D images with large data volumes that can reach several dozens of GB.

Those images are intended for analysis and quantification using image processing techniques. However, they are so large that sometimes they can't even be loaded into a computer’s main memory at one time.

One idea is to "cut" the image in "blocks" and process them separately. Most algorithms are compatible with this block decomposition approach, but it is necessary for the others to fundamentally reconsider the algorithmic design.

This is particularly the case for image segmentation algorithms, such as the watershed algorithm. The appropriate way to process those large volume data is called "out-of-core". 

The purpose of this project is to investigate the feasibility of a new watershed algorithm with an out-of-core approach. 

We will:

- Access the state-of-the-art of global research on watershed algorithm variants and
strategies used to process large data on other image analysis problems;
- Design a new watershed segmentation algorithm, with an «out-of-core»/external
memory approach, so that we can process data that is too large to fit into a computer’s
memory at one time. This algorithm must produce exactly the same result
as if we had processed it without dividing the blocks (in core approach).
- Produce experimental results that shows or not the relevancy of the method chosen.


## Bibliography

[1] J. Cousty, L. Najman, Y. Kenmochi, S. Guimarães, Hierarchical segmentations with
graphs: quasi-flatzones, minimum spanning trees, and saliency maps, Journal of Mathematical
Imaging and Vision, Springer Verlag, 2017.

[2] J. Cousty, G. Bertrand, L. Najman, M. Couprie, Watershed Cuts: Minimum Spanning
Forests and the Drop of Water Principle, IEEE Transactions on Pattern Analysis
and Machine Intelligence, Institute of Electrical and Electronics Engineers, 2009.

[3] L. Najman, J. Cousty, B. Perret, Playing with Kruskal: algorithms for morphological
trees in edge-weighted graphs, C.L. Luengo Hendriks, G. Borgefors, R. Strand.
International Symposium on Mathematical Morphology, May 2013, Uppsala, Sweden.

[4] Kazemier, Jan J., Georgios K. Ouzounis, and Michael HF Wilkinson. "Connected
morphological attribute filters on distributed memory parallel machines." International
Symposium on Mathematical Morphology and Its Applications to Signal and Image Processing.
Springer, Cham, 2017.