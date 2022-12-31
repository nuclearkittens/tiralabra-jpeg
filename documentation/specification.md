# PROJECT SPECIFICATION
This project focusses on the lossless image compression format JPEG. The aim is to create an application that performs the steps included in image compression in an efficient manner.

+ **Degree programme:** BSc in Computer Science (tkt-kandi)
+ **Language:** English
    + peer/code reviews welcome in Finnish, too
+ **Programming language:** Python
    + not too familiar with other programming languages, so preferably Python for peer/code reviews

## Overview

When it comes to digital images, one of the most widely-used and popular format is JPEG. JPEG is a lossy compression method (meaning that some of the data in the image is lost), with adjustable degree of compression to manage both image quality and storage size. In this project, I aim to write a program that simulates the different steps used in JPEG image compression.

The JPEG compression can be divided into the encoding and decoding phases, which, similarly, can be split into several steps. The steps for encoding are:

+ **Colour space transformation and downsampling:** the image is converted from RGB (red, blue, and green channels) to YCbCr (luma, red-difference and blue-difference chroma). The reason behind this is the human ability to see colours, as we are more sensitive to brightness-related colour information (as opposed to hue and saturation). Hence, in YcbCr colour space we can delete some of the less important information (chroma subsampling).

+ **Block splitting:** colour channels are split into blocks – size depends on subsampling (8x8 with no subsampling), and different border-filling methods can be used (specified colour, repeating edge pixels, etc.).

+ **DCT:** component blocks are converted into their frequency-domain represtation using two-dimensi.onal discrete cosine transform (matrix operation)

+ **Quantisation:** dividing each frequency-domain element by the relevant quantisation matrix constant and rounding the floating point value to the nearest integer; this is the lossy part of the compression.

+ **Further compression:** lossless compression, Huffman encoding (or a variant of it) is used.

The decoding phase mirrors the encoding one, as it inverses the operations (excluding quantisation, as it is irreversible). (Wikipedia 2019a; 2019b; 2020)

## Data structures and algorithms

The main focus will be in understanding DCT and Huffman coding (and writing the algorithms for these operations). As for the matrices, vanilla Python is not the best option what with nested lists and writing functions for even the simplest matrix operations. NumPy offers n-dimensional arrays, so if that is allowed (given the complexity of the other parts of the project), that is what I am going to use.

## Time and space complexities

A naïve implementation of 2D DCT has four nested loops, giving us a time complexity of O(n<sup>4</sup>) with a n x n matrix. However, by using a fast Fourier transform (FFT) to compute the DCTs, the time complexity can be reduced to O(n<sup>2</sup> log n) (jamesvphan, 2014; Mikulic, 2001). Space complexity equates to the size of the matrix, so it would be O(n<sup>2</sup>).

As for Huffman encoding, the algorithm is greedy – for a tree with n nodes, without sorting, each iteration takes O(log n) time and this is repeated n times, so the time complexity is O(n log n). (Morris, 1998)
