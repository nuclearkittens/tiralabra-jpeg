from queue import PriorityQueue

class Node:
    def __init__(self, val, freq, left, right):
        self._val = val
        self._freq = freq
        self._left = left
        self._right = right

    @classmethod
    def new_leaf(self, val, freq):
        return self(val, freq, None, None)

    @classmethod
    def new_node(self, left, right):
        freq = left.freq+right.freq
        return self(None, freq, left, right)

    def is_leaf(self):
        return self.val is not None

    def __eq__(self, other):
        self_props = (self.val, self.freq, self.left, self.right)
        other_props = (other.val, other.freq, other.left, other.right)
        return self_props == other_props

    def __lt__(self, other):
        return self.freq < other.freq

    def __le__(self, other):
        return self.freq < other.freq or self.freq == other.freq

    @property
    def val(self):
        return self._val

    @property
    def freq(self):
        return self._freq

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

class HuffmanTree:
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
        return ''.join([val for val in self.huffman_table.values()])

    @property
    def huffman_table(self):
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
