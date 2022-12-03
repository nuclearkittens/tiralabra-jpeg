'''Module for reading from & writing to the console.'''

class ConsoleIO:
    '''IO for the console.'''
    def write(self, value):
        '''Write given string value to console.'''
        print(value)

    def read(self, prompt):
        '''Read user input from console'''
        return input(prompt)
