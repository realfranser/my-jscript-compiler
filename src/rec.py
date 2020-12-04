import json
import argparse



# File Paths
sourceTokenFilePath = 'sources/tokens.json'
tokenFilePath = 'output/tokens.txt'
errorFilePath = 'output/errors.txt'
TSFilePath = 'output/ts.txt'
parseFilePath = 'output/parse.txt'
# Global flag
lastLine=0
openComment = False
tsOgNumber = 0
tsAcNumber = 0

TS = [] #lista tabla de simbolos
TL = [] #lista tokens
parse=[]

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

def writeParse(parse):
	parseFile.write('Descendente')
	for p in parse:
		parseFile.write(' ')
		parseFile.write(str(p))

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
		TS.append(Simbolo(numTabla,lexema,tipo,despl,numParam,tipoParam,modoParam,tipoRetorno,etiqFuncion)) # ACTUALIZAR !!! en caso de que ya exista actualizar el valor
	return len(TS)

def writeTS(tabla):
	nums = getNumTabla(tabla)
	for tsNumber in nums:
		lineaNumeroTS = 'Contenido Tabla Simbolos # '+str(tsNumber)+' :\n'
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
					lineaTS = '	+ numParam: ' + str(simbolo.numParam) +'\n'
					TSFile.write(lineaTS)
				if simbolo.tipoParam and simbolo.modoParam:
						counter = 1
						for j in simbolo.tipoParam :
							#for i in simbolo.modoParam:   ------ revisar in da future
							lineaTS = '	+ TipoParam'+str(counter)+': ' + j +'\n'
							TSFile.write(lineaTS)
							lineaTS = '	+ ModoParam'+str(counter)+': ' + j +'\n'
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
							token = '<reservedWord,' + atribute + '>\n'
							TL.append(atribute)
							found = True
							break
			if found == False:
				pos = addToTS(0,atribute) ################# Editar cuando hagamos semantico
				token = '<ID,' + str(pos) + '>\n' ## el Analizador Lexico añade los lexemas de tipo ID a la Tabla de Símbolos
				TL.append('ID')
				

		else:	
			token = '<' + tokenCode + ',' + atribute + '>\n'
			if(tokenCode == 'chain' or tokenCode == 'wholeConst'):
				TL.append(tokenCode)
			else:
				TL.append(atribute)

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
	global openComment,lastLine
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
			if not lista and openComment and (lastLine == lineCounter+1):
					generarError('++ Error: /* comentario en bloque no se cierra')

		elif leerChar(lista) == '\n' or leerChar(lista) == ' ' or leerChar(lista) == '\t':
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
					if leerChar(lista) == '\r' or leerChar(lista) =='\n':
						generarError('++ Error: \' cadena no se cierra en linea,abierto en caracter: '
																+str(aperturaEnCaracter) +' ,linea: ' + str(lineCounter))
						contadorCaracter = contadorCaracter+1
						lista = lista[1:]
						break
						
					contadorCaracter = contadorCaracter +1
					lista = lista[1:]
					
					if 	not lista:
						generarError('++ Error: \' cadena no se cierra en linea,abierto en caracter: '
																+str(aperturaEnCaracter) +' ,linea: ' + str(lineCounter))

			if len(cadena)<67 and seCierra:
				generarToken('chain',cadena)
			elif seCierra:
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
				if(openComment == True):
					print('!! Atención: /* comentario en bloque no se cierra, abierto en caracter: '+
																str(aperturaEnCaracter)+ ' ,linea: ' + str(lineCounter))

			else:
			  generarError('++ Error: / esta solo en caracter: '+str(contadorCaracter)+' ,linea: '+str(lineCounter))

		else:
			generarError('++ Error: Caracter no reconocido:['+ leerChar(lista) + '] en caracter: '+str(contadorCaracter)+' ,linea: '+str(lineCounter))
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]


sig_token = ''
def A_sint():
	global sig_token , TLcopy
	TLcopy = TL
	sig_token = TLcopy[0]
	P(); # deduzco que es el axioma , en las diapositivas no pone nada
	if sig_token != '$':
		errorParse('A_sint')

def equipara(t):
	global TLcopy,sig_token
	if sig_token == t:
		TLcopy = TLcopy[1:]
		sig_token = TLcopy[0]
	else:
		errorParse('equipara')


def errorParse(error):
	#habra que cambiarlo
	print('Error en regla',error)
	exit()

# Una función para cada no terminal (y una rama para cada regla)

def E():
	if sig_token == 'not' or sig_token == 'openPar' or sig_token == 'chain' or sig_token == 'wholeConst' or sig_token == 'false' or sig_token == 'ID' or sig_token == 'true' :
		parse.append(1) 
		R()
		E1()
	else:
		errorParse('E')

def E1():
	global sig_token
	if sig_token == 'and':
		parse.append(2)
		equipara('and')
		R()
		E1()
	elif sig_token == 'closePar' or sig_token == 'colon' or sig_token == 'semicolon': # FOLLOW de E1  =  { ) , ; }
		parse.append(3)
	else:
		errorParse('E1')

def R():
	if sig_token == 'not' or sig_token == 'openPar' or sig_token =='chain' or sig_token =='wholeConst' or sig_token =='false' or sig_token =='ID' or sig_token =='true':
		parse.append(4)
		U()
		R1()
	else:
		errorParse('R')

def R1():
	global sig_token
	if sig_token == 'equals':
		parse.append(5)
		equipara('equals')
		U()
		R1()
	elif sig_token == 'notEquals':
		parse.append(6)
		equipara('notEquals')
		U()
		R1()
	elif sig_token == 'and' or sig_token == 'closePar' or sig_token == 'colon' or sig_token == 'semicolon':
		parse.append(7)
	else:
		errorParse('R1')


def U():
	if sig_token == 'not' or sig_token == 'openPar' or sig_token =='chain' or sig_token =='wholeConst' or sig_token =='false' or sig_token =='ID' or sig_token =='true':
		parse.append(8)
		V()
		U1()
	else:
		errorParse('U')

def U1():
	global sig_token
	if sig_token == 'plus':
		parse.append(9)
		equipara('plus')
		V()
		U1()
	elif sig_token == 'minus':
		parse.append(10)
		equipara('minus')
		V()
		U1()
	elif sig_token == 'notEquals' or sig_token == 'and' or sig_token == 'closePar' or sig_token == 'colon' or sig_token == 'semicolon' or sig_token == 'equals':
		parse.append(11)
	else:
		errorParse('R2')

def V():
	 if sig_token == 'ID':
	 	parse.append(12)
	 	equipara('ID')
	 	V1()
	 elif sig_token == 'openPar':
	 	parse.append(13)
	 	equipara('openPar')
	 	E()
	 	equipara('closePar')
	 elif sig_token == 'wholeConst':
	 	parse.append(14)
	 	equipara('wholeConst')
	 elif sig_token == 'chain':
	 	parse.append(15)
	 	equipara('chain')
	 elif sig_token == 'true':
	 	parse.append(16)
	 	equipara('true')
	 elif sig_token == 'false':
	 	parse.append(17)
	 	equipara('false')
	 elif sig_token == 'not':
	 	parse.append(18)
	 	equipara('not')
	 	equipara('ID')


def V1():
	if sig_token == 'openPar':
	 	parse.append(19)
	 	equipara('openPar')
	 	L()
	 	equipara('closePar')
	elif sig_token == 'autoInc':
	 	parse.append(20)
	 	equipara('autoInc')
	elif sig_token == 'notEquals' or sig_token == 'and' or sig_token == 'closePar' or sig_token == 'plus' or sig_token == 'colon' or sig_token == 'minus' or sig_token == 'semicolon' or sig_token == 'equals':
		parse.append(21)
	else:
		errorParse('V1')



def S():
	if sig_token == 'ID':
		parse.append(22)
		equipara('ID')
		S1()

	elif sig_token == 'alert':
		parse.append(23)
		equipara('alert')
		equipara('openPar')
		E()
		equipara('closePar')
		equipara('semicolon') 
	elif sig_token == 'input':
		parse.append(24)
		equipara('input')
		equipara('openPar')
		equipara('ID')
		equipara('closePar')
		equipara('semicolon')
	elif sig_token == 'return':
		parse.append(25)
		equipara('return')
		X()
		equipara('semicolon')
def S1(): 
	if sig_token == 'equal':
		parse.append(26)
		equipara('equal')
		E()
		equipara('semicolon')
	elif sig_token == 'openPar':
		parse.append(27)
		equipara('openPar')
		L()
		equipara('closePar')
		equipara('semicolon')
	else:              # parece que no hay follow de s1 comprobar
		errorParse('S1')


def L():
	if sig_token == 'not' or sig_token == 'openPar' or sig_token =='chain' or sig_token =='wholeConst' or sig_token =='false' or sig_token =='ID' or sig_token =='true':
		parse.append(28)
		E()
		Q()
	elif sig_token == 'closePar':
		parse.append(29)
	else:
		errorParse('L')

def Q():
	if sig_token == 'colon':
		parse.append(30)
		equipara('colon')
		E()
		Q()
	elif sig_token == 'closePar':
		parse.append(31)
	else :
		errorParse('Q')

def X():
	if sig_token == 'not' or sig_token == 'openPar' or sig_token =='chain' or sig_token =='wholeConst' or sig_token =='false' or sig_token =='ID' or sig_token =='true':
		parse.append(32)
		E()
	elif sig_token == 'semicolon':
		parse.append(33)
	else:
		errorParse('X')

def B():
	if sig_token == 'if':
		parse.append(34)
		equipara('if')
		equipara('openPar')
		E()
		equipara('closePar')
		S()
	elif sig_token == 'let':
		parse.append(35)
		equipara('let')
		T()
		equipara('ID')
		equipara('semicolon')
	elif sig_token == 'alert' or sig_token == 'ID' or sig_token == 'input' or sig_token == 'return':
		parse.append(36)
		S()
	elif sig_token == 'do':
	 	parse.append(37)
	 	equipara('do')
	 	equipara('openBraq')
	 	C()
	 	equipara('closeBraq')
	 	equipara('while')
	 	equipara('openPar')
	 	E()
	 	equipara('closePar')
	 	equipara('semicolon')
	else:
		errorParse('B')

def T(): 
	if sig_token == 'number':
		parse.append(38)
		equipara('number')
	elif sig_token == 'boolean':
		parse.append(39)
		equipara('boolean')
	elif sig_token == 'string':
		parse.append(40)
		equipara('string')
	else:
		errorParse('T')

def F():
	if sig_token == 'function':
		parse.append(41)
		equipara('function')
		H()
		equipara('ID')
		equipara('openPar')
		A()
		equipara('closePar')
		equipara('openBraq')
		C()
		equipara('closeBraq')
	else:
		errorParse('F')


def H():
	if sig_token == 'boolean' or sig_token == 'number' or sig_token == 'string':
		parse.append(42)
		T()
	elif sig_token == 'ID':
		parse.append(43)
	else:
		errorParse('H')
		
def A():
	if sig_token == 'boolean' or sig_token == 'number' or sig_token == 'string':
		parse.append(44)
		T()
		equipara('ID')
		K()
	elif sig_token == 'closePar':
		parse.append(45)
	else:
		errorParse('A')
		
def K():
 	if sig_token == 'colon':
 		parse.append(46)
 		equipara('colon')
 		T()
 		equipara('ID')
 		K()
 	elif sig_token == 'closePar':
 		parse.append(47)
 	else:
 		errorParse('K')

def C():
	if sig_token == 'alert' or  sig_token == 'do' or  sig_token == 'ID' or sig_token == 'if' or  sig_token =='input' or  sig_token =='let' or  sig_token =='return':
		parse.append(48)
		B()
		C()
	elif sig_token == 'closeBraq':
		parse.append(49)
	else:
		errorParse('C')

def P():
	if sig_token == 'alert' or  sig_token == 'do' or  sig_token == 'ID' or  sig_token == 'if' or  sig_token =='input' or  sig_token =='let' or  sig_token =='return':
		parse.append(50)
		B()
		P()
	elif sig_token == 'function':
		parse.append(51)
		F()
		P()
	elif sig_token == '$':
		pass
		#hemos terminado
		# habra que añadir a TL un dolar al final para saber que hemos acabado el archivo
	else:
		errorParse('P')
		






						

def main():
	global tokenFile,errorFile,openComment,TSFile,tsAcNumber,tsOgNumber,TS,lastLine,parse, parseFile
	
	# Parses argument, and requires the user to provide one file
	parser = argparse.ArgumentParser(add_help=True)
	parser.add_argument('-f', type =str,nargs=1,help='Required filename you want to compile')
	args = parser.parse_args()

	
	testFilePath = args.f[0]

    #
    # tokenFilePath, errorFilePath, TSFilePath have to be flushed each time .py is executed, do to this , these are opened in 'w' mode.
    # These paths can be changed at the begining of the file.
    #

	with open(testFilePath,'r') as test, open(tokenFilePath,'w') as tokenFile, open (errorFilePath,'w') as errorFile, open(TSFilePath,'w') as TSFile , open(parseFilePath,'w') as parseFile:
		
		openComment =False
		lineCounter = 0
		lines = test.readlines()
		tokenLines = lines # backup so the OG list is not modified in case we need it
		lastLine = len(tokenLines)
		#generarTS()
		while tokenLines:
			lineCounter= lineCounter+1
			analizadorLinea(leerLinea(tokenLines),lineCounter)
			tokenLines = tokenLines[1:]
	# clean up , close files
		writeTS(TS)
		TL.append('$')
		print(*TL)
		A_sint()
		writeParse(parse)
	test.close()
	errorFile.close()
	tokenFile.close()
	TSFile.close()


	


if __name__== '__main__':
  	main()