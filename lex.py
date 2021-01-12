#lexer class
import enum, sys

class Lexer:
    def __init__(self, source):
        # initialize cursors and adding \n to the source to make it easier to parse
        self.source = source + '\n'
        self.cur_char = ''
        self.cur_pos = -1
        self.next_char()

    # Process next char
    def next_char(self):
        self.cur_pos += 1
        if self.cur_pos >= len(self.source):
            self.cur_char = '\0' # EOF
        else:
            self.cur_char = self.source[self.cur_pos]

    # Return lookahead char
    def peek(self):
        if self.cur_pos + 1 >= len(self.source):
            return '\0'
        return self.source[self.cur_pos+1]

    # Invalid Token
    def abort(self, message):
        sys.exit('Lexing error. ' + message)

    # Skip Whitespace
    def skip_white_space(self,):
        while self.cur_char == ' ' or self.cur_char == '\t' or self.cur_char == '\r':
            self.next_char()

    # Skip Comments
    def skip_comment(self,):
        if self.cur_char == '#':
            while self.cur_char != '\n':
                self.next_char()

    @staticmethod
    def check_keyword(token_text:str):
        '''
        token_text: str, identifier text
        returns
        Token_Type: check if the given token is or not a keyword
        '''
        for kind in Token_Type:
            if kind.name == token_text and kind.value >= 100 and kind.value < 200:
                return kind
        return None

    # Return next token
    def get_token(self,):
        self.skip_white_space()
        self.skip_comment()
        if self.cur_char == '+':
            token = Token(self.cur_char, Token_Type.PLUS)
        elif self.cur_char == '-':
            token = Token(self.cur_char, Token_Type.MINUS)
        elif self.cur_char == '*':
            token = Token(self.cur_char, Token_Type.ASTERISK)
        elif self.cur_char == '/':
            token = Token(self.cur_char, Token_Type.SLASH)
        elif self.cur_char == '\n':
            token = Token(self.cur_char, Token_Type.NEWLINE)
        elif self.cur_char == '\0':
            token = Token(self.cur_char, Token_Type.EOF)
        elif self.cur_char == "=":
            if self.peek() == '=':
                last_char = self.cur_char
                self.next_char()
                token = Token(last_char+self.cur_char, Token_Type.EQEQ)
            else:
                token = Token(self.cur_char, Token_Type.EQ)
        elif self.cur_char == '>':
            if self.peek() == '=':
                last_char = self.cur_char
                self.next_char()
                token = Token(last_char+self.cur_char, Token_Type.GTEQ)
            else:
                token = Token(self.cur_char, Token_Type.GT)
        elif self.cur_char == '<':
            if self.peek() == '=':
                last_char = self.cur_char
                self.next_char()
                token = Token(last_char+self.cur_char, Token_Type.LTEQ)
            else:
                token = Token(self.cur_char, Token_Type.LT)
        elif self.cur_char == '!':
            if self.peek() == '=':
                last_char = self.cur_char
                self.next_char()
                token = Token(last_char+self.cur_char, Token_Type.NOTEQ)
            else:
                self.abort('Expected !=, got {}'.format(self.peek()))
        elif self.cur_char == '\"':
            self.next_char()
            start_pos = self.cur_pos

            while self.cur_char != '\"':
                # No support for special character... maybe later
                if self.cur_char == '\r' or self.cur_char == '\n' or self.cur_char == '\t' or self.cur_char == '%': # Fix for pep8
                    self.abort('Illegal character in string')
                self.next_char()

            token_text + self.source[start_pos:self.cur_pos]
            token = Token(token_text, Token_Type.STRING)
        elif self.cur_char.isdigit():
            start_pos = self.cur_pos
            while self.peek().isdigit():
                self.next_char()
            if self.peek() == '.':
                self.next_char()

                if not self.peek().isdigit():
                    self.abort('Illegal character in number.')
                while self.peek().isdigit():
                    self.next_char()

            token_text = self.source[start_pos:self.cur_pos+1]
            token = Token(token_text, Token_Type.NUMBER)

        elif self.cur_char.isalpha():
            start_pos = self.cur_pos
            while self.peek().isalnum():
                self.next_char()

            token_text = self.source[start_pos:self.cur_pos+1]
            keyword = Token.check_keyword(token_text)
            if keyword is None:
                token = Token(token_text, Token_Type.IDENT)
            else:
                token = Token(token_text, keyword)


        else:
            # Unkown
            self.abort('Unkown token: {}'.format(self.cur_char))
        self.next_char()
        return token


#token class
# Maybe this should be a dataclass
class Token:
    def __init__(self, token_text, token_kind):
        self.text = token_text
        self.kind = token_kind


class Token_Type(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING =3
    # KEYWORD
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # OPERATORS
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211






