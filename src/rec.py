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

TS = []

class Simbolo:
	def __init__ (self,numTabla,lexema,tipo= None,despl=0,numParam=0,tipoParam=[],modoParam=[],tipoRetorno = None,etiqFuncion = None,param = None):
		# tipo Simbolo , Tabla de Simbolos matriz de 'Simbolo',
		self.numTabla = numTabla # Tabla a la que pertenece el simbolo
		self.lexema = lexema # lexema de linea 
		self.tipo = tipo 	 # tipo de identificador ej: int, boolean ,'cadena'
		self.despl = despl   # direccion relativa
		self.numParam = numParam # parametros subprograma
		self.tipoParam = tipoParam # lista tipos parametros subprograma
		self.modoParam = tipoRetorno # lista modo de paso parametro subprograma
		self.tipoRetorno = tipoRetorno  # tipo devuelto por funcion
		self.etiqFuncion = etiqFuncion # Etiqueta tipo funcion
		self.param = param # Parametro no pasado por valor


def getSimbolosTabla(tabla,numTabla):
	sol= []
	for i in tabla:
		if i.numTabla == numTabla:
			sol.append(i)
	return sol

def getNumTabla(tabla):
	sol= []
	for i in tabla:
		if not(i.numTabla in sol):
			sol.append(i.numTabla)
	return sol

def getLexema(tabla,lexema):
	for i in tabla:
		if i.lexema == lexema:
			return True
	return False

def addToTS(numTabla,lexema,tipo= None,despl=0,numParam=0,tipoParam=[],modoParam=[],tipoRetorno = None,etiqFuncion = None,param = None):
	if getLexema(TS,lexema) == False:
		TS.append(Simbolo(numTabla,lexema,tipo,despl,numParam,tipoParam,modoParam,tipoRetorno,etiqFuncion))

def writeTS(tabla):
	nums = getNumTabla(tabla)
	for tsNumber in nums:
		lineaNumeroTS = 'Contenido Tabla Símbolos # '+str(tsNumber)+' :\n'
		TSFile.write(lineaNumeroTS)
		for simbolo in tabla:
			if(simbolo.numTabla == tsNumber):
				lineaLexemaTS = '* LEXEMA : \''+simbolo.lexema+'\'\n'
				TSFile.write(lineaLexemaTS)
				lineaAtributoTS = '  ATRIBUTOS :\n'
				TSFile.write(lineaAtributoTS)
				if simbolo.tipo != None:
					lineaTS = '	+ tipo: ' + simbolo.tipo +'\n'
					TSFile.write(lineaTS)

				if simbolo.despl != 0:
					lineaTS = '	+ Despl: ' + str(simbolo.despl) +'\n'
					TSFile.write(lineaTS)

				if simbolo.numParam != 0:
					lineaTS = '	+ numParam: ' + str(imbolo.numParam) +'\n'
					TSFile.write(lineaTS)

				if simbolo.tipoParam and simbolo.modoParam:
						counter = 1
						for j in simbolo.tipoParam , i in simbolo.modoParam:
							lineaTS = '	+ TipoParam'+str(counter)+': ' + j +'\n'
							TSFile.write(lineaTS)
							lineaTS = '	+ ModoParam'+str(counter)+': ' + i +'\n'
							TSFile.write(lineaTS)

				if simbolo.tipoRetorno != None:
					lineaTS = '	+ TipoRetorno: ' + simbolo.tipoRetorno +'\n'
					TSFile.write(lineaTS)

				if simbolo.etiqFuncion != None:
					lineaTS = '	+ tipo: ' + simbolo.etiqFuncion +'\n'
					TSFile.write(lineaTS)

				if simbolo.param != None:
					lineaTS = '	+ tipo: ' + simbolo.param +'\n'
					TSFile.write(lineaTS)
	
								
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
				addToTS(0,atribute,'unknown',-1) ################# Editar cuando hagamos semantico

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

		elif leerChar(lista) == '\s' or leerChar(lista) == '\n' or leerChar(lista) == ' ' or leerChar(lista) == '\t':
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
				if len(cadena)<67:
					generarToken('chain',cadena)
				else:
			  		generarError('++ Error: \' cadena supera los 64 caracteres por: '
																+str(len(cadena)-66) +' ,en la linea: ' + str(lineCounter))

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
			generarError('++ Error: Caracter no reconocido:['+ leerChar(lista) + '] en caracter: '+str(contadorCaracter)+' ,linea: '+str(lineCounter))
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]

	print('//////// Número total de caracateres en la linea:'+str(contadorCaracter))




						

def main():
	global tokenFile,errorFile,openComment,TSFile,tsAcNumber,tsOgNumber,TS
	
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
		#generarTS()
		while tokenLines:
			lineCounter= lineCounter+1
			analizadorLinea(leerLinea(tokenLines),lineCounter)
			tokenLines = tokenLines[1:]
	# clean up , close files
		writeTS(TS)
	test.close()
	errorFile.close()
	tokenFile.close()
	TSFile.close()


	


if __name__== '__main__':
  	main()