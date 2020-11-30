from enum import Flag
import re


class Symbol:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.valor = ''

    def __repr__(self):
        return "{} tipo={} value={}".format(self.name, self.type, str(self.valor))


class Symbol_Table:
    def __init__(self, f_error):
        self.table = {}
        self.stack = []
        self.instructions = []
        self.tags = []
        self.file_error = f_error
        self.i_number = 0
        self.e_number = 0

    def write_semantic_error(self, n, e, d):
        self.file_error.write('{:<10}|{:<30}|{:<40}|{}\n'.format(
            str(n), e, d, ''))

    def add_constants(self, line_number):
        while True:
            if self.stack[0] == "#":
                self.stack.pop(0)
                break
            name = self.stack.pop(0)
            vt = self.stack.pop(0).split(',')
            value = vt[0]
            type = vt[1]
            if name not in self.table:
                curr_symbol = Symbol(name, 'Constante')
                try:
                    curr_symbol.valor = int(value)
                except:
                    curr_symbol.valor = value
                curr_symbol.type = type
                curr_symbol.valor = value
                self.table[name] = curr_symbol
                self.add_global_variable_tag(name, 'C', type, 0, 0)
                self.add_instruction('LIT', '{},0'.format(value))
                self.add_instruction('STO', '0,{}'.format(name))
            else:
                self.write_semantic_error(
                    line_number-1, name, '<semantico> La constante ya habia sido declarada')

    def add_variables_type(self, type, line_number):
        while True:
            if len(self.stack) == 0:
                break
            s = self.stack.pop(0).split(':=')
            name = s[0]

            if name in self.table:
                self.write_semantic_error(
                    line_number-1, name, '<semantico> La variable ya habia sido declarada')
                return

            value = ''
            try:
                value = s[1]
            except:
                value = ''
            if len(s) > 1:
                t = self.get_cte_type(s[1])
                if t != type.lower():
                    self.write_semantic_error(
                        line_number-1, name, '<semantico> La variable es de tipo <{}>'.format(t))
                    return
                self.add_instruction('LIT', '{},0'.format(value))
                self.add_instruction('STO', '0,{}'.format(name))
            curr_symbol = Symbol(name, type)
            self.table[name] = curr_symbol
            self.add_global_variable_tag(name, 'V', type, 0, 0)

    def add_instruction(self, operator, code):
        self.i_number += 1
        self.instructions.append('{} {} {}'.format(
            str(self.i_number), operator, code))

    def add_global_variable_tag(self, name, var_const, type, dim1, dim2):
        new_type = ''
        if type.lower() == 'entero':
            new_type = 'E'
        elif type.lower() == 'real':
            new_type = 'R'
        elif type.lower() == 'logico':
            new_type = 'L'
        elif type.lower() == 'alfabetico':
            new_type = 'A'

        self.tags.append('{},{},{},{},{},#,'.format(
            name, var_const, new_type, dim1, dim2))

    def add_tag(self, name, number):
        self.tags.append('{},{},{},{},{},#,'.format(
            name, 'I', 'I', number, '0'))

    def add_e_tag(self, line_n):
        self.tags.append('{},{},{},{},{},#,'.format(
            '_E{}'.format(self.e_number), 'I', 'I', line_n, '0'))

    def add_oprel_instruction(self, val):
        self.i_number += 1
        code = 0
        if val == '<':
            code = 9
        elif val == '>':
            code = 10
        elif val == '<=':
            code = 11
        elif val == '>=':
            code = 12
        elif val == '<>':
            code = 13
        elif val == '=':
            code = 14
        self.instructions.append('{} {} {}'.format(
            str(self.i_number), 'OPR', '0,{}'.format(code)))

    def add_math_instructions(self, val):
        self.i_number += 1
        code = 0
        if val == '+':
            code = 2
        elif val == '-':
            code = 3
        elif val == '*':
            code = 4
        elif val == '/':
            code = 5
        self.instructions.append('{} {} {}'.format(
            str(self.i_number), 'OPR', '0,{}'.format(code)))

    def get_cte_type(self, value):
        curr = None
        try:
            float(value)
            if value.__contains__('.'):
                curr = 'Real'
            else:
                curr = 'Entero'
        except:
            curr = value

        curr_type = ''
        if curr == 'Entero':
            curr_type = 'entero'
        elif curr == 'Real':
            curr_type = 'real'
        elif curr == "verdadero" or curr == "falso":
            curr_type = 'logico'
        else:
            curr_type = 'alfabetico'
        return curr_type
