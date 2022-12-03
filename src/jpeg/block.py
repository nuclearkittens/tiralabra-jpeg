import numpy as np

class Block():
    '''Class for a Minimum Coded Unit (MCU).

    args:
        h: int: height of the MCU; default = 8
        w: int: width of the MCU; default = 8
    '''
    def __init__(self, h=8, w=8):
        self._h = h
        self._w = w
        self._vpad = self._hpad = 0

    def split_blocks(self, im):
        '''Split an image matrix into blocks.

        args:
            im: array representation of an image

        return:
            blocks: ndarray: block pixel and colour channel data
            idx: ndarray: block coordinate data
        '''
        h, w, im = self.pad(im.shape[0], im.shape[1], im)
        channels = im.shape[2]

        blocks = []
        idx = []

        for j in range(0, h, self._h):
            for i in range(0, w, self._w):
                for ch in range(channels):
                    blocks.append(im[j:j+self._h, i:i+self._w, ch])
                    idx.append((j, i, ch))

        return np.array(blocks), np.array(idx)

    def reconstruct_im(self, blocks, idx):
        #TODO
        '''Reconstruct the image from MCUs.'''
        pass

    def pad(self, h, w, im):
        '''Add padding to image if dimensions are not 8Nx8M.'''
        vpad = h % self._h
        hpad = w % self._w
        if vpad != 0:
            im = self._vertical_pad(vpad, im)
        if hpad != 0:
            im = self._horizontal_pad(hpad, im)
        h, w = im.shape[0], im.shape[1]
        return h, w, im

    def remove_pad(self, im):
        '''Remove padding from reconstructed image.'''
        if self._hpad > 0:
            im = im[:-self._hpad,:,:]
            self._hpad = 0
        if self._vpad > 0:
            im = im[:,:-self._vpad,:]
            self._vpad = 0

    def _vertical_pad(self, pad, im):
        '''Add vertical padding by repeating last column of the image.'''
        self._vpad = pad
        return np.vstack((im, np.tile(im[-1], pad)))

    def _horizontal_pad(self, pad, im):
        '''Add horizontal padding by repeating last row of the image.'''
        self._hpad = pad
        return np.hstack((im, np.tile(im[:, [-1]], pad)))
