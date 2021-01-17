
lista = []


def comprobar(lista):
    if lista:
        print("Algo no ha salido como se esperaba")
    else:
        print("Funciona segun lo esperado")


def main():
    global lista
    comprobar(lista)


if __name__ == '__main__':
    main()
