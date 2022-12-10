'''MCU module.'''
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
        self._vpad = 0
        self._hpad = 0

    def split_blocks(self, im):
        '''Split an image matrix into blocks.

        args:
            im: array representation of an image

        return:
            blocks: ndarray: block pixel and colour channel data
            idx: ndarray: block coordinate data
        '''
        im = self.pad(im)
        h, w, chs = im.shape

        blocks = []
        idx = []

        for j in range(0, h, self._h):
            for i in range(0, w, self._w):
                for ch in range(chs):
                    blocks.append(im[j:j+self._h, i:i+self._w, ch])
                    idx.append((j, i, ch))

        return np.array(blocks), np.array(idx)

    def reconstruct_im(self, blocks, idx):
        #TODO
        '''Reconstruct the image from MCUs.'''
        pass

    def _check_pad(self, h, w):
        vpad = h % self._h
        hpad = w % self._w
        if vpad != 0:
            self._vpad = self._h - vpad
        if hpad != 0:
            self._hpad = self._w - hpad

    def pad(self, im):
        '''Add padding to image if dimensions are not 8Nx8M.'''
        h, w, _ = im.shape
        self._check_pad(h, w)

        if self._vpad:
            im = self._vertical_pad(im)
        if self._hpad:
            im = self._horizontal_pad(im)
        return im

    def remove_pad(self, im):
        '''Remove padding from reconstructed image.'''
        if self._hpad > 0:
            im = im[:-self._hpad,:,:]
            self._hpad = 0
        if self._vpad > 0:
            im = im[:,:-self._vpad,:]
            self._vpad = 0
        return im

    def _vertical_pad(self, im):
        '''Add vertical padding by repeating last column of the image.'''
        # self._vpad = pad
        # new_im = []
        # for i in range(im.shape[2]):
        #     ch = im[:,:,i]
        #     ch = np.hstack((ch, np.tile(ch[:,[-1]], pad)))
        #     new_im.append(ch)
        # return np.dstack(tuple(new_im))
        return np.concatenate((im, np.repeat(im[-1:], self._vpad, 0)), axis=0)

    def _horizontal_pad(self, im):
        '''Add horizontal padding by repeating last row of the image.'''
        # self._hpad = pad
        # new_im = []
        # for i in range(im.shape[2]):
        #     ch = im[:,:,i]
        #     ch = np.vstack((ch, np.tile(im[[-1]], pad)))
        #     new_im.append(ch)
        # return np.dstack(tuple(new_im))
        return np.concatenate((im, np.repeat(im[:,-1:], self._hpad, 1)), axis=1)
