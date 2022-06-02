import src
from src.Parser import Number

globalSymbolTable = src.SymbolTable()
globalSymbolTable.set("null", Number(0))

def run():
    inp = input('>>>')
    lexer = src.Lexer(inp, '<stdin>')
    tok, error = lexer.getTokens()
    if error:
        
        print(error.asStr())
        return

    parser = src.Parser(tok)
    ast = parser.parse()
    if ast.error:
        print(ast.error.asStr())
        return
    
    interpreter = src.Interpreter()
    context = src.Context('<program>')
    context.symbolTable = globalSymbolTable
    result = interpreter.visit(ast.node, context)
    if result.error:
        print(result.error.asStr())
        return
    print(result.value)

    
    
while True:
    run()
    