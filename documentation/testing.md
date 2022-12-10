# Testing document

## Unit tests

*to be continued*

Downsampler and ImageObject classes are tested, Block class mostly done.

Unit tests for the utility functions (mostly maths) are not included yet, but I will test them, possibly against in-built functions to check the maths are correct.

Coverage Sat Dec 10th, 2022:

![Screenshot of coverage report, showing 74% overall coverage](documentation/assets/coverage-2022-12-10-22-27-25.png)


## Manual testing

### Downsampling

There are several methods I tried for writing the algorithm for chroma subsampling. Currently the runtimes for these methods are displayed when running the example program. The fastest version (repeating values in the matrix) takes approximately 0.01 seconds for a 1024 x 1024 image, while the averaging method takes approximately 3.63 seconds and the convolution method 3.17 seconds with my setup.

### Discrete Cosine Transform

*to be continued*

Current runtimes for different DCT methods:
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