from .errors import *
import string
from .tokens import Token

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
    'na'
]

class Number:
	def __init__(self, value):
		self.value = value
		self.set_pos()
		self.set_context()

	def set_pos(self, pos_start=None, pos_end=None):
		self.pos_start = pos_start
		self.pos_end = pos_end
		return self

	def set_context(self, context=None):
		self.context = context
		return self

	def added_to(self, other):
		if isinstance(other, Number):
			return Number(self.value + other.value).set_context(self.context), None

	def subbed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value - other.value).set_context(self.context), None

	def multed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value * other.value).set_context(self.context), None

	def dived_by(self, other):
		if isinstance(other, Number):
			if other.value == 0:
				return None, RTError(
					other.pos_start, other.pos_end,
					'Division by zero',
					self.context
				)

			return Number(self.value / other.value).set_context(self.context), None

	def get_comparison_eq(self, other):
		if isinstance(other, Number):
			return Number(int(self.value == other.value)).set_context(self.context), None

	def get_comparison_ne(self, other):
		if isinstance(other, Number):
			return Number(int(self.value != other.value)).set_context(self.context), None

	def get_comparison_lt(self, other):
		if isinstance(other, Number):
			return Number(int(self.value < other.value)).set_context(self.context), None

	def get_comparison_gt(self, other):
		if isinstance(other, Number):
			return Number(int(self.value > other.value)).set_context(self.context), None

	def get_comparison_lte(self, other):
		if isinstance(other, Number):
			return Number(int(self.value <= other.value)).set_context(self.context), None

	def get_comparison_gte(self, other):
		if isinstance(other, Number):
			return Number(int(self.value >= other.value)).set_context(self.context), None

	def anded_by(self, other):
		if isinstance(other, Number):
			return Number(int(self.value and other.value)).set_context(self.context), None

	def ored_by(self, other):
		if isinstance(other, Number):
			return Number(int(self.value or other.value)).set_context(self.context), None

	def notted(self):
		return Number(1 if self.value == 0 else 0).set_context(self.context), None


	def __repr__(self):
		return str(self.value)

class NumberNode:
	def __init__(self, tok, pos_start, pos_end):
		self.tok = tok

		self.pos_start = pos_start
		self.pos_end = pos_end

	def __repr__(self):
		return f'{self.tok}'

class VarAccessNode:
    def __init__(self, varNameTok):
        self.var_name_tok = varNameTok
        
        self.pos_start = self.var_name_tok
        self.pos_end = self.var_name_tok.pos_end

class VarAssignNode:
    def __init__(self, varNameTok, valueNode):
        self.var_name_tok = varNameTok
        self.value_node = valueNode
        
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end

class BinOpNode:
	def __init__(self, left_node, op_tok, right_node):
		self.left_node = left_node
		self.op_tok = op_tok
		self.right_node = right_node

		self.pos_start = self.left_node.pos_start
		self.pos_end = self.right_node.pos_end

	def __repr__(self):
		return f'({self.left_node}, {self.op_tok}, {self.right_node})'

class UnaryOpNode:
	def __init__(self, op_tok, node):
		self.op_tok = op_tok
		self.node = node

		self.pos_start = self.op_tok.pos_start
		self.pos_end = node.pos_end

	def __repr__(self):
		return f'({self.op_tok}, {self.node})'

#######################################
# PARSE RESULT
#######################################

class ParseResult:
	def __init__(self):
		self.error = None
		self.node = None

	def register(self, res):
		if isinstance(res, ParseResult):
			if res.error: self.error = res.error
			return res.node

		return res

	def success(self, node):
		self.node = node
		return self

	def failure(self, error):
		self.error = error
		return self

#######################################
# PARSER
#######################################

class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.tok_idx = -1
		self.advance()

	def advance(self, ):
		self.tok_idx += 1
		if self.tok_idx < len(self.tokens):
			self.current_tok = self.tokens[self.tok_idx]
		return self.current_tok

	def parse(self):
		res = self.expr()
		if not res.error and self.current_tok.type != TT_EOF:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected '+', '-', '*' or '/'"
			))
		return res

	###################################

	def factor(self):
		res = ParseResult()
		tok = self.current_tok

		if tok.type in (TT_PLUS, TT_MINUS):
			res.register(self.advance())
			factor = res.register(self.factor())
			if res.error: return res
			return res.success(UnaryOpNode(tok, factor))

		elif tok.type == TT_IDENTIFIER:
			res.register(self.advance())
			return res.success(VarAccessNode(tok))
		
		elif tok.type in (TT_INT, TT_FLOAT):
			res.register(self.advance())
			return res.success(NumberNode(tok, tok.pos_start, tok.pos_end))

		elif tok.type == TT_LPAREN:
			res.register(self.advance())
			expr = res.register(self.expr())
			if res.error: return res
			if self.current_tok.type == TT_RPAREN:
				res.register(self.advance())
				return res.success(expr)
			else:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected ')'"
				))

		return res.failure(InvalidSyntaxError(
			tok.pos_start, tok.pos_end,
			"Expected int, float, identifier, '+', etc"
		))

	def term(self):
		return self.bin_op(self.factor, (TT_MUL, TT_DIV))

	def arith_expr(self):
		return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

	def comp_expr(self):
		res = ParseResult()

		if self.current_tok.matches(TT_KEYWORD, 'NOT'):
			op_tok = self.current_tok
			res.register(self.advance())

			node = res.register(self.comp_expr())
			if res.error: return res
			return res.success(UnaryOpNode(op_tok, node))
		
		node = res.register(self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))
		
		if res.error:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected int, float, identifier, '+', '-', '(' or 'NOT'"
			))

		return res.success(node)

	def expr(self):
		res = ParseResult()

		if self.current_tok.matches(TT_KEYWORD, 'VAR'):
			res.register(self.advance())

			if self.current_tok.type != TT_IDENTIFIER:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected identifier"
				))

			var_name = self.current_tok
			res.register(self.advance())

			if self.current_tok.type != TT_EQ:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected '='"
				))

			res.register(self.advance())
			expr = res.register(self.expr())
			if res.error: return res
			return res.success(VarAssignNode(var_name, expr))

		node = res.register(self.bin_op(self.comp_expr, ((TT_KEYWORD, 'AND'), (TT_KEYWORD, 'OR'))))

		if res.error:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected 'VAR', int, float, identifier, '+', '-', '(' or 'NOT'"
			))

		return res.success(node)

	###################################

	def bin_op(self, func_a, ops, func_b=None):
		if func_b == None:
			func_b = func_a
		
		res = ParseResult()
		left = res.register(func_a())
		if res.error: return res

		while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
			op_tok = self.current_tok
			res.register(self.advance())
			right = res.register(func_b())
			if res.error: return res
			left = BinOpNode(left, op_tok, right)

		return res.success(left)