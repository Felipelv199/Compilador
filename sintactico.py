import ply.yacc as yacc
from lexico import tokens


def p_gpoVar(p):
    '''GpoVar : GpoIds Delim PalRes Delim
    '''
    if p[2] != ':':
        print('<sintactico> Se esperan dos puntos antes de poner los tipos')
        return
    if p[4] != ';':
        print('<sintactico> Se espera un punto y coma terminando la sentecia')
        return
    p[0] = p[1] + p[2] + p[3] + p[4]


def p_grupoIds_Delim_Coma(p):
    'GpoIds : GpoIds Delim GpoId'
    if p[2] != ',':
        print('<sintactico> Se esperaba una coma para poder declarar varios IDs')
        return
    p[0] = p[1] + p[2] + p[3]


def p_grupoIds(p):
    'GpoIds : GpoId'
    p[0] = p[1]


def p_grupoId(p):
    '''GpoId : ID OpAsig CteEnt
    | ID OpAsig CteReal
    | ID OpAsig CteAlfa
    | ID OpAsig CteLog
    | ID'''
    p[0] = p[1]


def p_expArit(p):
    'GpoId : CteEnt OpArit CteEnt'
    if p[2] == '+':
        p[0] = p[1] + p[3]
    if p[2] == '-':
        p[0] = p[1] - p[3]
    if p[2] == '*':
        p[0] = p[1] * p[3]
    if p[2] == '/':
        p[0] = p[1] / p[3]


def p_error(p):
    print("Syntax error in input!")


def start_sintactic(f):
    parser = yacc.yacc()
    while True:
        try:
            s = input('calc > ')
        except EOFError:
            break
        if not s:
            continue
        print(s)
        result = parser.parse(s)
        print(result)
