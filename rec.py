import json
import argparse
targetFile = 'tokens.json'

openComment = False
								
def generarToken(tokenCode,atribute):
	with  open(targetFile) as f:
		data = json.load(f)
		if tokenCode == 'reservedWord':#buscar en token.json
			for i in data['tokens']:
				if (i['tokenCode'] == 'reservedWord'):
					for k in i['tokenList']:
						if k['atribute']==atribute:
							token = '<' + atribute + ',>\n'
							break
						else:
							token = '<ID,' + atribute + '>\n'
		else:	
			token = '<' + tokenCode + ',' + atribute + '>\n' 
		
		tokenFile.write(token)

def generarError(error):
		errorFile.write(error)
		errorFile.write('\n')
		
		
def leerChar(lista):
	char = None
	if lista:
		char = lista[0]
	return char

def leerLinea(lista):
	linea = None
	if lista:
		linea = lista[0]
	return linea

def analizadorLinea(line):
	global comentarioAbierto
	contadorCaracter = 0
	lista = line
	while lista:
		if comentarioAbierto == True:
			while lista:
				if leerChar(lista)== '*':	
					contadorCaracter = contadorCaracter+1
					lista = lista[1:]
					aperturaEnCaracter=contadorCaracter
					if leerChar(lista) == '/':
						contadorCaracter = contadorCaracter+1
						lista = lista[1:]
						comentarioAbierto = False
						break
					else:
							contadorCaracter = contadorCaracter+1
							lista = lista[1:]
				else:
					contadorCaracter = contadorCaracter+1
					lista = lista[1:]
			if(comentarioAbierto == False):
					print('!! Atención: /* comentario en bloque cerrado en caracter: '+str(aperturaEnCaracter))

		elif leerChar(lista) == ' ' or leerChar(lista) == '\n':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			print('** Delimitador en caracater:'+str(contadorCaracter))


		elif leerChar(lista) == '+':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			if leerChar(lista) == '+':
				contadorCaracter = contadorCaracter+1
				lista = lista[1:]
				generarToken('autoIncOp','autoinc')
			else:
				generarToken('aritOp','plus')

		elif leerChar(lista) == '-':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			if leerChar(lista) == '-':
				contadorCaracter = contadorCaracter+1
				lista = lista[1:]
				generarToken('autoDecOp','autodec')
			else:
				generarToken('aritOp','minus')

		elif leerChar(lista) == '=':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			if leerChar(lista) == '=':
				contadorCaracter = contadorCaracter+1
				lista = lista[1:]
				generarToken('relOp','equals')
			else:
				generarToken('asigOp','equal')

		elif leerChar(lista) == '!':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			if leerChar(lista) == '=':
				contadorCaracter = contadorCaracter+1
				lista = lista[1:]
				generarToken('relOp','notEquals')
			else:
				generarToken('logOp','not')

		elif leerChar(lista)=='&':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			if leerChar(lista) == '&':
				contadorCaracter = contadorCaracter+1
				lista = lista[1:]
				generarToken('logOp','and')
			else:
				generarError('++ Error: & is alone')

		elif leerChar(lista) == ',':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			generarToken('separator','colon')

		elif leerChar(lista) == ';':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			generarToken('separator','semicolon')

		elif leerChar(lista) == '{':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			generarToken('separator','openBraq')

		elif leerChar(lista) == '}':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			generarToken('separator','closeBraq')

		elif leerChar(lista) == '(':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			generarToken('separator','openPar')

		elif leerChar(lista) == ')':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			generarToken('separator','closePar')

		elif leerChar(lista)== '\'':
			cadena = leerChar(lista)
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			seCierra = False
			aperturaEnCaracter=contadorCaracter
			while lista:
				cadena = cadena + leerChar(lista)
				if leerChar(lista)== '\'':
					seCierra =True
					contadorCaracter = contadorCaracter+1
					lista = lista[1:]
					break
				else:
					contadorCaracter = contadorCaracter+1
					lista = lista[1:]
			if(seCierra == False):
				generarError('++ Error: \' cadena no se cierra en ningun momento,abierto en caracter: '+str(aperturaEnCaracter))

			else:
			  generarToken('chain',cadena)

		elif leerChar(lista).isdigit()== True:
			numero = leerChar(lista)
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			while lista:		
				if leerChar(lista).isdigit() == True:
					numero = numero + leerChar(lista)
					contadorCaracter = contadorCaracter+1
					lista = lista[1:]
				else:
					break

			generarToken('wholeConst',numero)	

		elif leerChar(lista).isalpha()== True:
			alphanum = leerChar(lista)
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			while lista:		
				if leerChar(lista).isalpha()== True or leerChar(lista).isdigit() == True or leerChar(lista) == '_':
					alphanum = alphanum + leerChar(lista)
					contadorCaracter = contadorCaracter+1
					lista = lista[1:]
				else:
					break

			generarToken('reservedWord',alphanum)


		elif leerChar(lista)== '/':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			if leerChar(lista) == '*':
				contadorCaracter = contadorCaracter+1
				lista = lista[1:]
				comentarioAbierto = True
				aperturaEnCaracter=contadorCaracter
				while lista:
					if leerChar(lista)== '*':
						contadorCaracter = contadorCaracter+1
						lista = lista[1:]
						if leerChar(lista) == '/':
							caracateresontadorCaracter = contadorCaracter+1
							lista = lista[1:]
							comentarioAbierto = False
							break
						else:
							contadorCaracter = contadorCaracter+1
							lista = lista[1:]
					else:
						contadorCaracter = contadorCaracter+1
						lista = lista[1:]
				if(comentarioAbierto == True):
					print('!! Atención: /* comentario en bloque no se cierra en la linea, abierto en caracter: '+str(aperturaEnCaracter))

			else:
			  generarError('++ Error: / is alone')

		else:
			generarError('++ Error: Caracter no reconocido:'+ leerChar(lista))
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]

	print('//////// Número total de caracateres en la linea:'+str(contadorCaracter))




						

def main():
	global tokenFile,errorFile,comentarioAbierto
	parser = argparse.ArgumentParser(add_help=True)
	parser.add_argument('-f', type =str,nargs=1,help='Required filename you want to compile')
	args = parser.parse_args()
	tokenFile = open('tokens.txt','w')
	with open(args.f[0],'r') as f, open ('error.txt','w') as errorFile:
		comentarioAbierto =False
		lines = f.readlines()
		lineas = lines # por si acaso
		while lineas:
			print('-------------------------------------------')
			print('comentarioAbierto='+str(comentarioAbierto))
			analizadorLinea(leerLinea(lineas))
			lineas = lineas[1:]

	f.close()
	errorFile.close()
	tokenFile.close()

	


if __name__== '__main__':
  	main()