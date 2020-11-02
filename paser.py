# Yacc example

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from compilador import tokens


def p_factor_tipo(p):
    'factor : PalRes'
    p[0] = p[1]


def p_error(p):
    print("Syntax error in input!")


# Build the parser
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print(result)
