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
            Prgrm : constantes variables FuncProc PROGRAMA Block FIN DE PROGRAMA
            '''
            p[0] = self.join_result(p)

        def p_Prgrm_error_Programa(p):
            '''
            Prgrm : constantes variables FuncProc error Block FIN DE PROGRAMA
            '''
            print("Mala sintaxis es neceario poner Programa")

        def p_Prgrm_error_Fin(p):
            '''
            Prgrm : constantes variables FuncProc PROGRAMA Block error DE PROGRAMA
                  | constantes variables FuncProc PROGRAMA Block FIN error PROGRAMA
                  | constantes variables FuncProc PROGRAMA Block FIN DE error
            '''
            print("Mala sintaxis es neceario poner Fin de Programa")

        def p_FuncProc(p):
            '''
            FuncProc : Func FuncProc
                     | Proc FuncProc
                     |
            '''
            p[0] = self.join_result(p)

        def p_Proc(p):
            '''
            Proc : PROCEDIMIENTO ID LPARENTHESIS Params RPARENTHESIS variables INICIO Block FIN DE PROCEDIMIENTO DOTCOMMA
            '''
            p[0] = self.join_result(p)

        def p_Func(p):
            '''
            Func : FUNCION ID LPARENTHESIS Params RPARENTHESIS 2DOTS TIPO variables INICIO Block FIN DE FUNCION DOTCOMMA
            '''
            p[0] = self.join_result(p)

        def p_Block(p):
            '''
            Block : Estatuto DOTCOMMA Block
                  |
            '''
            p[0] = self.join_result(p)

        def p_Estatuto(p):
            '''
            Estatuto : LIMPIAR
                     | INTERRUMPE
                     | CONTINUA
                     | Si
                     | Desde
                     | Repetir
                     | Mientras
                     | Cuando
                     | Regresa
                     | Asigna
                     | Lproc
                     | Imprime
                     | Imprimenl
                     | Lee
            '''
            p[0] = self.join_result(p)

        def p_Lee(p):
            '''
            Lee : LEE LPARENTHESIS RPARENTHESIS
                | LEE LPARENTHESIS ID RPARENTHESIS
            '''
            p[0] = self.join_result(p)

        def p_Imprimenl(p):
            '''
            Imprimenl : IMPRIMENL LPARENTHESIS RPARENTHESIS
                      | IMPRIMENL LPARENTHESIS GpoExp RPARENTHESIS
            '''
            p[0] = self.join_result(p)

        def p_Imprime(p):
            '''
            Imprime : IMPRIME LPARENTHESIS RPARENTHESIS
                    | IMPRIME LPARENTHESIS GpoExp RPARENTHESIS
            '''
            p[0] = self.join_result(p)

        def p_GpoExp(p):
            '''
            GpoExp : Exprlog
                   | Exprlog COMMA GpoExp
            '''
            p[0] = self.join_result(p)

        def p_Lproc(p):
            '''
            Lproc : ID LPARENTHESIS Uparams RPARENTHESIS
                  | ID LPARENTHESIS RPARENTHESIS
            '''
            p[0] = self.join_result(p)

        def p_Regresa(p):
            '''
            Regresa : REGRESA
                    | REGRESA LPARENTHESIS Exprlog RPARENTHESIS
            '''
            p[0] = self.join_result(p)

        def p_Cuando(p):
            '''
            Cuando : CUANDO EL VALOR DE ID INICIO GpoSea FIN
                   | CUANDO EL VALOR DE ID INICIO GpoSea CUALQUIER OTRO 2DOTS BckEsp FIN
            '''
            p[0] = self.join_result(p)

        def p_GpoSea(p):
            '''
            GpoSea : SEA GpoConst 2DOTS BckEsp GpoSea
                   |
            '''
            p[0] = self.join_result(p)

        def p_Mientras(p):
            '''
            Mientras : MIENTRAS SE CUMPLA QUE LPARENTHESIS Exprlog RPARENTHESIS BckEsp
            '''
            p[0] = self.join_result(p)

        def p_Repetir(p):
            '''
            Repetir : REPETIR Block HASTA QUE LPARENTHESIS Exprlog RPARENTHESIS
            '''
            p[0] = self.join_result(p)

        def p_Desde(p):
            '''
            Desde : DESDE EL VALOR DE Asigna HASTA Expr BckEsp
                  | DESDE EL VALOR DE Asigna HASTA Expr INCR CteEnt BckEsp
                  | DESDE EL VALOR DE Asigna HASTA Expr DECR CteEnt BckEsp
            '''
            p[0] = self.join_result(p)

        def p_Asigna(p):
            '''
            Asigna : ID OpAsig Exprlog
                   | ID Udim OpAsig Exprlog
            '''
            p[0] = self.join_result(p)

        def p_Si(p):
            '''
            Si : SI LPARENTHESIS Exprlog RPARENTHESIS HACER BckEsp
               | SI LPARENTHESIS Exprlog RPARENTHESIS HACER BckEsp SINO BckEsp
            '''
            p[0] = self.join_result(p)

        def p_BckEsp(p):
            '''
            BckEsp : Estatuto
                   | INICIO Block FIN
                   |
            '''
            p[0] = self.join_result(p)

        def p_Exprlog(p):
            '''
            Exprlog : Opy
                    | Opy O Exprlog
            '''
            p[0] = self.join_result(p)

        def p_Opy(p):
            '''
            Opy : Opno
                | Opno Y Opy
            '''
            p[0] = self.join_result(p)

        def p_Opno(p):
            '''
            Opno : Oprel
                 | NO Oprel
            '''
            p[0] = self.join_result(p)

        def p_Oprel(p):
            '''
            Oprel : Expr
                  | Expr OpRel Oprel
            '''
            p[0] = self.join_result(p)

        def p_Expr(p):
            '''
            Expr : Multi
                 | Multi PLUS Expr
                 | Multi MINUS Expr
            '''
            p[0] = self.join_result(p)

        def p_Multi(p):
            '''
            Multi : Expo ADD Multi
                  | Expo DIVIDE Multi
                  | Expo PERCENTAGE Multi
                  | Expo
            '''
            p[0] = self.join_result(p)

        def p_Expo(p):
            '''
            Expo : Signo
                 | Signo POW Expo
            '''
            p[0] = self.join_result(p)

        def p_Signo(p):
            '''
            Signo : MINUS Termino
                  | Termino
            '''
            p[0] = self.join_result(p)

        def p_Termino(p):
            '''
            Termino : ID
                    | ID Lfunc
                    | ID Udim
                    | LPARENTHESIS Exprlog RPARENTHESIS
                    | CteEnt
                    | CteReal
                    | CteAlfa
                    | CteLog
            '''
            p[0] = self.join_result(p)

        def p_Lfunc(p):
            '''
            Lfunc : ID LPARENTHESIS Uparams RPARENTHESIS
                  | ID LPARENTHESIS RPARENTHESIS
            '''
            p[0] = self.join_result(p)

        def p_Udim(p):
            '''
            Udim : Expr Udim
                 | Expr
            '''
            p[0] = self.join_result(p)

        def p_Uparams(p):
            '''
            Uparams : Exprlog
                    | Exprlog COMMA Uparams
            '''
            p[0] = self.join_result(p)

        def p_Params(p):
            '''
            Params : GpoPars 2DOTS TIPO Params
                   | 
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

        def p_constantes(p):
            '''
            constantes : CONSTANTES GpoConst
                       |
            '''
            p[0] = self.join_result(p)

        def p_gpoConst(p):
            '''
            GpoConst : GpoIds DOTCOMMA GpoConst
                     |
            '''
            p[0] = self.join_result(p)

        def p_variables(p):
            '''
            variables : VARIABLES GpoVars
                      |
            '''
            p[0] = self.join_result(p)

        def p_grupoVars(p):
            '''
            GpoVars : GpoIds 2DOTS TIPO DOTCOMMA GpoVars
                    | GpoIds 2DOTS TIPO DOTCOMMA
            '''
            p[0] = self.join_result(p)

        def p_grupoVars_error(p):
            '''
            GpoVars : GpoIds 2DOTS error DOTCOMMA GpoVars
                    | GpoIds 2DOTS error DOTCOMMA
            '''
            print("Syntax error in print statement. Bad expression")

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

        def p_error(p):
            if p:
                print("Syntax error in input!", p.type, p)
            else:
                print('End of file reached')

        parser = yacc.yacc()
        s = self.input
        result = parser.parse(s, lexer=lexer)
        print(result)
