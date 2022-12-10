from ui.app import App

def main():
    app = App()
    app.run()

if __name__ == '__main__':
    # main()
    import numpy as np
    from entities.block import Block

    mat1 = np.random.randint(256, size=(5, 5))
    mat2 = np.random.randint(256, size=(5, 5))
    mat3 = np.random.randint(256, size=(5, 5))
    im = np.dstack((mat1, mat2, mat3))
    block = Block()
    blox, idx = block.split_blocks(im)
    print(idx)

