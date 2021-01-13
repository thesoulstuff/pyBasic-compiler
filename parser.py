import sys
from lex import *

class Parser:
    def __init__(self, lexer):
        pass

    def check_token(self, kind):
        pass

    def check_peek(self, kind):
        pass

    def match(self, kind):
        pass

    def next_token(self, kind):
        pass

    def abort(self, message):
        sys.exit('Error. {}'.format(message))

