'''Core functionality of the application.'''
from config import TITLE, INSTRUCTIONS, YES, NO, QUIT
from ui.console_io import ConsoleIO
from ui.example import Example
from entities.block import Block
from entities.downsampler import Downsampler
from entities.image_object import ImageObject

class App:
    '''Handle UI functionality for the command line application.'''
    def __init__(self):
        self._running = False
        self._io = ConsoleIO()
        self._ds = Downsampler()
        self._block = Block()

        im = ImageObject('src/data/rgb2-1024x1024.tif')
        self._example = Example(self._io, im, self._ds, self._block)

    def run(self):
        '''Run the application.'''
        self._running = True
        self._io.write(TITLE)
        self._io.write(INSTRUCTIONS)
        while self._running:
            prompt = '\nrun the example (y/n)?: '
            cmd = self._io.read(prompt)
            if cmd == YES:
                self._io.write('\nrunning example...')
                self._example.run()
            elif cmd == NO:
                self._run()
            elif cmd == QUIT:
                self._quit()
            else:
                self._io.write('\ninvalid input!')

    def _run(self):
        '''Run the application.'''
        self._io.write('\nonly example available!')

    def _quit(self):
        '''Quit the application.'''
        self._io.write('\nquitting app...')
        self._running = False
