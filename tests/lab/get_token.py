file_path = './tests/lab/hola.js'

line_count = 0
file_lines = []


class Token:
    def __init__(self, tipo, valor, line):
        self.tipo = tipo
        self.valor = valor
        self.line = line

    def to_string(self):
        return 'Tipe: '+self.tipo+' Atribute: '+self.valor+' Line: '+str(self.line)+'\n'


def pedir_token():
    global line_count, file_lines

    token = get_token() if not (len(file_lines) == 1 and file_lines[0] == '') else Token(
        'final', 'eof', line_count)

    if token.tipo == 'final' and token.valor == 'eol':
        file_lines = file_lines[1:]
        line_count += 1
        token = pedir_token()

    return token


def get_token():
    global line_count, file_lines
    palabra = ''
    linea = file_lines[0]

    while linea:
        if linea == '\n' and palabra == '':
            return Token('final', 'eol', line_count)
        elif linea == '\n':
            return Token('palabra', palabra, line_count)
        elif linea[0] == ' ':
            file_lines[0] = file_lines[0][1:]
            return Token('palabra', palabra, line_count)
        else:
            palabra += linea[0]
            linea = file_lines[0] = file_lines[0][1:]
            if linea == '':
                return Token('palabra', palabra, line_count)

    return None


def main():
    global line_count, file_lines

    line_count = 1

    with open(file_path, 'r') as file:

        file_lines = file.readlines()
    while True:
        token = pedir_token()
        print(token.to_string())
        if token.valor != 'eof':
            print(token.to_string())
            continue
        break


if __name__ == '__main__':
    main()
