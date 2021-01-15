"""
 Este analizador "master" hace las llamadas correspondientes a los diferentes sub-analizadores (lexico, sintactico y semantico)
 Se encarga de la gestion de errores
 Maneja las tablas de simbolos
"""

file_paths = {
    "token_source": "assets/tokens.json",
    "token_output": "assets/output/tokens.txt",
    "error": "assets/output/errors.txt",
    "ts": "assets/output/ts.txt",
    "parse": "assets/output/parse.txt"
}


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
    with open(test_file_path, 'r') as test,
            open(file_paths["token_output"], 'w') as token_file,
            open(file_paths["error"], 'w') as error_file,
            open(file_paths["ts"], 'w') as ts_file,
            open(file_paths["parse"], 'w') as parse_file:
        pass    
        

if __name__ == '__main__':
    main()

