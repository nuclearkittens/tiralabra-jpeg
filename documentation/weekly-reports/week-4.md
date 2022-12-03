# WEEKLY REPORT 4

Either I'm yet another victim of the Impostor Syndrome or I actually have no skills and knowledge whatsoever. Plus finding the ever-so-elusive motivation is still a struggle. Both loving and hating the topic I chose at the moment. Frustrated? Yes. Determined? Also yes.

In addition, to anyone who has the misfortune codereviewing this: sorry in advance. There is not a main program yet, nor much testing, so it might be a bit difficult to grasp what is happening. 

## Project progress

*should've finished subsampling & splitting into MCUs*

A fairly naïve implementation of chroma subsampling has been implemented. It is slow (with time complexity O(n<sup>2</sup>)), but it was the only implementation I managed to a) get to work and b) actually understood the functionality. I did try just taking every other row & column from the Cb and Cr matrices, but with actual images (compared to test matrices) there was no difference in the original and downsampled image, and I gave up on troubleshooting it at some point.

The third implementation uses 2D convolution, which resizes the chroma channels (in comparison to the earlier implementations, which repeated the values to keep the same shape & size). Almost as slow as the first implementation, so I guess this is not functional either.

I was not too happy with the ImageArray class, so (once again) refactoring took way too much time. It is still not how I want it to be (just dumped everything into utils, ugh), and no new tests have been written nor moved where they should be.

Started writing the module for MCUs, but it is very much unfinished and not tested at all. There might be some indexing errors in the padding methods, as I said, not tested as of Sat 26 Nov).

## This week I learnt...

So, in theory, chroma subsampling *seems* to be simple enough. Still haven't figured out an effective way to implement this without functions from external libraries – average box filtering/2D convolution seems to be the way, but I have completely forgotten everything I've learnt about them and cannot for the life of me write an implementation for anything like that. Thus, we have the current, slow solution. And another, 2D convolution based slow solution (naïve implementation as well). What have I learnt from this? I am not good at optimising, and there are too many ways to do any given thing. The research continues.

## Questions, problems, and such

## What next?

Testing, testing, testing. And reconstructing. And finishing the Block module. Then onto DCT and such.
