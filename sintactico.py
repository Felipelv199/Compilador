import re
import ply.yacc as yacc
from lexico import tokens


class sintactico:
    def __init__(self, inpt, f_error):
        self.input = inpt
        self.file_error = f_error

    def write_sintactic_error(self, error_description):
        self.file_error.write('{:<10}|{:<30}|{:<40}|{}\n'.format(
            '', '', error_description, ''))

    def print_sintactic_error(self, p, error_description):
        print('ERROR: {} | {}'.format(
            p.lexer.lineno, error_description))

    def join_result(self, p):
        s = ''
        for i in range(1, len(p)):
            s += str(p[i])
        return s

    def start_sintactic(self, lexer):
        def p_Prgrm(p):
            '''
            Prgrm : constantes variables FuncProc PROGRAMA Block FIN DE PROGRAMA DOT
            '''
            p[0] = self.join_result(p)

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
                  | DOTCOMMA Block
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
                     | Lfunc
                     | Imprime
                     | Imprimenl
                     | Leer
            '''
            p[0] = self.join_result(p)

        def p_Lee(p):
            '''
            Leer : LEE LPARENTHESIS RPARENTHESIS
                 | LEE LPARENTHESIS ID RPARENTHESIS
            '''
            p[0] = self.join_result(p)

        def p_Imprimenl(p):
            '''
            Imprimenl : IMPRIMENL LPARENTHESIS GpoExp RPARENTHESIS
            '''
            p[0] = self.join_result(p)

        def p_Imprimenl_error1(p):
            '''
            Imprimenl : IMPRIMENL error GpoExp RPARENTHESIS
            '''
            self.print_sintactic_error(p, 'Falto "(" de apertura')

        def p_Imprimenl_error2(p):
            '''
            Imprimenl : IMPRIMENL LPARENTHESIS GpoExp error
            '''
            self.print_sintactic_error(p, 'Falto ")" de cerradura')

        def p_Imprime(p):
            '''
            Imprime : IMPRIME LPARENTHESIS GpoExp RPARENTHESIS
            '''
            p[0] = self.join_result(p)

        def p_GpoExp(p):
            '''
            GpoExp : Exprlog
                   | Exprlog COMMA GpoExp
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
                    | Lfunc
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
                  | ID LPARENTHESIS empty RPARENTHESIS 
            '''
            p[0] = self.join_result(p)

        def p_Lfunc_error1(p):
            '''
            Lfunc : ID error GpoExp RPARENTHESIS
            '''
            self.print_sintactic_error(p, 'Falto "(" de apertura')

        def p_Lfunc_error2(p):
            '''
            Lfunc : ID LPARENTHESIS GpoExp error
            '''
            self.print_sintactic_error(p, 'Falto ")" de cerradura')

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
            constantes : CONSTANTES GpoIds DOTCOMMA constantes
                       | GpoIds DOTCOMMA constantes
                       |
            '''
            p[0] = self.join_result(p)

        def p_gpoConst(p):
            '''
            GpoConst : Cte
                     | Cte COMMA GpoConst
            '''
            p[0] = self.join_result(p)

        def p_Cte(p):
            '''
            Cte : CteEnt
                | CteReal
                | CteAlfa
                | CteLog
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
                    |
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
            '''
            empty :
            '''

        def p_error(p):
            if not p:
                print('Fin del archivo')
            print(p.type, p.value, p.lineno)

        parser = yacc.yacc()
        s = self.input
        result = parser.parse(s, lexer=lexer)
        print(result)
