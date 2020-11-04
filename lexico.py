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
    'PalRes',
    'PLUS',
    'Tipo'
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
    '.': 'DOT',
    ",": "COMMA",
    ":": "2DOTS",
    ";": "DOTCOMMA",
    "[": "LBRACKET",
    "]": "RBRACKET",
    "(": "LPARENTHESIS",
    ")": "RPARENTHESIS",
}

tokens += PalRes.values()


class lexico:

    def __init__(self, inpt, f_lex, f_error):
        self.input = inpt
        self.file_lex = f_lex
        self.file_error = f_error

    def get_error_line(self, t):
        s = ''
        for i in range(len(t.lexer.lexdata)):
            s += t.lexer.lexdata[i]
            if t.lexer.lexdata[i] == '\n' and i < t.lexer.lexpos-1:
                s = ''
            elif i >= t.lexer.lexpos-1 and t.lexer.lexdata[i] == ';' or t.lexer.lexdata[i] == '\n':
                break
        return s.strip()

    def write_lexical_error(self, t, error_description):
        if t.lexer.lineno == -1:
            return
        error_lineno = t.lexer.lineno
        error = t.value.strip()
        error_line = self.get_error_line(t)
        self.file_error.write('{:<10}|{:<30}|{:<40}|{}\n'.format(
            error_lineno, error, error_description, error_line))

    def start_lexico(self):

        t_OpArit = r'[+-/%^*]'
        t_OpRel = r'=|(<>)|<|>|(<=)|(>=)'
        t_OpLog = r'y|(no)|o'
        t_PLUS = r'[+]'

        def t_OpAsig(t):
            r':='
            return t

        def t_Delim(t):
            r'([.,;:()[]|])'
            t.type = PalRes[t.value]
            return t

        def t_CteLog(t):
            r'(verdadero)|(falso)'
            return t

        def t_IDError(t):
            r'[\d][a-zA-Z0-9_]*[ ]*((:=)|[(])'
            self.write_lexical_error(
                t, '<lexico>Un identificador no comienza con <digito>')

        def t_ID(t):
            r'[a-zA-Z_][a-zA-Z0-9_]*'
            if t.value.lower() in PalRes:
                if t.value.lower() == 'entero' or t.value.lower() == 'real' or t.value.lower() == 'alfabetico' or t.value.lower() == 'logico':
                    t.type = 'Tipo'
                    return t
                t.type = PalRes[t.value.lower()]
                return t
            for palabra in PalRes:
                similarity = SequenceMatcher(
                    None, t.value.lower(), palabra).ratio()
                if similarity > .85:
                    self.write_lexical_error(
                        t, '<lexico>Palabra reservada mal escrita, quisiste decir {}'.format(palabra))
                    return
            return t

        def t_CteRealError(t):
            r'\d+([.]|E)([^\d]*)(;|\n)'
            self.write_lexical_error(t, '<lexico>Se esperaba <digito>')

        def t_CteReal(t):
            r'\d+([.]|E)\d+'
            return t

        def t_CteEnt(t):
            r'\d+'
            t.value = int(t.value)
            return t

        def t_CteAlfaError(t):
            r'["]([^"^;^\n]*)(;|\n)'
            self.write_lexical_error(t, '<lexico>Constante alf sin cerrar')

        def t_CteAlfa(t):
            r'["]([^"]*)["]'
            return t

        t_ignore = ' \t'

        def t_newline(t):
            r'\n+'
            t.lexer.lineno += len(t.value)

        def t_error(t):
            print("Illegal character '%s'" % t.value[0])
            if t.lexer.lineno != -1:
                self.file_error.write(
                    '{}\t\t{}'.format(t.lexer.lineno, t.value))
            t.lexer.skip(1)

        # Build the lexer
        lexer = lex.lex()
        lexer.input(self.input)

        # Tokenize
        while True:
            tok = lexer.token()
            if not tok:
                lexer.lineno = -1
                break      # No more input
            self.file_lex.write("{:<40}|<{}>\n".format(tok.value, tok.type))
