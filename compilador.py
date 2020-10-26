import os
import ply.lex as lex
from difflib import SequenceMatcher

tokens = [
    'Delim',
    'OpArit',
    'OpRel',
    'OpLog',
    'OpAsig',
    'CteEnt',
    'CteReal',
    'CteRealError',
    'CteAlfa',
    'CteAlfaError',
    'CteLog',
    'IDError',
    'ID',
]

PalRes = {
    "constantes": "CONSTANTES",
    "variables": "VARIABLES",
    "real": "REAL",
    "alfabetico": "ALFABETICO",
    "logico": "LOGICO",
    "entero": "ENTERO",
    "funcion": "FUNCION",
    "inicio": "INICIO",
    "fin": "FIN",
    "de": "DE",
    "procedimiento": "PROCEDIMIENTO",
    "regresa": "REGRESA",
    "si": "SI",
    "hacer": "HACER",
    "sino": "SINO",
    "cuando": "CUANDO",
    "el": "EL",
    "valor": "VALOR",
    "sea": "SEA",
    "otro": "OTRO",
    "desde": "DESDE",
    "hasta": "HASTA",
    "incr": "INCR",
    "decr": "DECR",
    "repetir": "REPETIR",
    "que": "QUE",
    "mientras": "MIENTRAS", "se": "SE",
    "cumpla": "CUMPLA",
    "continua": "CONTINUA",
    "interrumpe": "INTERRUMPE",
    "lee": "LEE",
    "imprime": "IMPRIME",
    "imprimenl": "IMPRIMENL",
    "programa": "PROGRAMA",
    "findeprograma": "FINDEPROGRAMA",
    'limpiaPantalla': 'LIMPIAPANTALLA',
}

tokens += PalRes.values()


def get_error_line(t):
    s = ''
    for i in range(len(t.lexer.lexdata)):
        s += t.lexer.lexdata[i]
        if t.lexer.lexdata[i] == '\n':
            s = ''
        elif i == t.lexer.lexpos:
            break
    return s.strip()


def write_lexical_error(t, error_description):
    error_lineno = t.lexer.lineno
    error = t.value.strip()
    error_line = get_error_line(t)
    error_file.write('{:<10}|{:<30}|{:<40}|{}\n'.format(
        error_lineno, error, error_description, error_line))


t_Delim = r'([.,;:()[]|])'
t_OpArit = r'[+-/%^*]'
t_OpRel = r'=|(<>)|<|>|(<=)|(>=)'
t_OpLog = r'y|(no)|o'
t_CteLog = r'(verdadero)|(false)'


def t_OpAsig(t):
    r':='
    return t


def t_IDError(t):
    r'[\d][a-zA-Z0-9_]*[ ]*((:=)|,|[(])'
    write_lexical_error(t, '<lexico>Un identificador no comienza con <digito>')


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.lower() in PalRes:
        lex_file.write("{:<40}|<{}>\n".format(t.value, 'PalRes'))
        return
    for palabra in PalRes:
        similarity = SequenceMatcher(None, t.value.lower(), palabra).ratio()
        if similarity > .85:
            write_lexical_error(
                t, '<lexico>Palabra reservada mal escrita, quisiste decir {}'.format(palabra))
            return
    return t


def t_CteRealError(t):
    r'\d+([.]|E)([^\d]*)(;|\n)'
    write_lexical_error(t, '<lexico>Se esperaba <digito>')


def t_CteReal(t):
    r'\d+([.]|E)\d+'
    return t


def t_CteEnt(t):
    r'\d+'
    return t


def t_CteAlfaError(t):
    r'["]([^"^;^\n]*)(;|\n)'
    write_lexical_error(t, '<lexico>Constante alf sin cerrar')


def t_CteAlfa(t):
    r'["]([^"]*)["]'
    return t


t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    error_file.write('{}\t\t{}'.format(t.lexer.lineno, t.value))
    t.lexer.skip(1)


file_name = "example1"
file = open("{}.up".format(file_name), "r")
lex_file = open("{}.lex".format(file_name), "w")
lex_file.write(
    "----------------------------------------------------------------------------\n")
lex_file.write(("{:<40}|{}\n").format('Lexema', 'Token'))
lex_file.write(
    "----------------------------------------------------------------------------\n")

error_file = open("{}.err".format(file_name), "w")
error_file.write(
    "----------------------------------------------------------------------------------------------------\n")
error_file.write(("{:<10}|{:<30}|{:<40}|{}\n").format(
    'Linea', 'Error', 'Descripcion', 'Linea Del Error'))
error_file.write(
    "----------------------------------------------------------------------------------------------------\n")

# Build the lexer
lexer = lex.lex()

lexer.input(file.read())

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    lex_file.write("{:<40}|<{}>\n".format(tok.value, tok.type))

lex_file.close()
error_file.close()
