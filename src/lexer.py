from telnetlib import SE
from .errors import Error, IllegalCharError
from .tokens import Token
from .Parser import Parser
from .position import Position

DIGITS = '0123456789'
TT_INT		= 'INT'
TT_FLOAT    = 'FLOAT'
TT_PLUS     = 'PLUS'
TT_MINUS    = 'MINUS'
TT_MUL      = 'MUL'
TT_DIV      = 'DIV'
TT_LPAREN   = 'LPAREN'
TT_RPAREN   = 'RPAREN'
TT_EOF      = 'EOF'


class Lexer:
    def __init__(self, text, fn):
        self.text = text
        self.pos = Position(-1, 1, 1, fn, text)
        self.currentChar = None
        self.textIdx = -1
        
    def advance(self):
        self.pos.advance()
        self.currentChar = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
    
    def getTokens(self):
        self.advance()
        tokens = []
        while self.currentChar != None:
            if self.currentChar in ' /t':
                self.advance()
            elif self.currentChar in DIGITS:
                tokens.append(self.mkNum())
            elif self.currentChar == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.currentChar == '-':
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.currentChar == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.currentChar == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.currentChar == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.currentChar == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            else: return tokens, IllegalCharError('not a tok', 6,8) 
            
        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None
    
    def mkNum(self):
        num_str = ''
        dotCount = 0

        while self.currentChar != None and self.currentChar in DIGITS + '.':
            if self.currentChar == '.':
                if dotCount == 1: break
                dotCount += 1
                num_str += '.'
            else:
                num_str += self.currentChar
            self.advance()

        if dotCount == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))
    


            