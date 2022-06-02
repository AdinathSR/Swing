from .strings_with_arrows import string_with_arrows

class Error:
    def __init__(self, name, details, pos, pos2 ):
        self.name = name
        self.details = details
    
    def asStr(self):
        return f'{self.name}: {self.details}'
    
class IllegalCharError(Error):
    def __init__(self,details,pos, pos2):
        super().__init__("IllegalCharError", details,  pos, pos2)
        
class InvalidSyntaxError(Error):
    def __init__(self,pos, pos2, details):
        super().__init__("InvalidSyntaxError", details, pos, pos2)

class RTError(Error):
	def __init__(self, pos_start, pos_end, details, context):
		super().__init__('Runtime Error', details, pos_start, pos_end)
		self.context = context

	def as_string(self):
		result  = self.generate_traceback()
		result += f'{self.error_name}: {self.details}'
		result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
		return result

	def generate_traceback(self):
		result = ''
		pos = self.pos_start
		ctx = self.context

		while ctx:
			result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
			pos = ctx.parent_entry_pos
			ctx = ctx.parent

		return 'Traceback (most recent call last):\n' + result
