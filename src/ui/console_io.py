'''Module for reading from & writing to the console.'''
from PIL import Image

class ConsoleIO:
    '''IO for the console.'''
    def write(self, value):
        '''Write given string value to console.'''
        print(value)

    def read(self, prompt):
        '''Read user input from console'''
        return input(prompt)

    def show_im(self, im):
        '''Open an image to view.'''
        Image.fromarray(im).show()
