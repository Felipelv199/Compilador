import ply.yacc as yacc
from lexico import tokens


class sintactico:
    def __init__(self, inpt, f_error):
        self.input = inpt
        self.file_error = f_error

    def write_sintactic_error(self, error_description):
        self.file_error.write('{:<10}|{:<30}|{:<40}|{}\n'.format(
            '', '', error_description, ''))

    def start_sintactic(self):
        def p_Prgrm_(p):
            '''Prgrm : Prgrm variables 
            | Prgrm FuncProc
            '''
            p[0] = p[1]

        def p_Prgrm_Blocks(p):
            '''Prgrm : variables 
            | FuncProc
            '''
            p[0] = p[1]

        def p_FuncProc(p):
            '''
            FuncProc : FuncProc Func
            | FuncProc Proc
            '''
            p[0] = p[1]

        def p_FuncProc_Blocks(p):
            '''
            FuncProc : Func
            | Proc
            '''
            p[0] = p[1]

        def p_Proc(p):
            'Proc : PalRes ID Delim Params Delim Delim PalRes Delim'
            p[0] = p[1]

        def p_Func(p):
            'Func : PalRes ID Delim Params Delim Delim'
            p[0] = p[1]

        def p_Params_Delim(p):
            'Params : Params GpoPars Delim PalRes'
            p[0] = p[1]

        def p_Params(p):
            'Params : GpoPars Delim PalRes'
            p[0] = p[1]

        def p_GpoPars_Delim(p):
            'GpoPars : GpoPars ID'
            p[0] = p[1]

        def p_GpoPars(p):
            'GpoPars : ID'
            p[0] = p[1]

        def p_variables(p):
            '''variables : variables GpoVars
            | variables PalRes GpoVars'''
            p[0] = p[1] + p[2]

        def p_variables_Blocks(p):
            '''variables : GpoVars
            | PalRes GpoVars'''
            p[0] = p[1]

        def p_gpoVars_Tipes(p):
            'GpoVars : GpoVars GpoVar'
            p[0] = p[1] + p[2]

        def p_gpoVars(p):
            'GpoVars : GpoVar'
            p[0] = p[1]

        def p_gpoVar(p):
            'GpoVar : GpoIds Delim PalRes Delim'
            if p[2] != ':':
                self.write_sintactic_error(
                    '<sintactico> Se esperan dos puntos antes de poner los tipos')
                return
            if p[4] != ';':
                self.write_sintactic_error(
                    '<sintactico> Se espera un punto y coma terminando la sentecia')
                return
            p[0] = p[1] + p[2] + p[3] + p[4]

        def p_grupoIds_Delim_Coma(p):
            'GpoIds : GpoIds Delim GpoId'
            if p[2] != ',':
                self.write_sintactic_error(
                    '<sintactico> Se esperaba una coma para poder declarar varios IDs')
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
            | ID
            '''
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

        parser = yacc.yacc()
        lines = self.input.split("\n")
        while True:
            try:
                s = lines.pop(0)
            except:
                break
            if not s:
                continue
            result = parser.parse(s)
            print(result)
