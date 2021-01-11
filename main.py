from lex import *

def main():
    source = '=-*/'
    lexer = Lexer(source)
    token =lexer.get_token()

    while token.kind != Token_Type.EOF:
        print(token.kind)
        token = lexer.get_token()




if __name__ == '__main__':
    main()
