import re
import ply.yacc as yacc
from lexico import tokens
from ejecutable import Ejecutable


class sintactico:
    def __init__(self, inpt, f_error, s_t, eje):
        self.input = inpt
        self.file_error = f_error
        self.s_table = s_t
        self.eje = eje
        self.li_number = 0

    def write_sintactic_error(self, p, t, description):
        error_line_n = p.lexer.lineno
        error_line = []
        token = p.parser.token()
        while True:
            if not token:
                break
            error_line.append(str(token.value))
            if token.value == ';':
                break
            token = p.parser.token()
        self.file_error.write('{:<10}|{:<30}|{:<40}|{}\n'.format(
            str(error_line_n), t, description, ' '.join(error_line)))
        p.parser.errok()

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
            self.s_table.add_instruction('OPR', '0,0')
            self.s_table.add_tag(
                '_P', self.s_table.i_number - self.li_number)
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

        def p_Proc_Error1(p):
            '''
            Proc : PROCEDIMIENTO ID error Params RPARENTHESIS variables INICIO Block FIN DE PROCEDIMIENTO DOTCOMMA
            '''
            self.write_sintactic_error(
                p, '<(>', 'Falto parentesis de apertura en el procedimiento')

        def p_Proc_Error2(p):
            '''
            Proc : PROCEDIMIENTO ID LPARENTHESIS Params error variables INICIO Block FIN DE PROCEDIMIENTO DOTCOMMA
            '''
            self.write_sintactic_error(
                p, '<)>', 'Falto parentesis de cerradura en el procedimiento')

        def p_Proc_Error3(p):
            '''
            Proc : PROCEDIMIENTO ID LPARENTHESIS Params RPARENTHESIS variables INICIO Block FIN DE PROCEDIMIENTO error
            '''
            self.write_sintactic_error(
                p, '<;>', 'Falto punto y coma al terminar el procedimiento')

        def p_Func(p):
            '''
            Func : FUNCION ID LPARENTHESIS Params RPARENTHESIS 2DOTS TIPO variables INICIO Block FIN DE FUNCION DOTCOMMA
            '''
            p[0] = self.join_result(p)

        def p_Func_Error1(p):
            '''
            Func : FUNCION ID error Params RPARENTHESIS 2DOTS TIPO variables INICIO Block FIN DE FUNCION DOTCOMMA
            '''
            self.write_sintactic_error(
                p, '<(>', 'Falto parentesis de apertura en la función')

        def p_Func_Error2(p):
            '''
            Func : FUNCION ID LPARENTHESIS Params error 2DOTS TIPO variables INICIO Block FIN DE FUNCION DOTCOMMA
            '''
            self.write_sintactic_error(
                p, '<)>', 'Falto parentesis de cerradura en la función')

        def p_Func_Error3(p):
            '''
            Func : FUNCION ID LPARENTHESIS Params RPARENTHESIS error TIPO variables INICIO Block FIN DE FUNCION DOTCOMMA
            '''
            self.write_sintactic_error(
                p, '<:>', 'Faltaron dos puntos antes del tipo en la función')

        def p_Func_Error4(p):
            '''
            Func : FUNCION ID LPARENTHESIS Params RPARENTHESIS 2DOTS TIPO variables INICIO Block FIN DE FUNCION error
            '''
            self.write_sintactic_error(
                p, '<;>', 'Falto punto y coma al finalizar la función')

        def p_Block(p):
            '''
            Block : Estatuto DOTCOMMA Block
                  |
            '''
            p[0] = self.join_result(p)

        def p_Block_Error1(p):
            '''
            Block : Estatuto error Block
            '''
            self.write_sintactic_error(
                p, '<;>', 'Falto punto y coma al terminar el bloque')

        def p_Estatuto(p):
            '''
            Estatuto : INTERRUMPE
                     | CONTINUA
                     | Desde
                     | Repetir
                     | Mientras
                     | Cuando
                     | Regresa
                     | Lproc
                     | Asigna
                     | Imprime
                     | Imprimenl
                     | Leer
            '''
            p[0] = self.join_result(p)

        def p_Estatuto_Si(p):
            '''
            Estatuto : Si
            '''
            print(p[1], self.s_table.instructions)

        def p_Estatuto_limpiar(p):
            '''
            Estatuto : LIMPIAR
            '''
            self.s_table.add_instruction('OPR', '0,18')
            p[0] = self.join_result(p)

        def p_Lproc(p):
            '''
            Lproc : ID LPARENTHESIS Uparams RPARENTHESIS
                  | ID LPARENTHESIS empty RPARENTHESIS
            '''
            p[0] = self.join_result(p)

        def p_Lproc_Error1(p):
            '''
            Lproc : ID error Uparams RPARENTHESIS
                  | ID error empty RPARENTHESIS
            '''
            self.write_sintactic_error(
                p, '<(>', 'Falto parentesis de apertura en llamada a procedimiento')

        def p_Lproc_Error2(p):
            '''
            Lproc : ID LPARENTHESIS Uparams error
                  | ID LPARENTHESIS empty error
            '''
            self.write_sintactic_error(
                p, '<)>', 'Falto parentesis de cerradura en llamada a procedimiento')

        def p_Lee(p):
            '''
            Leer : LEE LPARENTHESIS ID RPARENTHESIS
                 | LEE LPARENTHESIS ID Udim RPARENTHESIS
            '''
            self.s_table.add_instruction('OPR', '{},19'.format(p[3]))
            self.li_number = self.s_table.i_number

        def p_Imprimenl(p):
            '''
            Imprimenl : IMPRIMENL LPARENTHESIS GpoExp RPARENTHESIS
                      | IMPRIMENL LPARENTHESIS empty RPARENTHESIS
            '''
            self.s_table.add_instruction('OPR', '0,21')
            self.li_number = self.s_table.i_number
            p[0] = self.join_result(p)

        def p_Imprimenl_error1(p):
            '''
            Imprimenl : IMPRIMENL error GpoExp RPARENTHESIS
                      | IMPRIMENL error empty RPARENTHESIS
            '''
            self.write_sintactic_error(
                p, '<(>', 'Falto parentesis de apertura en Imprimenl')

        def p_Imprimenl_error2(p):
            '''
            Imprimenl : IMPRIMENL LPARENTHESIS GpoExp error
                      | IMPRIMENL LPARENTHESIS empty error
            '''
            self.write_sintactic_error(
                p, '<)>', 'Falto parentesis de cerradura en Imprimenl')

        def p_Imprime(p):
            '''
            Imprime : IMPRIME LPARENTHESIS GpoExp RPARENTHESIS
                    | IMPRIME LPARENTHESIS empty RPARENTHESIS
            '''
            self.s_table.add_instruction('OPR', '0,20')
            self.li_number = self.s_table.i_number
            p[0] = self.join_result(p)

        def p_Imprime_error1(p):
            '''
            Imprime : IMPRIME error GpoExp RPARENTHESIS
                    | IMPRIME error empty RPARENTHESIS
            '''
            self.write_sintactic_error(
                p, '<(>', 'Falto parentesis de cerradura en Imprime')

        def p_Imprime_error2(p):
            '''
            Imprime : IMPRIME LPARENTHESIS GpoExp error
                    | IMPRIME LPARENTHESIS empty error
            '''
            self.write_sintactic_error(
                p, '<)>', 'Falto parentesis de cerradura en Imprime')

        def p_GpoExp(p):
            '''
            GpoExp : Exprlog
                   | Exprlog COMMA GpoExp
            '''
            p[0] = self.join_result(p)

        def p_Regresa(p):
            '''
            Regresa : REGRESA LPARENTHESIS Exprlog RPARENTHESIS
                    | REGRESA
            '''
            p[0] = self.join_result(p)

        def p_Regresa_Error1(p):
            '''
            Regresa : REGRESA error Exprlog RPARENTHESIS
            '''
            self.write_sintactic_error(
                p, '<(>', 'Falto parentesis de apertura en regresa')

        def p_Regresa_Error2(p):
            '''
            Regresa : REGRESA LPARENTHESIS Exprlog error
            '''
            self.write_sintactic_error(
                p, '<)>', 'Falto parentesis de cerradura en regresa')

        def p_Cuando(p):
            '''
            Cuando : CUANDO EL VALOR DE ID INICIO GpoSea FIN
                   | CUANDO EL VALOR DE ID INICIO GpoSea OTRO 2DOTS BckEsp FIN
            '''
            p[0] = self.join_result(p)

        def p_GpoSea(p):
            '''
            GpoSea : SEA GpoConst 2DOTS BckEsp GpoSea
                   | SEA GpoConst 2DOTS BckEsp
            '''
            p[0] = self.join_result(p)

        def p_GpoSea_Error1(p):
            '''
            GpoSea : SEA GpoConst error BckEsp GpoSea
            '''
            self.write_sintactic_error(p, ';', 'Falto punto y coma en sea')

        def p_Mientras(p):
            '''
            Mientras : MIENTRAS SE CUMPLA QUE LPARENTHESIS Exprlog RPARENTHESIS BckEsp
            '''
            p[0] = self.join_result(p)

        def p_Mientras_Error1(p):
            '''
            Mientras : MIENTRAS SE CUMPLA QUE error Exprlog RPARENTHESIS BckEsp
            '''
            self.write_sintactic_error(
                p, '<(>', 'Falto parentesis de apertura en mientras')

        def p_Mientras_Error2(p):
            '''
            Mientras : MIENTRAS SE CUMPLA QUE LPARENTHESIS Exprlog error BckEsp
            '''
            self.write_sintactic_error(
                p, '<)>', 'Falto parentesis de cerradura en mientras')

        def p_Repetir(p):
            '''
            Repetir : REPETIR Block HASTA QUE LPARENTHESIS Exprlog RPARENTHESIS
            '''
            p[0] = self.join_result(p)

        def p_Repetir_Error1(p):
            '''
            Repetir : REPETIR Block HASTA QUE error Exprlog RPARENTHESIS
            '''
            self.write_sintactic_error(
                p, '<(>', 'Falto parentesis de apertura en repetir')

        def p_Repetir_Error2(p):
            '''
            Repetir : REPETIR Block HASTA QUE LPARENTHESIS Exprlog error
            '''
            self.write_sintactic_error(
                p, '<)>', 'Falto parentesis de cerradura en repetir')

        def p_Desde(p):
            '''
            Desde : DESDE EL VALOR DE Asigna HASTA Expr BckEsp
                  | DESDE EL VALOR DE Asigna HASTA LPARENTHESIS Exprlog RPARENTHESIS  BckEsp
                  | DESDE EL VALOR DE Asigna HASTA Expr INCR CteEnt BckEsp
                  | DESDE EL VALOR DE Asigna HASTA Expr DECR CteEnt BckEsp
            '''
            p[0] = self.join_result(p)

        def p_Asigna_Udim(p):
            '''
            Asigna : ID Dimens OpAsig Exprlog
                   | ID empty OpAsig Exprlog
            '''
            self.s_table.add_instruction('STO', '0,{}'.format(p[1]))
            self.li_number = self.s_table.i_number

        def p_Asigna_Error1(p):
            '''
            Asigna : ID Dimens error Exprlog
                   | ID empty error Exprlog
            '''
            self.write_sintactic_error(
                p, '<:=>', 'Falto simbolo de asignacion en asignacion')

        def p_Si(p):
            '''
            Si : SI LPARENTHESIS Exprlog RPARENTHESIS HACER BckEsp
            '''
            self.s_table.e_number += 1
            self.s_table.add_instruction(
                'JMC', 'F,_E{}'.format(self.s_table.e_number))
            self.s_table.add_e_tag(self.s_table.i_number)
            self.s_table.e_number += 1
            self.s_table.add_instruction(
                'JMP', 'F,_E{}'.format(self.s_table.e_number))
            self.s_table.add_e_tag(self.s_table.i_number+1)
            self.li_number = self.s_table.i_number
            p[0] = self.join_result(p)

        def p_Si_sino(p):
            '''
            Si : SI LPARENTHESIS Exprlog RPARENTHESIS HACER BckEsp SINO BckEsp
            '''
            p[0] = self.join_result(p)

        def p_Si_Error1(p):
            '''
            Si : SI error Exprlog RPARENTHESIS HACER BckEsp
               | SI error Exprlog RPARENTHESIS HACER BckEsp SINO BckEsp
            '''
            self.write_sintactic_error(
                p, '<(>', 'Falto parentesis de apertura en Si')

        def p_Si_Error2(p):
            '''
            Si : SI LPARENTHESIS Exprlog error HACER BckEsp
               | SI LPARENTHESIS Exprlog error HACER BckEsp SINO BckEsp
            '''
            self.write_sintactic_error(
                p, '<)>', 'Falto parentesis de cerradura en Si')

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
            '''
            p[0] = self.join_result(p)

        def p_Exprlog_o(p):
            '''
            Exprlog : Opy O Exprlog
            '''
            self.s_table.add_instruction('OPR', '0,15')
            self.li_number = self.s_table.i_number
            p[0] = self.join_result(p)

        def p_Opy(p):
            '''
            Opy : Opno
            '''
            p[0] = self.join_result(p)

        def p_Opy_y(p):
            '''
            Opy : Opno Y Opy
            '''
            self.s_table.add_instruction('OPR', '0,16')
            self.li_number = self.s_table.i_number
            p[0] = self.join_result(p)

        def p_Opno(p):
            '''
            Opno : Oprel
            '''
            p[0] = self.join_result(p)

        def p_Opno_no(p):
            '''
            Opno : NO Oprel
            '''
            self.s_table.add_instruction('OPR', '0,17')
            self.li_number = self.s_table.i_number
            p[0] = self.join_result(p)

        def p_Oprel(p):
            '''
            Oprel : Expr
            '''
            p[0] = self.join_result(p)

        def p_Oprel_opRel(p):
            '''
            Oprel : Expr OpRel Oprel
            '''
            self.s_table.add_oprel_instruction(p[2])
            self.li_number = self.s_table.i_number
            p[0] = self.join_result(p)

        def p_Expr(p):
            '''
            Expr : Multi
            '''
            p[0] = self.join_result(p)

        def p_Expr_operations(p):
            '''
            Expr : Multi PLUS Expr
                 | Multi MINUS Expr
            '''
            self.s_table.add_math_instructions(p[2])
            self.li_number = self.s_table.i_number
            p[0] = self.join_result(p)

        def p_Multi(p):
            '''
            Multi : Expo
            '''
            p[0] = self.join_result(p)

        def p_Multi_operations(p):
            '''
            Multi : Expo ADD Multi
                  | Expo DIVIDE Multi
                  | Expo PERCENTAGE Multi
            '''
            self.s_table.add_math_instructions(p[2])
            self.li_number = self.s_table.i_number
            p[0] = self.join_result(p)

        def p_Expo(p):
            '''
            Expo : Signo
            '''
            p[0] = self.join_result(p)

        def p_Expo_pow(p):
            '''
            Expo : Signo POW Expo
            '''
            self.s_table.add_instruction('OPR', '0,7')
            self.li_number = self.s_table.i_number
            p[0] = self.join_result(p)

        def p_Signo(p):
            '''
            Signo : Termino
            '''
            p[0] = self.join_result(p)

        def p_Signo_minus(p):
            '''
            Signo : MINUS Termino
            '''
            type = ''
            if p[2] in self.s_table.table:
                value = self.s_table.table[p[2]].valor
                if value == '':
                    return
                type = self.s_table.get_cte_type(value)
            else:
                type = self.s_table.get_cte_type(p[2])

            if type != 'real' and type != 'entero':
                self.s_table.write_semantic_error(
                    p.lexer.lineno-1, self.join_result(p), '<semantico> Esta operacion no puede ser realizada por este tipo de dato')
                return
            self.s_table.add_instruction('OPR', '0,3')
            self.li_number = self.s_table.i_number
            p[0] = self.join_result(p)

        def p_Termino(p):
            '''
            Termino : Lfunc
                    | Dimens
            '''
            p[0] = self.join_result(p)

        def p_Termino_ID(p):
            '''
            Termino : ID
                    | ID Udim
            '''
            if p[1] not in self.s_table.table:
                self.s_table.write_semantic_error(
                    p.lexer.lineno-1, p[1], '<semantico> La variable o constante no a sido declarada')
                return
            id = p[1]
            self.s_table.add_instruction('LOD', '{},0'.format(id))
            self.li_number = self.s_table.i_number
            self.s_table.stack.append(self.s_table.table[p[1]].type)
            p[0] = self.join_result(p)

        def p_Termino_const(p):
            '''
            Termino : CteEnt
                    | CteReal
                    | CteAlfa
                    | CteLog
            '''
            self.s_table.add_instruction('LIT', '{},0'.format(p[1]))
            self.li_number = self.s_table.i_number
            p[0] = self.join_result(p)

        def p_Lfunc(p):
            '''
            Lfunc : ID LPARENTHESIS Uparams RPARENTHESIS
                  | ID LPARENTHESIS empty RPARENTHESIS
            '''
            p[0] = self.join_result(p)

        def p_Lfunc_Error1(p):
            '''
            Lfunc : ID error Uparams RPARENTHESIS
                  | ID error empty RPARENTHESIS
            '''
            self.write_sintactic_error(
                p, '<(>', 'Falto parentesis de apertura en llamada a funcion')

        def p_Lfunc_Error2(p):
            '''
            Lfunc : ID LPARENTHESIS Uparams error
                  | ID LPARENTHESIS empty error
            '''
            self.write_sintactic_error(
                p, ')', 'Falto parentesis de cerradura en llamada a funcion')

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

        def p_Uparams_Error1(p):
            '''
            Uparams : Exprlog error Uparams
            '''
            self.write_sintactic_error(
                p, '<,>', 'Falto coma despues de la expresion')

        def p_Params(p):
            '''
            Params : GpoPars 2DOTS TIPO DOTCOMMA Params
                   | GpoPars 2DOTS TIPO
                   |
            '''
            p[0] = self.join_result(p)

        def p_Params_Error1(p):
            '''
            Params : GpoPars error TIPO DOTCOMMA Params
                   | GpoPars error TIPO
            '''
            self.write_sintactic_error(
                p, '<:>', 'Faltaron dos puntos antes de poner tipo de parametro')

        def p_Params_Error2(p):
            '''
            Params : GpoPars 2DOTS TIPO error Params
            '''
            self.write_sintactic_error(
                p, '<;>', 'Falto punto y coma despues de poner tipo de parametro')

        def p_grupoPars(p):
            '''
            GpoPars : ID COMMA GpoPars
                    | ID
            '''
            p[0] = self.join_result(p)

        def p_grupoPars_Error1(p):
            '''
            GpoPars : ID error GpoPars
            '''
            self.write_sintactic_error(
                p, '<,>', 'Falto coma despues de poner el id')

        def p_grupoPar(p):
            '''
            GpoPar : ID
            '''
            p[0] = self.join_result(p)

        def p_constantes(p):
            '''
            constantes : CONSTANTES gpoConstantes
            '''
            self.s_table.stack.append('#')
            self.s_table.add_constants(p.lexer.lineno)
            p[0] = self.join_result(p)

        def p_constantes_empty(p):
            '''
            constantes : empty
            '''
            p[0] = self.join_result(p)

        def p_gpoConstantes(p):
            '''
            gpoConstantes : ID OpAsig Cte DOTCOMMA gpoConstantes
            '''
            self.s_table.stack.append(p[1])
            self.s_table.stack.append(p[3])
            p[0] = self.join_result(p)

        def p_gpoConstantes_recursion(p):
            '''
            gpoConstantes : ID OpAsig Cte DOTCOMMA
            '''
            self.s_table.stack.append(p[1])
            self.s_table.stack.append(p[3])
            p[0] = self.join_result(p)

        def p_gpoConst(p):
            '''
            GpoConst : Cte
                     | Cte COMMA GpoConst
            '''
            p[0] = self.join_result(p)

        def p_gpoConst_Error1(p):
            '''
            GpoConst : Cte error GpoConst
            '''
            self.write_sintactic_error(
                p, '<,>', 'Falto coma despues de la constante')

        def p_Cte_ent(p):
            '''
            Cte : CteEnt
            '''
            p[0] = self.join_result(p) + ',entero'

        def p_Cte_real(p):
            '''
            Cte : CteReal
            '''
            p[0] = self.join_result(p) + ',real'

        def p_Cte_alf(p):
            '''
            Cte : CteAlfa
            '''
            p[0] = self.join_result(p) + ',alfa'

        def p_Cte_log(p):
            '''
            Cte : CteLog
            '''
            p[0] = self.join_result(p) + ',logico'

        def p_variables(p):
            '''
            variables : VARIABLES GpoVars
                      |
            '''
            p[0] = self.join_result(p)

        def p_grupoVars_recursion(p):
            '''
            GpoVars : GpoIds 2DOTS TIPO DOTCOMMA GpoVars
            '''
            self.s_table.stack += p[1].split(',')
            self.s_table.add_variables_type(p[3], p.lexer.lineno)
            p[0] = self.join_result(p)

        def p_grupoVars(p):
            '''
            GpoVars : GpoIds 2DOTS TIPO DOTCOMMA
            '''
            self.s_table.stack += p[1].split(',')
            self.s_table.add_variables_type(p[3], p.lexer.lineno)
            p[0] = self.join_result(p)

        def p_grupoIds(p):
            '''
            GpoIds : GpoId
                   | GpoPar
            '''
            p[0] = self.join_result(p)

        def p_grupoIds_recursion(p):
            '''
            GpoIds : GpoId COMMA GpoIds
                   | GpoPar COMMA GpoIds
            '''
            p[0] = self.join_result(p)

        def p_grupoId(p):
            '''
            GpoId : ID OpAsig CteEnt
                  | ID OpAsig CteReal
                  | ID OpAsig CteAlfa
                  | ID OpAsig CteLog
            '''
            p[0] = self.join_result(p)

        def p_grupoId_dimens(p):
            '''
            GpoId : ID Dimens
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
            else:
                print(p.type, p.value, p.lineno)

        parser = yacc.yacc()
        s = self.input
        parser.parse(s, lexer=lexer)
        self.eje.write_in_document_tags(self.s_table.tags)
        self.eje.write_in_document_instructions(self.s_table.instructions)
        print(self.s_table.table)
