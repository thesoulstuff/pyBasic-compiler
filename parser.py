import sys
from lex import *

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        self.symbols = set() # Variables
        self.labels_declared = set() # Labels declared
        self.labels_gotoed = set() # Goto

        self.cur_token = None
        self.peek_token = None

        self.next_token()
        self.next_token()

    def check_token(self, kind):
        return kind == self.cur_token.kind

    def check_peek(self, kind):
        return kind == self.peek_token.kind

    def match(self, kind):
        if not self.check_token(kind):
            self.abort('Expected {}, got {}'.format(
                kind.name, 
                self.cur_token.kind.name)
                )
        self.next_token()

    def next_token(self,):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.get_token()

    def abort(self, message):
        sys.exit('Error. {}'.format(message))

    # Production rules
    # program ::= {statement}
    def program(self,):
        print("PROGRAM")

        while self.check_token(Token_Type.NEWLINE):
            self.next_token()

        # Parse all the statements
        while not self.check_token(Token_Type.EOF):
            self.statement()

        for label in self.labels_gotoed:
            if label not in self.labels_declared:
                self.abort('Attempting to GOTO to undeclared lable: {}'.format(
                    label
                    )
                )


    def comparison(self,):
        print('COMPARSION')

        self.expression()

        if self.is_comparison_operator():
            self.next_token()
            self.expression()
        else:
            self.abort('Expected comparison operator at: {}'.format(
                self.cur_token.text
                )
            )

        while self.is_comparison_operator():
            self.next_token()
            self.expression()

    def is_comparison_operator(self,):
        return self.check_token(Token_Type.GT) or \
                self.check_token(Token_Type.GTEQ) or \
                self.check_token(Token_Type.LT) or \
                self.check_token(Token_Type.LTEQ) or \
                self.check_token(Token_Type.EQEQ) or \
                self.check_token(Token_Type.NOTEQ)

    def expression(self,):
        print("Expression")

        self.term()
        while self.check_token(Token_Type.PLUS) or self.check_token(Token_Type.MINUS):
            self.next_token()
            self.term()

    def term(self,):
        print('TERM')

        self.unary()

        while self.check_token(Token_Type.SLASH) or self.check_token(Token_Type.ASTERISK):
            self.next_token()
            self.unary()

    def unary(self,):
        print('UNARY')

        if self.check_token(Token_Type.PLUS) or self.check_token(Token_Type.MINUS):
            self.next_token()
        self.primary()

    def primary(self,):
        print('PRIMARY ({})'.format(self.cur_token.text))

        if self.check_token(Token_Type.NUMBER):
            self.next_token()
        elif self.check_token(Token_Type.IDENT):

            if self.cur_token.text not in self.symbols:
                self.abort('Referencing variable before assignment: {}'.format(
                    self.cur_token.text
                    )
                )

            self.next_token()
        else:
            self.abort('Unexpected token at {}'.format(
                self.cur_token.text
                )
            )


    def statement(self,):
        # PRINT (expression | string)
        if self.check_token(Token_Type.PRINT):
            print("STATEMENT PRINT")
            self.next_token()

            if self.check_token(Token_Type.STRING):
                self.next_token()
            else:
                self.expression()
        
        # IF comparison THEN {statemen} ENDIF
        elif self.check_token(Token_Type.IF):
            print('STATEMENT IF')
            self.next_token()
            self.comparison()

            self.match(Token_Type.THEN)
            self.nl()

            #Zero or more statements
            while not self.check_token(Token_Type.ENDIF):
                self.statement()

            self.match(Token_Type.ENDIF)

        elif self.check_token(Token_Type.WHILE):
            print('STATEMENT WHILE')
            self.next_token()
            self.comparison()

            self.match(Token_Type.REPEAT)
            self.nl()

            while not self.check_token(Token_Type.ENDWHILE):
                self.statement()

            self.match(Token_Type.ENDWHILE)

        elif self.check_token(Token_Type.LABEL):
            print("STATEMENT LABEL")
            self.next_token()

            if self.cur_token.text in self.labels_declared:
                self.abort('Label already exists: {}'.format(
                    self.cur_token
                    )
                )
            self.labels_declared.add(self.cur_token.text)


            self.match(Token_Type.IDENT)


        elif self.check_token(Token_Type.GOTO):
            print("STATEMENT GOTO")
            self.next_token()

            self.labels_gotoed.add(self.cur_token.text)

            self.match(Token_Type.IDENT)


        elif self.check_token(Token_Type.LET):
            print("STATEMENT LET")
            self.next_token()

            if self.cur_token.text not in self.symbols:
                self.symbols.add(self.cur_token.text)

            self.match(Token_Type.IDENT)
            self.match(Token_Type.EQ)
            self.expression()

        
        elif self.check_token(Token_Type.INPUT):
            print("STATEMENT INPUT")
            self.next_token()

            if self.cur_token.text not in self.symbols:
                self.symbols.add(self.cur_token.text)

            self.match(Token_Type.IDENT)
            
        else:
            self.abort('Invalid statement at {} ({})'.format(
                self.cur_token.text,
                self.cur_token.kind.name
                )
                )

        self.nl()

    # nl ::= '\n'
    def nl(self,):
        print("NEWLINE")

        self.match(Token_Type.NEWLINE)

        while self.check_token(Token_Type.NEWLINE):
            self.next_token()




