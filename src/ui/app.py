'''Core functionality of the application.'''
from timeit import default_timer as timer

from config import TITLE, INSTRUCTIONS, YES, NO, QUIT
from ui.console_io import ConsoleIO
from entities.compressor import Compressor
from entities.img import RawImage

class App:
    '''Handle UI functionality for the command line application.'''
    def __init__(self):
        self._running = False
        self._io = ConsoleIO()
        self._compressor = Compressor()

    def run(self):
        '''Run the application.'''
        self._running = True
        self._io.write(TITLE)
        self._io.write(INSTRUCTIONS)
        while self._running:
            prompt = '\nrun the example (y/n)?: '
            cmd = self._io.read(prompt)
            if cmd.lower() == YES:
                self._io.write('\nrunning example...')
                self.example()
            elif cmd.lower() == NO:
                self._run()
            elif cmd.lower() == QUIT:
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

    def example(self):
        quality = 50
        fpath = 'src/data/rgb2-1024x1024.tif'
        orig_im = RawImage(fpath=fpath)

        self._io.write('\nopened original image; compressing to 50% quality')
        self._show_im(orig_im.im)
        self._io.write(f'\nimage size: {orig_im.size} bytes')
        self._io.write(f'\nimage shape: {orig_im.shape}')

        self._io.write('\nencoding...')
        start = timer()
        compressed = self._compressor.compress(fpath, quality=quality)
        stop = timer()
        time = stop - start
        self._io.write(f'\ncompression took {time} seconds')
        self._io.write(f'\nencoded size: {compressed.size} bytes')

        self._io.write('\decoding image data...')
        start = timer()
        im = self._compressor.decompress(compressed)
        stop = timer()
        time = stop - start
        self._show_im(im)
        self._io.write(f'\ndecompression took {time} seconds')
        self._io.write(f'\image size: {im.size} bytes')
        self._io.write(f'\nimage shape: {im.shape}')

        #TODO: calc compression ratio
        self._io.write('\n**example finished**')


    def _show_im(self, im):
        cmd = self._io.read('show image (y/n)?: ')
        if cmd.lower() == YES:
            self._io.show_im(im)