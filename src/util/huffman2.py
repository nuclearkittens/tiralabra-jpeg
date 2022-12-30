'''Huffman encoding.'''
from queue import PriorityQueue

class Node:
    '''Node of a Huffman tree.'''
    def __init__(self, val, freq, left, right):
        self._val = val
        self._freq = freq
        self._left = left
        self._right = right

    @classmethod
    def new_leaf(self, val, freq):
        '''Initialise a new leaf.'''
        return self(val, freq, None, None)

    @classmethod
    def new_node(self, left, right):
        '''Initialise a new node.'''
        freq = left.freq+right.freq
        return self(None, freq, left, right)

    def is_leaf(self):
        '''Check if node is a leaf.'''
        return self.val is not None

    def __lt__(self, other):
        return self.freq < other.freq

    @property
    def val(self):
        '''Return the value of the node.'''
        return self._val

    @property
    def freq(self):
        '''Return the frequency of the node.'''
        return self._freq

    @property
    def left(self):
        '''Return the left child of the node.'''
        return self._left

    @property
    def right(self):
        '''Return the right child of the node.'''
        return self._right

class HuffmanTree:
    '''Class for a Huffman tree.'''
    def __init__(self, arr):
        pq = PriorityQueue()

        for val, freq in self._calc_freq(arr).items():
            pq.put(Node.new_leaf(val, freq))

        while pq.qsize() >= 2:
            u = pq.get()
            v = pq.get()
            pq.put(Node.new_node(u, v))

        self._root = pq.get()
        self._huff_table = dict()

    @property
    def binstr(self):
        '''Return the binary string created from the tree values.'''
        return ''.join([val for val in self.huffman_table.values()])

    @property
    def huffman_table(self):
        '''Return a dictionary with tree values and corresponding codewords.'''
        if len(self._huff_table) == 0:
            self._create_huffman_table()
        return self._huff_table

    def _create_huffman_table(self):
        def traverse_tree(node, binstr=''):
            if node is None:
                return
            if node.is_leaf():
                self._huff_table[node.val] = binstr
                return
            traverse_tree(node.left, binstr+'0')
            traverse_tree(node.right, binstr+'1')

        traverse_tree(self._root)

    def _calc_freq(self, arr):
        freqs = dict()
        for val in arr:
            if val in freqs:
                freqs[val] += 1
            else:
                freqs[val] = 1
        return freqs
