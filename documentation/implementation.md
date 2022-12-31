# Implementation

Although originally I was going to implement both the encoding and decoding parts of the JPEG algorithm, I could not for the life of me figure out decoding the Huffman values, so only the encoding is implemented in the final program.

The program consists of several main functions that are specified below. An overview of the JPEG algorithm can be found in the [project specification](documentation/specification.md).

The bibliography and references for the project can be found [here](documentation/bibliography.md).

## Project structure

The main functionalities of the application can be found under `util`, which is further divided into modules by type of the utility (e.g. linear algebra, encoding/decoding algorithms, image-related functions). The `entities` consists of more object-like entities, including the `Compressor` and `Encoder` classes and two different types of image-like objects.

The main loop for the application is found under `ui`, as is the `ConsoleIO` object for writing to and reading from the console. Environmental variables are grouped together in `config.py`, and test images can be found in the `src/data` directory.

## Colour space transformation and downsampling

The colour space used in JPEG file format is YCbCr, meaning it has one channel for luminance and two for chrominance. As the human eye is more sensitive to luminance, compressing the chrominance channels have less visible effects on the resulting image. The chroma subsampling is done by removing values from the chroma channel matrices. It is not the most elegant solution, but a fairly fast one (see the [testing document](documentation/testing.md)).

The time complexity for the colour space transformation is O(n), where n is the number of pixels in the image. This is because the main operation being performed is the dot product between the image and the colour space transform matrix, which involves looping over every pixel in the image. The time complexity could potentially be affected by the the type of data being used (e.g. if the image is a very large high resolution image). Similarly, the time complexity for the subsampling is O(n).

## Block splitting and DCT

To perform DCT and quantisation on the images to further reduce the file size, the image has to be split into 8x8 blocks. 

Both the `splice_blocks()` and `combine_blocks()` iterate over every pixel of the image, so their time complexities are O(n), n being the number of pixels. These methods are implemented by using NumPy's built-in functions to reshape arrays and swap their axes, neither of them modifying the arrays in place and both having time complexities of O(n).

As the `quantise()` function relies on element-wise multiplication of matrices (which works in linear time), its time complexity is also O(n). This is true for the inverse as well, as the division is performed element-wise.

Discrete cosine transform (DCT) is used for compressing the image. The naïve method (using the official formula) has a time complexity of O(n<sup>2</sup>) for one-dimensional arrays and therefore O(n<sup>4</sup>) for matrices (=2D arrays). Therefore, the naïve method would be too slow for bigger matrices, and a recursive method using Fast Fourier Transform (FFT) and Discrete Fourier Transform (DFT) is implemented instead. This method has a time complexity of O(n<sup>2</sup> log n) for 2D DCT, since the time complexities for 1D FFT and DFT are O(n log n) and O(n<sup>2</sup>) respectively. Below are examples of runtimes for small square matrices.

Runtimes for different DCT methods:
| DCT | Size | Time (s) |
|---|---|---|
| naïve | 8 x 8 | 0.007 |
| FFT & DFT | 8 x 8 | 0.003 |
| naïve | 16 x 16 | 0.105 |
| FFT & DFT | 16 x 16 | 0.010 |
| naïve |32 x 32 | 1.743 |
| FFT & DFT | 32 x 32 | 0.038 |
| naïve | 64 x 64 | 25.08 |
| FFT & DFT | 64 x 64 | 0.149 |

## Huffman, run length and differential encoding

The time complexity of a Huffman coding algorithm depends on the specific implementation but in general, the time complexity is O(n log n), where n is the number of elements being encoded. This is because the algorithm involves building a binary tree to represent the frequencies of the encoded elements, and binary trees have a time complexity of O(n log n) for many common operations such as inserting and deleting elements.

The implementation used in my project relies on set Huffman tables (binary trees), so the time complexity should be O(n), n being the number of input elements. Most of the operations in the encoding method (such as formatting and string concatenation) work in constant time and hence do not affect the time complexity as a whole. However, with large amounts of data (pixels) to encode, the algorithm becomes slow.

Both the differential and run length encoding (as well as decoding) work in linear time (O(n)). In differential encoding the main operation is element-wise subtraction, which requires constant time per operation and is looped over every element of the input data, i.e. n times. Similar principle applies to run length encoding.

For the respective decoding algorithms, the differential decoding function uses Python's `itertools.accumulate()`, which has a time complexity of O(n), and the run length decoding performs a constant time operation (tuple creation) to every element of the input data, hence giving it a time complexity of O(n).

## Flaws & improvements

As mentioned earlier, the application does not have the decoding process implemented. Hence, the compressed images are not in a form that could be shown to the user nor saved to a file.

Reading and saving the compressed images is also something that could be added. Obviously part of this is the missing Huffman decoding, but another issue I had was figuring out *how* the JPEG file is actually written (headers, markers, exif data and such).