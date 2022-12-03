'''Core functionality of the application.'''
from config import TITLE, INSTRUCTIONS, YES, NO, QUIT

class App:
    '''Handle UI functionality for the command line application.'''
    def __init__(self, io):
        self._io = io
        self._running = False

    def run(self):
        self._running = True
        self._io.write(TITLE)
        self._io.write(INSTRUCTIONS)
        while self._running:
            prompt = '\n run the example (y/n)?: '
            cmd = self._io.read(prompt)
            if cmd == YES:
                self._run_example()
            elif cmd == NO:
                self._run()
            elif cmd == QUIT:
                self._quit()
            else:
                self._io.write('\n invalid input!')

    def _run(self):
        self._io.write('\n only example available!')

    def _run_example(self):
        self._io.write('\n running example...')

    def _quit(self):
        self._io.write('\n quitting app...')
        self._running = False
