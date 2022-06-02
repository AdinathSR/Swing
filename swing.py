import src

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
        return None
    
    interpreter = src.Interpreter()
    context = src.Context('<program>')
    result = interpreter.visit(ast.node, context)
    
    print(result.value, result.error)

    
 
    
    
while True:
    run()
    