import os
import ply.lex as lex

# os.system('flex compilador.l && gcc -o out lex.yy.c && out.exe examen.up')
# os.system('flex compilador.l && gcc -o out lex.yy.c && out.exe')

tokens = [
    'Delim',
    'OpArit',
    'OpRel',
    'OpLog',
    'OpAsig',
    'CteEnt',
    'CteReal',
    'CteAlfa',
    'CteLog',
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

t_Delim = r'([.,;:()[]|])'
t_OpArit = r'[+-/%^*]'
t_OpRel = r'=|(<>)|<|>|(<=)|(>=)'
t_OpLog = r'y|(no)|o'
t_CteLog = r'(verdadero)|(false)'


def t_OpAsig(t):
    r':='
    return t


def t_CteReal(t):
    r'\d+([.]|E)\d+'
    return t


def t_CteEnt(t):
    r'\d+'
    return t


def t_CteAlfa(t):
    r'["]([^"]*)["]'
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.lower() in PalRes:
        t.type = PalRes[t.value.lower()]

    return t


t_ignore = ' \t\n'


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
    "---------------------------------------------------------------------\n")
lex_file.write("Lexema\t\t\t\t\tToken\n")
lex_file.write(
    "---------------------------------------------------------------------\n")

error_file = open("{}.err".format(file_name), "w")
error_file.write(
    "---------------------------------------------------------------------\n")
error_file.write("Línea\tError\t\t\t\tDescripción\t\t\t\tLinea Del Error\n")
error_file.write(
    "---------------------------------------------------------------------\n")

# Build the lexer
lexer = lex.lex()

lexer.input(file.read())

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    lex_file.write("{}\t\t\t\t<{}>\n".format(tok.value, tok.type))
    print(tok.type, tok.value)

lex_file.close()
error_file.close()
