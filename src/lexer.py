
import string
from .errors import *
from .tokens import Token
from .Parser import Parser
from .position import Position

LETTERS = string.ascii_letters
DIGITS = '0123456789'
LETTERS_DIGITS = LETTERS + DIGITS
TT_INT		= 'INT'
TT_FLOAT    = 'FLOAT'
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD = 'KEYWORD'
TT_PLUS     = 'PLUS'
TT_MINUS    = 'MINUS'
TT_MUL      = 'MUL'
TT_DIV      = 'DIV'
TT_EQ       = 'EQ'
TT_EE       = 'EE'
TT_NE       = 'NE'
TT_GT       = 'GT'
TT_LT       = 'LT'
TT_GTE      = 'GTE'
TT_LTE      = 'LTE'
TT_LPAREN   = 'LPAREN'
TT_RPAREN   = 'RPAREN'
TT_EOF      = 'EOF'

KEYWORDS = [
    'yehai',
    'aur',
    'ya',
    'na',
    'agar',
    'phir',
    'nahito',
    'nahito_agar',
    'jabtak'
]

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
            elif self.currentChar in LETTERS:
                tokens.append(self.mkIdentifier())
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
            elif self.currentChar == '=':
                tokens.append(self.mkEquals())
                self.advance()
            elif self.currentChar == '!':
                tok, error = self.mkNotEquals()
                if error: return [], error
                tokens.append(tok)
            elif self.currentChar == '>':
                tokens.append(self.mkGreaterThan())
                self.advance()
            elif self.currentChar == '<':
                tokens.append(self.mkLessThan())
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
    
    def mkIdentifier(self):
        idstr = ''
        posStart = self.pos.copy()
        tokType = None
        while self.currentChar != None and self.currentChar in LETTERS_DIGITS + '_':
            idstr += self.currentChar
            self.advance()
            
        tokType = TT_KEYWORD if idstr in KEYWORDS else TT_IDENTIFIER
        return Token(tokType, idstr, posStart, self.pos)
    
    def mkNotEquals(self):
        pos_start = self.pos.copy()
        self.advance()
        
        if self.currentChar == '=':
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None

        self.advance()
        return None, ExpectedCharError('expected \'=\'', pos_start, self.pos)
    
    def mkEquals(self):
        pos_start = self.pos.copy()
        self.advance()
        tokType = TT_EQ
        
        if self.currentChar == '=':
            self.advance()
            tokType = TT_EE   
            
        return Token(tokType, pos_start=pos_start, pos_end=self.pos)     
    
    def mkGreaterThan(self):
        pos_start = self.pos.copy()
        self.advance()
        tokType = TT_GT
        
        if self.currentChar == '=':
            self.advance()
            tokType = TT_GTE   
            
        return Token(tokType, pos_start=pos_start, pos_end=self.pos)    
    
    def mkLessThan(self):
        pos_start = self.pos.copy()
        self.advance()
        tokType = TT_LT
        
        if self.currentChar == '=':
            self.advance()
            tokType = TT_LTE 
            
        return Token(tokType, pos_start=pos_start, pos_end=self.pos)    