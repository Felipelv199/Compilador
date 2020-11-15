from sintactico import sintactico
from lexico import lexico

file_name = "examen"
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

s = file.read()
lex = lexico(s, lex_file, error_file)
lexer = lex.start_lexico()

sintactic = sintactico(s, error_file)
sintactic.start_sintactic(lexer)

file.close()
lex_file.close()
error_file.close()
