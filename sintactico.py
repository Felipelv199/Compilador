import ply.yacc as yacc
from lexico import tokens


class sintactico:
    def __init__(self, inpt, f_error):
        self.input = inpt
        self.file_error = f_error

    def write_sintactic_error(self, error_description):
        self.file_error.write('{:<10}|{:<30}|{:<40}|{}\n'.format(
            '', '', error_description, ''))

    def join_result(self, p):
        s = ''
        for i in range(1, len(p)):
            s += str(p[i])
        return s

    def start_sintactic(self, lexer):
        def p_Prgrm(p):
            '''
            Prgrm : variables FuncProc
                  | variables
                  | Block
            '''
            p[0] = self.join_result(p)

        def p_Block(p):
            '''
            Block : Estatuto DOTCOMMA
            '''
            p[0] = self.join_result(p)

        def p_Estatuto(p):
            '''
            Estatuto : SiEst
            '''
            p[0] = self.join_result(p)

        def p_SiEst(p):
            '''
            SiEst : SI LPARENTHESIS RPARENTHESIS HACER
            '''
            p[0] = self.join_result(p)

        def p_FuncProc(p):
            '''
            FuncProc : Func Proc
            '''
            p[0] = self.join_result(p)

        def p_Func(p):
            '''
            Func : FUNCION ID LPARENTHESIS Params RPARENTHESIS 2DOTS TIPO DOTCOMMA
                 | FUNCION ID LPARENTHESIS RPARENTHESIS 2DOTS TIPO DOTCOMMA
                 | FUNCION ID LPARENTHESIS Params RPARENTHESIS 2DOTS TIPO DOTCOMMA Func
                 | FUNCION ID LPARENTHESIS RPARENTHESIS 2DOTS TIPO DOTCOMMA Func
            '''
            p[0] = self.join_result(p)

        def p_Proc(p):
            '''
            Proc : PROCEDIMIENTO ID LPARENTHESIS Params RPARENTHESIS DOTCOMMA
                 | PROCEDIMIENTO ID LPARENTHESIS RPARENTHESIS DOTCOMMA
                 | PROCEDIMIENTO ID LPARENTHESIS Params RPARENTHESIS DOTCOMMA Proc
                 | PROCEDIMIENTO ID LPARENTHESIS RPARENTHESIS DOTCOMMA Proc
            '''
            p[0] = self.join_result(p)

        def p_Params(p):
            '''
            Params : GpoPars 2DOTS TIPO
                   | GpoPars 2DOTS TIPO Params
            '''
            p[0] = self.join_result(p)

        def p_grupoPars(p):
            '''
            GpoPars : GpoPar
                    | GpoPar COMMA GpoPars
            '''
            p[0] = self.join_result(p)

        def p_grupoPar(p):
            '''
            GpoPar : ID
            '''
            p[0] = self.join_result(p)

        def p_variables(p):
            '''
            variables : VARIABLES GpoVars
            '''
            p[0] = self.join_result(p)

        def p_grupoVars(p):
            '''
            GpoVars : GpoIds 2DOTS TIPO DOTCOMMA GpoVars
                    | GpoIds 2DOTS TIPO DOTCOMMA
            '''
            p[0] = self.join_result(p)

        def p_grupoIds(p):
            '''
            GpoIds : GpoId
                   | GpoPar
                   | GpoId COMMA GpoIds
                   | GpoPar COMMA GpoIds
            '''
            p[0] = self.join_result(p)

        def p_grupoId(p):
            '''
            GpoId : ID OpAsig CteEnt
                  | ID OpAsig CteReal
                  | ID OpAsig CteAlfa
                  | ID OpAsig CteLog
                  | ID Dimens
            '''
            p[0] = self.join_result(p)

        def p_Dimens_1D(p):
            '''
            Dimens : LBRACKET ID RBRACKET
                   | LBRACKET CteEnt RBRACKET
            '''
            p[0] = self.join_result(p)

        def p_Dimens_2D(p):
            '''
            Dimens : LBRACKET ID RBRACKET LBRACKET ID RBRACKET
                   | LBRACKET CteEnt RBRACKET LBRACKET CteEnt RBRACKET
            '''
            p[0] = self.join_result(p)

        def p_empty(p):
            'empty :'
            pass

        def p_error(p):
            print(p)
            print("Syntax error in input!")

        parser = yacc.yacc()
        s = self.input
        result = parser.parse(s, lexer=lexer)
        print(result)
