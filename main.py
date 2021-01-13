import sys
from lex import *
from parser import *

def main():
    print('Teeny Tiny Compiler')

    if len(sys.lexer) != 2:
        sys.exit('Error: Compiler needs source file as argument.')
    with open(sys.argv[1], 'r') as inputFile:
        source = inputFile.read()

    lexer = Lexer(source)
    parser = Parser(lexer)

    parser.program()
    print('parsing completed.')




if __name__ == '__main__':
    main()
