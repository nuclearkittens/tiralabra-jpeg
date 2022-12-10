import unittest
import numpy as np

from entities.block import Block

class TestBlock(unittest.TestCase):
    def setUp(self):
        self.test_mat1 = np.random.randint(256, size=(8, 8))
        self.test_mat2 = np.random.randint(256, size=(15, 12))
        self.test_im1 = np.dstack((self.test_mat1, self.test_mat1, self.test_mat1))
        self.test_im2 = np.dstack((self.test_mat2, self.test_mat2, self.test_mat2))
        self.test_block = Block()

    def test_block_init(self):
        self.assertEqual(self.test_block._h, 8)
        self.assertEqual(self.test_block._w, 8)
        self.assertEqual(self.test_block._vpad, 0)
        self.assertEqual(self.test_block._hpad, 0)

    def test_vertical_pad(self):
        padded = self.test_block._vertical_pad(self.test_im2)
        h = self.test_im2.shape[0]
        padded_h = padded.shape[0]
        self.assertTrue(padded_h-h == self.test_block._vpad)
        self.assertEqual(self.test_im2[:,-1].all(), padded[:,-1].all())

    def test_horizontal_pad(self):
        padded = self.test_block._horizontal_pad(self.test_im2)
        w = self.test_im2.shape[1]
        padded_w = padded.shape[1]
        self.assertTrue(padded_w-w == self.test_block._hpad)
        self.assertEqual(self.test_im2[-1].all(), padded[-1].all())

    def test_pad_no_pad(self):
        orig_h = self.test_im1.shape[0]
        orig_w = self.test_im1.shape[1]
        new_im = self.test_block.pad(self.test_im1)
        new_h = new_im.shape[0]
        new_w = new_im.shape[1]
        self.assertEqual((orig_h, orig_w, self.test_im1), (new_h, new_w, new_im))

    def test_remove_pad(self):
        padded = self.test_block.pad(self.test_im2)
        unpadded = self.test_block.remove_pad(padded)
        self.assertEqual(self.test_im2.all(), unpadded.all())

    #TODO: test_split_blocks

    def test_reconstruct_im(self):
        blocks, idx = self.test_block.split_blocks(self.test_im2)
        new_im = self.test_block.reconstruct_im(blocks, idx)
        self.assertEqual(self.test_im2.all(), new_im.all())