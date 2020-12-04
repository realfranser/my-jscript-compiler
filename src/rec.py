import json
import argparse



# File Paths
sourceTokenFilePath = 'sources/tokens.json'
tokenFilePath = 'output/tokens.txt'
errorFilePath = 'output/errors.txt'
TSFilePath = 'output/ts.txt'
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
class Token:
	def __init__(self,tokenCode,atribute):
		self.tokenCode = tokenCode
		self.atribute = atribute

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
							TL.append(Token('reservedWord',atribute))
							found = True
							break
			if found == False:
				pos = addToTS(0,atribute,'unknown',-1) ################# Editar cuando hagamos semantico
				token = '<ID,' + str(pos) + '>\n' ## el Analizador Lexico añade los lexemas de tipo ID a la Tabla de Símbolos
				TL.append(Token('ID',atribute))
				

		else:	
			token = '<' + tokenCode + ',' + atribute + '>\n' 
			TL.append(Token(tokenCode,atribute))
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



def A_sint():
	global sig_token , TLcopy
	TLcopy = TL
	sig_token = TLcopy[0].atributo
	P(); # deduzco que es el axioma , en las diapositivas no pone nada
	if sig_token != '$' # esto no se si es asi porque no se de donde sacamos el $ ya que en la TL no tenemos ningun $ a no ser que haya que añadirlo como ultimo token(sigo las diapositivas)
		errorParse('A_sint')
def equipara(t):
	global TLcopy
	if sig_tok == t:
		TLcopy = TLcopy[1:]
		sig_token = TLcopy[0].atributo
	else
		errorParse('equipara')


def errorParse(error):
	#habra que cambiarlo
	print('Error en regla %s',error)
	exit()

# Una función para cada no terminal (y una rama para cada regla)

def E():
	if sig_token == '!' or sig_token == '(' or sig_token == 'CAD' or sig_token == 'ENT' or sig_token == 'FALSE' or sig_token == 'ID' or sig_token == 'TRUE' :
		parse.add(1) # hay que cambiar estos numeros en funcion del automata sintactico que debemos crear
		R()
		E1()
	else:
		errorParse('E')

def E1():
	global sig_token
	if sig_token == '&&':
		parse.add(2)
		equipara('&&')
		R()
		E1()
	elif sig_token == ')' or sig_token == ',' or sig_token == ';': # FOLLOW de E1  =  { ) , ; }
		parse.add(3)
	else:
		errorParse('E1')

def R():
	if sig_token == '!' or sig_token == '(' or sig_token =='CAD' or sig_token =='ENT' or sig_token =='FALSE' or sig_token =='ID' or sig_token =='TRUE':
		parse.add(4)
		U()
		R1()
	else:
		errorParse('R')

def R1():
	global sig_token
	if sig_token == '==':
		parse.add(5)
		equipara('==')
		U()
		R1()
	elif sig_token == '!=':
		parse.add(6)
		equipara('!=')
		U()
		R1()
	elif sig_token == '&&' or sig_token == ')' or sig_token == ',' or sig_token == ';':
		parse.add(7)
	else
		errorParse('R1')


def U():
	if sig_token == '!' or sig_token == '(' or sig_token =='CAD' or sig_token =='ENT' or sig_token =='FALSE' or sig_token =='ID' or sig_token =='TRUE':
		parse.add(8)
		V()
		U1()
	else:
		errorParse('U')

def U1():
	global sig_token
	if sig_token == '+':
		parse.add(9)
		equipara('+')
		V()
		U1()
	elif sig_token == '-':
		parse.add(10)
		equipara('-')
		V()
		U1()
	elif sig_token == '!=' or sig_token == '&&' or sig_token == ')' or sig_token == ',' or sig_token == ';' or sig_token == '==':
		parse.add(11)
	else
		errorParse('R2')

def V():
	 if sig_token == 'ID'
	 	parse.add(12)
	 	equipara('ID')
	 	V1()
	 elif sig_token == '(':
	 	parse.add(16)
	 	equipara('(')
	 	E()
	 	equipara(')')
	 elif sig_token == 'ENT'
	 	parse.add(17)
	 	equipara('ENT')
	 elif sig_token == 'CAD'
	 	parse.add(17)
	 	equipara('CAD')
	 elif sig_token == 'TRUE'
	 	parse.add(17)
	 	equipara('TRUE')
	 elif sig_token == 'FALSE'
	 	parse.add(17)
	 	equipara('FALSE')
	 elif sig_token == '!'
	 	parse.add(18)
	 	equipara('!')
	 	equipara('ID')


def V1():
	if sig_token == '(':
	 	parse.add(13)
	 	equipara('(')
	 	L()
	 	equipara(')')
	elif sig_token == '++':
	 	parse.add(14)
	 	equipara('++')
	elif sig_token == '!=' or sig_token == '&&' or sig_token == ')' or sig_token == '+' or sig_token == ',' or sig_token == '-' or sig_token == ';' or sig_token == '==':
		parse.add(15)
	else:
		errorParse('V1')



def S():
	if sig_token == 'ID':
		parse.add(19)
		equipara('ID')
		S1()

	elif sig_token == 'ALERT':
		parse.add(22)
		equipara('ALERT')
		equipara('(')
		E()
		equipara(')')
		equipara(';') 
	elif sig_token == 'INPUT':
		parse.add(23)
		equipara('INPUT')
		equipara('(')
		equipara('ID')
		equipara(')')
		equipara(';')
	elif sig_token == 'RETURN':
		parse.add(24)
		equipara('RETURN')
		X()
		equipara(';')
def S1(): 
	if sig_token == '=':
		parse.add(20)
		equipara('=')
		E()
		equipara(';')
	elif sig_token == '(':
		parse.add(21)
		equipara('(')
		L()
		equipara(')')
		equipara(';')
	else:              # parece que no hay follow de s1 comprobar
		errorParse('S1')


def L():
	if sig_token == '!' or sig_token == '(' or sig_token =='CAD' or sig_token =='ENT' or sig_token =='FALSE' or sig_token =='ID' or sig_token =='TRUE':
		parse.add(25)
		E()
		Q()
	elif sig_token == ')':
		parse.add(26)
	else:
		errorParse('L')

def Q():
	if sig_token == ',':
		parse.add(27)
		equipara(',')
		E()
		Q()
	elif sig_token == ')':
		parse.add(28)
	else 
		errorParse('Q')

def X():
	if sig_token == '!' or sig_token == '(' or sig_token =='CAD' or sig_token =='ENT' or sig_token =='FALSE' or sig_token =='ID' or sig_token =='TRUE':
		parse.add(29)
		E()
	elif
		parse.add(30)
	else:
		errorParse('X')

def B():
	if sig_token == 'IF':
		parse.add(31)
		equipara('IF')
		equipara('(')
		E()
		equipara(')')
		S()
	elif sig_token == 'LET':
		parse.add(32)
		equipara('LET')
		T()
		equipara('ID')
	elif sig_token == 'DO':
	 	parse.add(33)
	 	equipara('DO')
	 	equipara('{')
	 	C()
	 	equipara('}')
	 	equipara('WHILE')
	 	equipara('(')
	 	E()
	 	equipara(')')
	 	equipara(';')
	elif sig_token == 'ALERT' or sig_token == 'ID' or sig_token == 'INPUT' or sig_token == 'RETURN':
		parse.add(34)
		S()
	else:
		errorParse('B')

def T(): 
	if sig_token == 'NUMBER':
		parse.add(35)
		equipara('NUMBER')
	elif sig_token == 'BOOLEAN':
		parse.add(36)
		equipara('BOOLEAN')
	elif sig_token == 'STRING':
		parse.add(37)
		equipara('STRING')
	else:
		errorParse('T')

def F():
	if sig_token == 'FUNCTION':
		parse.add(38)
		equipara('FUNCTION')
		H()
		equipara('ID')
		equipara('(')
		A()
		equipara(')')
		equipara('{')
		C()
		equipara('}')
	else:
		errorParse('F')


def H():
	if sig_token == 'BOOLEAN' or sig_token == 'NUMBER' or sig_token == 'STRING':
		parse.add(39)
		T()
	elif sig_token == 'ID':
		parse.add(40)
	else:
		errorParse('H')
		
def A():
	if sig_token == 'BOOLEAN' or sig_token == 'NUMBER' or sig_token == 'STRING':
		parse.add(41)
		T()
		equipara('ID')
		K()
	elif sig_token == ')':
		parse.add(42)
	else:
		errorParse('A')
		
def K():
 	if sig_token == ',':
 		parse.add(43)
 		equipara(',')
 		T()
 		equipara('ID')
 		K()
 	elif sig_token == ')':
 		parse.add(44)
 	else:
 		errorParse('K')

def C():
	if sig_token == 'ALERT' or if sig_token == 'DO' or if sig_token == 'ID' or if sig_token == 'IF' or if sig_token =='INPUT' or if sig_token =='LET' or if sig_token =='RETURN':
		parse.add(45)
		B()
		C()
	elif sig_token == '}':
		parse.add(46)
	else:
		errorParse('C')

def P():
	if sig_token == 'ALERT' or if sig_token == 'DO' or if sig_token == 'ID' or if sig_token == 'IF' or if sig_token =='INPUT' or if sig_token =='LET' or if sig_token =='RETURN':
		parse.add(47)
		B()
		P()
	elif sig_token == 'FUNCTION':
		parse.add(48)
		F()
		P()
	elif sig_token == '$'
		equipara('$') # habra que añadir a TL un dolar al final para saber que hemos acabado el archivo
	else:
		errorParse('P')
		






						

def main():
	global tokenFile,errorFile,openComment,TSFile,tsAcNumber,tsOgNumber,TS,lastLine
	
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
	test.close()
	errorFile.close()
	tokenFile.close()
	TSFile.close()


	


if __name__== '__main__':
  	main()