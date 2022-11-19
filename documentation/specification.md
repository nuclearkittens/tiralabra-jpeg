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

A naïve implementation of 2D DCT has four nested loops, giving us a time complexity of O(n<sup>4</sup>) with a n x n matrix. However, by using a fast Fourier transform (FFT) to compute the DCTs, the time complexity can be reduced to O(n<sup>2</sup> log n) (jamesvphan, 2014;Mikulic, 2001). Space complexity equates to the size of the matrix, so it would be O(n<sup>2</sup>).

As for Huffman encoding, the algorithm is greedy – for a tree with n nodes, without sorting, each iteration takes O(log n) time and this is repeated n times, so the time complexity is O(n log n). (Morris, 1998)

*to be continued?*

## Bibliography & references

algo-rithm (2014). *performance - I am looking for a simple algorithm for fast DCT and IDCT of matrix [NxM].* [online] Stack Overflow. Available at: https://stackoverflow.com/questions/22768869/i-am-looking-for-a-simple-algorithm-for-fast-dct-and-idct-of-matrix-nxm [Accessed 11 Nov. 2022].

Cho, N.-I. and Lee, S.-U. (1991). Fast algorithm and implementation of 2-D discrete cosine transform. *IEEE Transactions on Circuits and Systems*, 38(3), pp.297–305. doi:10.1109/31.101322.

Framester (2012). *python - Fast Cosine Transform via FFT.* [online] Signal Processing Stack Exchange. Available at: https://dsp.stackexchange.com/questions/2807/fast-cosine-transform-via-fft/ [Accessed 11 Nov. 2022].

Girod, B. (n.d.). *EE398A Image and Video Compression Transform Coding no. 1.* [online] Available at: https://web.stanford.edu/class/ee398a/handouts/lectures/07-TransformCoding.pdf [Accessed 11 Nov. 2022].

International Telecommunications Union (2021). *H.273 : Coding-independent code points for video signal type identification.* [online] www.itu.int. Available at: https://www.itu.int/rec/T-REC-H.273-202107-I/en [Accessed 11 Nov. 2022].

jamesvphan (2014). *algorithm - How to compute Discrete Fourier Transform?* [online] Stack Overflow. Available at: https://stackoverflow.com/questions/26353003/how-to-compute-discrete-fourier-transform/ [Accessed 11 Nov. 2022].

Ji, X., Zhang, C., Wang, J. and Boey, S.H. (2009). Fast 2-D 8×8 discrete cosine transform algorithm for image coding. *Science in China Series F: Information Sciences*, 52(2), pp.215–225. doi:10.1007/s11432-009-0038-4.

Mikulic, E. (2001). *2D Discrete Cosine Transform.* [online] unix4lyfe.org. Available at: https://unix4lyfe.org/dct/ [Accessed 11 Nov. 2022].

Morris, J. (1998). *Data Structures and Algorithms: Introduction.* [online] www.cs.auckland.ac.nz. Available at: https://www.cs.auckland.ac.nz/software/AlgAnim/huffman.html [Accessed 12 Nov. 2022].

Papakostas, G.A., Koulouriotis, D.E. and Karakasis, E.G. (2009). Efficient 2-D DCT Computation from an Image Representation Point of View. *Image Processing.* doi:10.5772/7043.

Weisstein, E.W. (n.d.). *Huffman Coding.* [online] mathworld.wolfram.com. Available at: https://mathworld.wolfram.com/HuffmanCoding.html [Accessed 11 Nov. 2022].

Wikipedia (2019a). *Chroma subsampling.* [online] Wikipedia. Available at: https://en.wikipedia.org/wiki/Chroma_subsampling [Accessed 11 Nov. 2022].

Wikipedia (2019b). *JPEG.* [online] Wikipedia. Available at: https://en.wikipedia.org/wiki/JPEG [Accessed 11 Nov. 2022].

Wikipedia (2020). *YCbCr.* [online] Wikipedia. Available at: https://en.wikipedia.org/wiki/YCbCr [Accessed 11 Nov. 2022].
‌