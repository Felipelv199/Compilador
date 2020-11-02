# Yacc example

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from compilador import tokens




def p_expression_plus(p):
    'factor : CteEnt OpArit CteEnt'

    if p[2]=='+':
        p[0] = p[1] + p[3]
    if p[2]=='-':
        p[0] = p[1] - p[3]
    if p[2]=='*':
        p[0] = p[1] * p[3]
    if p[2]=='/':
        p[0] = p[1] / p[3]

def p_asignacionID(p):
    '''factor : ID OpAsig CteEnt
    | ID OpAsig CteReal
    | ID OpAsig CteAlfa
    | ID OpAsig CteLog'''
    p[0]=p[1]

def p_expression_term(p):
     'expression : term'
     print('valor: ' + p[1])
     p[0] = p[1]


def p_term_factor(p):
     'term : factor'
     p[0] = p[1]

def p_factor_tipo(p):
    'factor : PalRes'
    p[0] = p[1]

def p_factor_num(p):
     '''factor : CteEnt
                | CteReal '''
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
