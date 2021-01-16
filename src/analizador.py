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
    "token_source": "assets/tokens.json",
    "token_output": "assets/output/tokens.txt",
    "error": "assets/output/errors.txt",
    "ts": "assets/output/ts.txt",
    "parse": "assets/output/parse.txt"
}

token_list = []
tablas_simbolos = {}
parse = []

# CLASSES


class Token:
    def __init__(self, token, linea):
        self.token = token
        self.linea = linea


class Simbolo:
    """
    Elemento que conforma las tablas de simbolos
    """

    def __init__(self, lexema, tipo=None, despl=None, num_param=None, tipo_param=[], modo_paso=[], tipo_dev=None, etiqueta=None):
        self.lexema = lexema  # lexema de linea
        self.tipo = tipo 	 # tipo de identificador ej: int, boolean ,'cadena'
        self.despl = despl   # direccion relativa
        self.num_param = num_param  # parametros subprograma
        self.tipo_param = tipo_param  # lista tipos parametros subprograma
        self.modo_paso = modo_paso  # lista modo de paso parametro subprograma
        self.tipo_dev = tipo_dev  # tipo devuelto por funcion
        self.etiqueta = etiqueta  # Etiqueta tipo funcion


class Tabla_Simbolos:
    """
    Elemento tabla de simbolos:
    Inputs:
        - nombre: nombre de la tabla de simbolos
    Functions:
    """

    def __init__(self, nombre):
        self.nombre = nombre
        self.desplazamiento = 0
        self.entradas = []
        self.sizes = {
            "entero": 2,
            "logico": 1,
            "cadena": 64  # Revisar size de las cadenas
        }

    def insertar_simbolo(self, simbolo):
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
            string += '	+ Tipo: ' + simbolo.tipo + '\n' if simbolo.tipo != None else ''
            string += '	+ Despl: ' + \
                str(simbolo.despl) + '\n' if simbolo.despl != None else ''
            string += '	+ Num_Param: ' + \
                str(simbolo.num_param) + \
                '\n' if simbolo.num_param != None else ''

            for i in range(len(simbolo.tipo_parm)):
                string = '	+ Tipo_Param' + \
                    str(i)+': ' + simbolo.tipo_param[i] + '\n'
                string = '	+ Modo_Paso' + \
                    str(i)+': ' + simbolo.modo_paso[i] + '\n'

            string += '	+ Tipo_Retorno: ' + simbolo.tipoRetorno + \
                '\n' if simbolo.tipo_retorno != None else ''
            string += '	+ Tipo: ' + simbolo.etiqFuncion + \
                '\n' if simbolo.etiqueta != None else ''
            string += '	+ Tipo: ' + simbolo.param + '\n' if simbolo.param != None else ''

        return string

# FUNCTIONS


def main():
    # declaracion de variables globales
    global token_file, open_comment
    # Parses argument, and requires the user to provide one file
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-f', type=str, nargs=1,
                        help='Required filename you want to compile')
    args = parser.parse_args()

    test_file_path = args.f[0]

    """
    The following files have to be flushed each time .py executes, to do this, they are opened in 'w' mode
    These paths are stored in the dictionary file_paths and can be changed as wished
    """
    with open(test_file_path, 'r') as test, open(file_paths["token_output"], 'w') as token_file, open(file_paths["error"], 'w') as error_file, open(file_paths["ts"], 'w') as ts_file, open(file_paths["parse"], 'w') as parse_file:

        open_comment = False
        line_count = 1
        # Introduce linea a linea en el analizador sintactico
        file_lines = test.readLines()
        while file_lines:
            # es posible que no sea necesaria la comprobacion file_lines
            sintactico.analizar(
                file_lines[0] if file_lines else None, line_count)
            line_count += 1
            file_lines[1:]
        # Escribir en el fichero tabla de simbolos, todas las tablas de simbolos
        for tabla in tablas_simbolos:
            ts_file.write(tabla.to_string+"\n\n")
        # Se anyade para ver si ha terminado el archivo
        token_list.append(Token('$', line_count-1))
        # Escribir en el fichero parse, todos los parses
        parse_string = 'Descendente'
        for p in parse:
            parse_string += ' '+str(p)
        parse_file.write(parse_string)


if __name__ == '__main__':
    main()
