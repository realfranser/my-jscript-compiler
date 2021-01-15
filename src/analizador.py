"""
 Este analizador "master" hace las llamadas correspondientes a los diferentes sub-analizadores (lexico, sintactico y semantico)
 Se encarga de la gestion de errores
 Maneja las tablas de simbolos
"""
import json
import argparse

file_paths = {
    "token_source": "assets/tokens.json",
    "token_output": "assets/output/tokens.txt",
    "error": "assets/output/errors.txt",
    "ts": "assets/output/ts.txt",
    "parse": "assets/output/parse.txt"
}


class Simbolo:
    """
    Elemento que conforma las tablas de simbolos
    """

    def __init__(self, lexema, tipo=None, despl=0, num_param=0, tipo_param=[], modo_paso=[], tipo_dev=None, etiqueta=None):
        self.lexema = lexema  # lexema de linea
        self.tipo = tipo 	 # tipo de identificador ej: int, boolean ,'cadena'
        self.despl = despl   # direccion relativa
        self.num_param = num_param  # parametros subprograma
        self.tipo_param = tipo_param  # lista tipos parametros subprograma
        self.modo_paso = modo_paso  # lista modo de paso parametro subprograma
        self.tipo_dev = tipo_dev  # tipo devuelto por funcion
        self.etiqueta = etiqueta  # Etiqueta tipo funcion


def main():

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
        pass


if __name__ == '__main__':
    main()
