parser = src.Parser(tok)
    ast = parser.parse()
    if ast.error:
        print(ast.error.asStr())
        return None
    
    interpreter = src.Interpreter()
    context = src.Context('<program>')
    result = interpreter.visit(ast.node, context)
    
    print(result.value, result.error)