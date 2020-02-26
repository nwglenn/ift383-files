# CREDIT: https://docs.python.org/3/tutorial/errors.html

'''
Custom exception for when the user inputs the wrong fomat of event times
'''

class Error(Exception):
    pass

class FormatError(Error):

    def __init__(self, message):
        self.message = message
