

def comprobar(lista):
    if lista:
        print("Algo no ha salido como se esperaba")
    else:
        print("Funciona segun lo esperado")


def sumar_uno(num):
    num += 1
    return num


def main():
    #global lista
    # comprobar(lista)
    print(sumar_uno(1))


if __name__ == '__main__':
    main()
