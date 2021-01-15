import sys
from lex import *

class Parser:
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

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
        self.emitter.header_line('#include <stdio.h>')
        self.emitter.header_line('int main(void){')

        while self.check_token(Token_Type.NEWLINE):
            self.next_token()

        # Parse all the statements
        while not self.check_token(Token_Type.EOF):
            self.statement()

        # Wrap up
        self.emitter.emit_line('return 0;')
        self.emitter.emit_line('}')

        for label in self.labels_gotoed:
            if label not in self.labels_declared:
                self.abort('Attempting to GOTO to undeclared lable: {}'.format(
                    label
                    )
                )


    def comparison(self,):

        self.expression()

        if self.is_comparison_operator():
            self.emitter.emit(self.cur_token.text)
            self.next_token()
            self.expression()
        else:
            self.abort('Expected comparison operator at: {}'.format(
                self.cur_token.text
                )
            )

        while self.is_comparison_operator():
            self.emitter.emit(self.cur_token.text)
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

        self.term()
        while self.check_token(Token_Type.PLUS) or self.check_token(Token_Type.MINUS):
            self.emitter.emit_line(self.cur_token.text)
            self.next_token()
            self.term()

    def term(self,):

        self.unary()

        while self.check_token(Token_Type.SLASH) or self.check_token(Token_Type.ASTERISK):
            self.emitter.emit(self.cur_token.text)
            self.next_token()
            self.unary()

    def unary(self,):

        if self.check_token(Token_Type.PLUS) or self.check_token(Token_Type.MINUS):
            self.emitter.emit(self.cur_token.text)
            self.next_token()
        self.primary()

    def primary(self,):

        if self.check_token(Token_Type.NUMBER):
            self.emitter.emit(self.cur_token.text)
            self.next_token()
        elif self.check_token(Token_Type.IDENT):

            if self.cur_token.text not in self.symbols:
                self.abort('Referencing variable before assignment: {}'.format(
                    self.cur_token.text
                    )
                )

            self.emitter.emit(self.cur_token.text)
            self.next_token()
        else:
            self.abort('Unexpected token at {}'.format(
                self.cur_token.text
                )
            )


    def statement(self,):
        # PRINT (expression | string)
        if self.check_token(Token_Type.PRINT):
            self.next_token()

            if self.check_token(Token_Type.STRING):
                self.emitter.emit_line('printf(\"{}\\n\");'.format(
                    self.cur_token.text
                    )
                )
                self.next_token()
            else:
                self.emitter.emit('printf(\"%.2f\\n\", (float)(')
                self.expression()
                self.emitter.emit_line('));')
        
        # IF comparison THEN {statemen} ENDIF
        elif self.check_token(Token_Type.IF):
            self.next_token()
            self.emitter.emit('if(')
            self.comparison()

            self.match(Token_Type.THEN)
            self.nl()
            self.emitter.emit_line('){')

            #Zero or more statements
            while not self.check_token(Token_Type.ENDIF):
                self.statement()

            self.match(Token_Type.ENDIF)
            self.emitter.emit_line('}')

        elif self.check_token(Token_Type.WHILE):
            self.next_token()
            self.emitter.emit('while(')
            self.comparison()

            self.match(Token_Type.REPEAT)
            self.nl()

            self.emitter.emit_line('){')


            while not self.check_token(Token_Type.ENDWHILE):
                self.statement()

            self.match(Token_Type.ENDWHILE)
            self.emitter.emit_line('}')

        elif self.check_token(Token_Type.LABEL):
            self.next_token()

            if self.cur_token.text in self.labels_declared:
                self.abort('Label already exists: {}'.format(
                    self.cur_token
                    )
                )
            self.labels_declared.add(self.cur_token.text)


            self.emitter.emit_line(self.cur_token.text+';')
            self.match(Token_Type.IDENT)


        elif self.check_token(Token_Type.GOTO):
            self.next_token()

            self.labels_gotoed.add(self.cur_token.text)
            self.emitter.emit_line('goto {};'.format(self.cur_token.text))

            self.match(Token_Type.IDENT)


        elif self.check_token(Token_Type.LET):
            self.next_token()

            if self.cur_token.text not in self.symbols:
                self.symbols.add(self.cur_token.text)
                self.emitter.header_line('float {};'.format(self.cur_token.text))


            self.emitter.emit('{} ='.format(self.cur_token.text))
            self.match(Token_Type.IDENT)
            self.match(Token_Type.EQ)
            self.expression()
            self.emitter.emit_line(';')


        
        elif self.check_token(Token_Type.INPUT):
            self.next_token()

            if self.cur_token.text not in self.symbols:
                self.symbols.add(self.cur_token.text)
                self.emitter.header_line('float {};'.format(self.cur_token.text))

            self.emitter.emit_line('if(0 == scanf(\"%f\", &{})) {{'.format(self.cur_token.text))
            self.emitter.emit_line('{} = 0;')
            self.emitter.emit('scanf(\"%')
            self.emitter.emit_line('*s\");')
            self.emitter.emit_line('}')
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

        self.match(Token_Type.NEWLINE)

        while self.check_token(Token_Type.NEWLINE):
            self.next_token()




