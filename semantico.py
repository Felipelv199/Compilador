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
        self.file_error = f_error

    def write_semantic_error(self, n, e, d):
        self.file_error.write('{:<10}|{:<30}|{:<40}|{}\n'.format(
            str(n), e, d, ''))

    def add_constants(self, line_number):
        while True:
            if self.stack[0] == "#":
                self.stack.pop(0)
                break
            name = self.stack.pop(0)
            value = self.stack.pop(0)
            if name not in self.table:
                curr_symbol = Symbol(name, 'Constante')
                try:
                    curr_symbol.valor = int(value)
                except:
                    curr_symbol.valor = value
                self.table[name] = curr_symbol
            else:
                self.write_semantic_error(
                    line_number-1, name, '<semantico> La constante ya habia sido declarada')
                print(line_number-1)

    def add_variables_type(self, type, line_number):
        while True:
            if len(self.stack) == 0:
                break
            name = self.stack.pop(0)
            if name not in self.table:
                curr_symbol = Symbol(name, type)
                self.table[name] = curr_symbol
            else:
                self.write_semantic_error(
                    line_number-1, name, '<semantico> La variable ya habia sido declarada')

    def math_operation(self, element1, operator, element2):
        try:
            element1 = float(element1)
        except:
            element1 = self.get_element_value(element1)
            if element1 == -1:
                print("<semantico> la variable no fue declarada")
        try:
            element2 = float(element2)
        except:
            element2 = self.get_element_value(element2)
            if element2 == -1:
                print("<semantico> la variable no fue declarada")
        operation = 0
        if operator == '+':
            operation = float(element1) + float(element2)
        elif operator == '-':
            operation = float(element1) - float(element2)
        elif operator == '*':
            operation = float(element1) * float(element2)
        elif operator == '/':
            operation = float(element1) / float(element2)
        return str(operation)

    def get_element_value(self, id):
        if id in self.table:
            return self.table[id].valor
        return -1

    def change_variable_value(self, name, value):
        if name in self.table:
            if self.table[name].type == 'Entero':
                self.table[name].valor = int(float(value)/1)
