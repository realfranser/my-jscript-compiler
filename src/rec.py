import json
import argparse



# File Paths
sourceTokenFilePath = 'sources/tokens.json'
tokenFilePath = 'output/tokens.txt'
errorFilePath = 'output/errors.txt'
TSFilePath = 'output/ts.txt'
# Global flag
openComment = False
tsOgNumber = 0
tsAcNumber = 0

def generarTS():
	global tsAcNumber
	lineaNumeroTS = 'Contenido Tabla Símbolos # '+str(tsAcNumber)+' :\n'
	TSFile.write(lineaNumeroTS)
	tsAcNumber = tsAcNumber + 1
	
def lexemaTS(lexema):
	lineaLexemaTS = '* LEXEMA : \''+lexema+'\'\n'
	TSFile.write(lineaLexemaTS)
	atributoTS()
		
def atributoTS():
	lineaAtributoTS = '  ATRIBUTOS :\n'
	TSFile.write(lineaAtributoTS)
	# Esto es solo para la primera entrega habra que cambiarlo cuando hagamos el sintactico
	valor = 'unknown'
	lineaATipoTS = '	+ tipo: ' + valor +'\n'
	TSFile.write(lineaATipoTS)
	valor = 'unknown'
	lineaADesplTS = '	+ despl: ' + valor +'\n'
	TSFile.write(lineaADesplTS)




								
def generarToken(tokenCode,atribute):
	found =False
	with  open(sourceTokenFilePath) as sourceTokenFile:
		data = json.load(sourceTokenFile)
		if tokenCode == 'reservedWord':#buscar en token.json
			for i in data['tokens']:
				if (i['tokenCode'] == 'reservedWord'):
					for k in i['tokenList']:
						if k['atribute']==atribute:
							token = '<' + atribute + ',>\n'
							found = True
							break
			if found == False:
				token = '<ID,' + atribute + '>\n' ## el Analizador Lexico añade los lexemas de tipo ID a la Tabla de Símbolos
				lexemaTS(atribute)

		else:	
			token = '<' + tokenCode + ',' + atribute + '>\n' 
		
		tokenFile.write(token)
		sourceTokenFile.close()

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

def analizadorLinea(line, lineCounter):
	global openComment
	contadorCaracter = 0
	lista = line
	while lista:
		if openComment == True:
			while lista:
				if leerChar(lista)== '*':	
					contadorCaracter = contadorCaracter+1
					lista = lista[1:]
					cerradoEnCaracter=contadorCaracter
					if leerChar(lista) == '/':
						contadorCaracter = contadorCaracter+1
						lista = lista[1:]
						openComment = False
						break
					else:
							contadorCaracter = contadorCaracter+1
							lista = lista[1:]
				else:
					contadorCaracter = contadorCaracter+1
					lista = lista[1:]
			if(openComment == False):
					print('!! Atención: */ comentario en bloque cerrado en caracter: '+
															str(cerradoEnCaracter)+' ,linea: '+str(lineCounter))

		elif leerChar(lista) == '\s' or leerChar(lista) == '\n' or leerChar(lista) == '\t':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			print('** Delimitador en caracater:'+str(contadorCaracter)+' ,linea: '+str(lineCounter))


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
				generarError('++ Error: & esta solo en caracter: '+str(contadorCaracter)+' ,linea: '+str(lineCounter))

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
				generarError('++ Error: \' cadena no se cierra en ningun momento,abierto en caracter: '
																+str(aperturaEnCaracter) +' ,linea: ' + str(lineCounter))

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
				openComment = True
				aperturaEnCaracter=contadorCaracter
				while lista:
					if leerChar(lista)== '*':
						contadorCaracter = contadorCaracter+1
						lista = lista[1:]
						if leerChar(lista) == '/':
							caracateresontadorCaracter = contadorCaracter+1
							lista = lista[1:]
							openComment = False
							break
						else:
							contadorCaracter = contadorCaracter+1
							lista = lista[1:]
					else:
						contadorCaracter = contadorCaracter+1
						lista = lista[1:]
				if(openComment == True):
					print('!! Atención: /* comentario en bloque no se cierra en la linea, abierto en caracter: '+
																str(aperturaEnCaracter)+ ' ,linea: ' + str(lineCounter))

			else:
			  generarError('++ Error: / esta solo en caracter: '+str(contadorCaracter)+' ,linea: '+str(lineCounter))

		else:
			generarError('++ Error: Caracter no reconocido:'+ leerChar(lista) + ' en caracter: '+str(contadorCaracter)+' ,linea: '+str(lineCounter))
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]

	print('//////// Número total de caracateres en la linea:'+str(contadorCaracter))




						

def main():
	global tokenFile,errorFile,openComment,TSFile,tsAcNumber,tsOgNumber
	
	# Parses argument, and requires the user to provide one file
	parser = argparse.ArgumentParser(add_help=True)
	parser.add_argument('-f', type =str,nargs=1,help='Required filename you want to compile')
	args = parser.parse_args()

	
	testFilePath = args.f[0]

    #
    # tokenFilePath, errorFilePath, TSFilePath have to be flushed each time .py is executed, do to this , these are opened in 'w' mode.
    # These paths can be changed at the begining of the file.
    #

	with open(testFilePath,'r') as test, open(tokenFilePath,'w') as tokenFile, open (errorFilePath,'w') as errorFile, open(TSFilePath,'w') as TSFile:
		
		openComment =False
		lineCounter = 0;
		lines = test.readlines()
		tokenLines = lines # backup so the OG list is not modified in case we need it
		generarTS()
		while tokenLines:
			lineCounter= lineCounter+1
			analizadorLinea(leerLinea(tokenLines),lineCounter)
			tokenLines = tokenLines[1:]
	# clean up , close files
	test.close()
	errorFile.close()
	tokenFile.close()
	TSFile.close()


	


if __name__== '__main__':
  	main()