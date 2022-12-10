from ui.app import App

def main():
    app = App()
    app.run()

if __name__ == '__main__':
    main()
    # import numpy as np
    # from timeit import default_timer
    # from entities.block import Block
    # from util.util import dct2d, dct2d_slow

    # FIXME: delete random wk #6 dct tests below

    # mat1 = np.random.randint(256, size=(5, 5))
    # mat2 = np.random.randint(256, size=(5, 5))
    # mat3 = np.random.randint(256, size=(5, 5))
    # im = np.dstack((mat1, mat2, mat3))
    # block = Block()
    # blox, idx = block.split_blocks(im)
    # x = np.random.random(512)
    # mat = np.random.randint(256, size=(64,64))
    # start = default_timer()
    # dct2d_slow(mat)
    # end = default_timer()
    # print(f'dct2 slow: {end-start} s')
    # start = default_timer()
    # dct2d(mat)
    # end = default_timer()
    # print(f'dct2 fft/dft: {end-start} s')





