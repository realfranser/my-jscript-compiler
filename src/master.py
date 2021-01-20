"""
 Este analizador "master" hace las llamadas correspondientes a los diferentes sub-analizadores (lexico, sintactico y semantico)
 Se encarga de la gestion de errores
 Maneja las tablas de simbolos
"""
import json
import argparse
from Sintactico import sintactico


# ATRIBUTES
file_paths = {
    "token_source": "src/assets/tokens.json",
    "token_output": "tests/output/tokens.txt",
    "error": "tests/output/errors.txt",
    "ts": "tests/output/ts.txt",
    "parse": "tests/output/parse.txt"
}


# imported by other files
line_count = 1
open_comment = False
last_line = False
parse = []


# CLASSES


class Token:
    def __init__(self, key, value, linea):
        self.key = key
        self.value = value
        self.linea = linea

    def to_string(self):
        return '<'+self.key+','+self.value+'>'


class Simbolo:
    """
    Elemento que conforma las tablas de simbolos
    """

    def __init__(self, lexema, tipo=None, despl=None, num_param=None, tipo_param=[], tipo_dev=None, etiqueta=None):
        self.lexema = lexema  # lexema de linea
        self.tipo = tipo 	 # tipo de identificador ej: int, boolean ,'cadena'
        self.despl = despl   # direccion relativa
        self.num_param = num_param  # parametros subprograma
        self.tipo_param = tipo_param  # lista tipos parametros subprograma
        self.tipo_dev = tipo_dev  # tipo devuelto por funcion
        self.etiqueta = etiqueta  # Etiqueta tipo funcion


class Tabla_Simbolos:
    """
    Elemento tabla de simbolos:
    Inputs:
        - nombre: nombre de la tabla de simbolos
    Functions:
    """

    def __init__(self, nombre, retorno):
        self.nombre = nombre
        self.desplazamiento = 0
        self.entradas = []
        self.retorno = retorno
        self.sizes = {
            "numero": 2,
            "boolean": 1,
            "string": 64  # Revisar size de las cadenas
        }

    def insertar(self, simbolo):
        """
        Inserta un nuevo simbolo en la tabla
        Si el simbolo es de un tipo perteneciente al diccionario sizes
        se le suma desplazamiento a la tabla modificando asi el atributo del simbolo
        """
        if simbolo.tipo in self.sizes:
            simbolo.despl = self.desplazamiento
            self.desplazamiento += self.sizes[simbolo.tipo]
        self.entradas.append(simbolo)

    def to_string(self):
        """
        Hacer el to string para que cada Tabla de Simbolos se printee como es debido
        """
        string = 'Contenido Tabla de Simbolos #'+self.nombre+' :\n'

        for simbolo in self.entradas:
            string += '* LEXEMA : \''+simbolo.lexema+'\'\n  ATRIBUTOS :\n'
            string += '	+ Tipo: ' + \
                str(simbolo.tipo) + '\n' if simbolo.tipo != None else ''
            string += '	+ Despl: ' + \
                str(simbolo.despl) + '\n' if simbolo.despl != None else ''
            string += '	+ Num_Param: ' + \
                str(simbolo.num_param) + \
                '\n' if simbolo.num_param != None else ''
            if simbolo.tipo == 'function':
                for i in range(len(simbolo.tipo_param)):
                    string += '	+ Tipo_Param ' + \
                        str(i)+': ' + str(simbolo.tipo_param[i]) + '\n'

            string += '	+ Tipo_Retorno: ' + simbolo.tipo_dev + \
                '\n' if simbolo.tipo_dev != None else ''
            string += '	+ Tipo: ' + simbolo.etiqueta + \
                '\n' if simbolo.etiqueta != None else ''

        return string

    def find(self, simbolo):
        return ([entry for entry in self.entradas if entry.lexema == simbolo.lexema][:1] or [None])[0]

# FUNCTIONS


def main():
    # declaracion de variables globales
    global token_file, open_comment, line_count, token_list
    # Parses argument, and requires the user to provide one file
   # parser = argparse.ArgumentParser(add_help=True)
    # parser.add_argument('-f', type=str, nargs=1,
    # help='Required filename you want to compile')
    # args = parser.parse_args()

    # test_file_path = args.f[0]
    test_file_path = './tests/test2.js'
    """
    The following files have to be flushed each time .py executes, to do this, they are opened in 'w' mode
    These paths are stored in the dictionary file_paths and can be changed as wished
    """
    with open(file_paths["token_output"], 'w') as token_file, open(file_paths["ts"], 'w') as ts_file, open(file_paths["parse"], 'w') as parse_file, open(file_paths["error"], 'w') as error_file:

        open_comment = False
        line_count = 1

        parse, token_list, tablas_simbolos = sintactico.analizador(
            test_file_path)

        # Escribir en el fichero tabla de simbolos, todas las tablas de simbolos
        for tabla in tablas_simbolos:
            ts_file.write(tabla.to_string()+"\n\n")

        # Escribir en el fichero parse, todos los parses
        parse_string = 'Descendente'
        for p in parse:
            parse_string += ' '+str(p)
        parse_file.write(parse_string)

        # Escribir en el fichero token_file todos los tokens
        token_string = ''
        for token in token_list[:-1]:
            token_string += (token.to_string() + '\n')
        token_file.write(token_string)

        # Escribir en el fichero de errores
        error_file.write("Compilado sin errores")


if __name__ == '__main__':
    main()
