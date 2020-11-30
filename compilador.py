from ejecutable import Ejecutable
from sintactico import sintactico
from lexico import lexico
from semantico import Symbol_Table
from sys import argv
from ejecutable import Ejecutable

try:
    file_name = argv[1]
except:
    print('No file name was provided')
    exit()

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

eje_file = open("{}.eje".format(file_name), "w")

s = file.read()
lex = lexico(s, lex_file, error_file)

symbol_table = Symbol_Table(error_file)
ejecutable = Ejecutable(eje_file)
sintactic = sintactico(s, error_file, symbol_table, ejecutable)
sintactic.start_sintactic(lex)

file.close()
lex_file.close()
error_file.close()
eje_file.close()
