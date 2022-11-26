# WEEKLY REPORT 4

Either I'm yet another victim of the Impostor Syndrome or I actually have no skills and knowledge whatsoever. Plus finding the ever-so-elusive motivation is still a struggle. Both loving and hating the topic I chose at the moment. Frustrated? Yes. Determined? Also yes.

## Project progress

*should've finished subsampling & splitting into mcus*

A fairly naïve implementation of chroma subsampling has been implemented. It is slow (with time complexity O(n<sup>2</sup>)), but it was the only implementation I managed to a) get to work and b) actually understood the functionality. I did try just taking every other row & column from the Cb and Cr matrices, but with actual images (compared to test matrices) there was no difference in the original and downsampled image, and I gave up on troubleshooting it at some point.

The third implementation uses 2D convolution, which seems to be faster (despite the double for-loop), and resizes the chroma channels (in comparison to the earlier implementations, which repeated the values to keep the same shape & size). This seems to be faster, but I have not timed it yet so cannot say for sure.

I was not too happy with the ImageArray class, so (once again) refactoring took way too much time.

## This week I learnt...

So, in theory, chroma subsampling *seems* to be simple enough. Still haven't figured out an effective way to implement this without functions from external libraries – average box filtering/2D convolution seems to be the way, but I have completely forgotten everything I've learnt about them and cannot for the life of me write an implementation for anything like that. Thus, we have the current, slow solution. *EDIT: currently working on the 2D convolution.*

## Questions, problems, and such

## What next?
