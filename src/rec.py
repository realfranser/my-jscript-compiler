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
	def __init__ (self,numTabla=0,lexema=None,tipo= None,despl=0,param=[],tipoRetorno = None):
		# tipo Simbolo , Tabla de Simbolos matriz de 'Simbolo',
		self.numTabla = numTabla # Tabla a la que pertenece el simbolo
		self.lexema = lexema # lexema de linea 
		self.tipo = tipo 	 # tipo de identificador ej: int, boolean ,'cadena'
		self.despl = despl   # direccion relativa
		self.param = param  # lista de tipo [[tipo param,modoparam],[tipo param,modoparam],...]
		#self.numParam = numParam # parametros subprograma
		#self.tipoParam = tipoParam # lista tipos parametros subprograma
		#self.modoParam = tipoRetorno # lista modo de paso parametro subprograma
		self.tipoRetorno = tipoRetorno  # tipo devuelto por funcion
		#self.etiqFuncion = etiqFuncion # Etiqueta tipo funcion
		#self.param = param # Parametro no pasado por valor
		
class Token:
	def __init__(self,token,linea,atribute):
		self.token = token
		self.linea = linea
		self.atribute= atribute

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
			return i
	return Simbolo(numTabla=0,lexema=None,tipo= None,despl=0,param=[],tipoRetorno=None)


def addToTS(simbolo):
	if getLexema(TS,Simbolo)!= Simbolo(numTabla=0,lexema=None,tipo= None,despl=0,param=[],tipoRetorno=None) and Simbolo != Simbolo(numTabla=0,lexema=None,tipo= None,despl=0,param=[],tipoRetorno=None):
		TS.append(simbolo) # ACTUALIZAR !!! en caso de que ya exista actualizar el valor
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

				# if simbolo.numParam != 0:
				# 	lineaTS = '	+ numParam: ' + str(simbolo.numParam) +'\n'
				# 	TSFile.write(lineaTS)
				# if simbolo.tipoParam and simbolo.modoParam:
				# 		counter = 1
				# 		for j in simbolo.tipoParam :
				# 			#for i in simbolo.modoParam:   ------ revisar in da future
				# 			lineaTS = '	+ TipoParam'+str(counter)+': ' + j +'\n'
				# 			TSFile.write(lineaTS)
				# 			lineaTS = '	+ ModoParam'+str(counter)+': ' + j +'\n'
				# 			TSFile.write(lineaTS)

				# if simbolo.tipoRetorno != None:
				# 	lineaTS = '	+ TipoRetorno: ' + simbolo.tipoRetorno +'\n'
				# 	TSFile.write(lineaTS)

				# if simbolo.etiqFuncion != None:
				# 	lineaTS = '	+ tipo: ' + simbolo.etiqFuncion +'\n'
				# 	TSFile.write(lineaTS)

				# if simbolo.param != None:
				# 	lineaTS = '	+ tipo: ' + simbolo.param +'\n'
				# 	TSFile.write(lineaTS)
	
								
def generarToken(tokenCode,atribute,linea):
	found =False
	with  open(sourceTokenFilePath) as sourceTokenFile:
		data = json.load(sourceTokenFile)
		if tokenCode == 'reservedWord':#buscar en token.json
			for i in data['tokens']:
				if (i['tokenCode'] == 'reservedWord'):
					for k in i['tokenList']:
						if k['atribute']==atribute:
							token = '<reservedWord,' + atribute + '>\n'
							tt = Token(atribute,linea,atribute)
							TL.append(Token(atribute,linea,atribute))
							found = True
							break
			if found == False:
				#pos = addToTS(0,atribute) ################# Editar cuando hagamos semantico
				token = '<ID,' + str(0) + '>\n' ## el Analizador Lexico añade los lexemas de tipo ID a la Tabla de Símbolos
				tt = Token('ID',linea,atribute)
				TL.append(Token('ID',linea,atribute))
				

		else:	
			token = '<' + tokenCode + ',' + atribute + '>\n'
			if(tokenCode == 'chain' or tokenCode == 'wholeConst'):
				tt = Token(tokenCode,linea,atribute)
				TL.append(Token(tokenCode,linea,atribute))
			else:
				tt = Token(atribute,linea,atribute)
				TL.append(Token(atribute,linea,atribute))

		tokenFile.write(token)
		sourceTokenFile.close()
		return tt

def generarError(error):
		errorFile.write(error)
		errorFile.write('\n')
		exit()
		
		
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

def analizadorLinea(lista, lineCounter):
	global openComment,lastLine
	contadorCaracter = 0
	token='null'
	while lista:
		if openComment == True:  # comentario abierto en otra llamada
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
			#if(openComment == False):
					
															
			if not lista and openComment and (lastLine == lineCounter+1):
					generarError('++ Error: /* comentario en bloque no se cierra')
					return lista,token

		elif leerChar(lista) == '\n' or leerChar(lista) == ' ' or leerChar(lista) == '\t':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			


		elif leerChar(lista) == '+':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			if leerChar(lista) == '+':
				contadorCaracter = contadorCaracter+1
				lista = lista[1:]
				token = generarToken('autoIncOp','autoinc',lineCounter)
			else:
				token = generarToken('aritOp','plus',lineCounter)
			return lista,token

		elif leerChar(lista) == '-':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			if leerChar(lista) == '-':
				contadorCaracter = contadorCaracter+1
				lista = lista[1:]
				token = generarToken('autoDecOp','autodec',lineCounter)
			else:
				token = generarToken('aritOp','minus',lineCounter)
			return lista,token

		elif leerChar(lista) == '=':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			if leerChar(lista) == '=':
				contadorCaracter = contadorCaracter+1
				lista = lista[1:]
				token = generarToken('relOp','equals',lineCounter)
			else:
				token = generarToken('asigOp','equal',lineCounter)
			return lista,token

		elif leerChar(lista) == '!':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			if leerChar(lista) == '=':
				contadorCaracter = contadorCaracter+1
				lista = lista[1:]
				token = generarToken('relOp','notEquals',lineCounter)
			else:
				token = generarToken('logOp','not',lineCounter)
			return lista,token

		elif leerChar(lista)=='&':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			if leerChar(lista) == '&':
				contadorCaracter = contadorCaracter+1
				lista = lista[1:]
				token = generarToken('logOp','and',lineCounter)
			else:
				generarError('++ Error: & esta solo en caracter: '+str(contadorCaracter)+' ,linea: '+str(lineCounter))
			return lista,token

		elif leerChar(lista) == ',':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			token = generarToken('separator','colon',lineCounter)
			return lista,token

		elif leerChar(lista) == ';':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			token = generarToken('separator','semicolon',lineCounter)
			return lista,token

		elif leerChar(lista) == '{':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			token = generarToken('separator','openBraq',lineCounter)
			return lista,token

		elif leerChar(lista) == '}':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			token = generarToken('separator','closeBraq',lineCounter)
			return lista,token

		elif leerChar(lista) == '(':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			token = generarToken('separator','openPar',lineCounter)
			return lista,token

		elif leerChar(lista) == ')':
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			token = generarToken('separator','closePar',lineCounter)
			return lista,token

		elif leerChar(lista)== '\"':
			cadena = '\"'
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
			seCierra = False
			aperturaEnCaracter=contadorCaracter
			while lista:
				cadena = cadena + leerChar(lista)
				if leerChar(lista)== '\"':
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
				cadena = cadena[:-1]
				cadena = cadena + '\"'
				token = generarToken('chain',cadena,lineCounter)

			elif seCierra:
			  	generarError('++ Error: \' cadena supera los 64 caracteres por: '
																+str(len(cadena)-66) +' ,en la linea: ' + str(lineCounter))
			return lista,token

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

			token = generarToken('wholeConst',numero,lineCounter)
			return lista,token

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

			token = generarToken('reservedWord',alphanum,lineCounter)
			return lista,token


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
				#if(openComment == True):
					
																

			else:
			  generarError('++ Error: / esta solo en caracter: '+str(contadorCaracter)+' ,linea: '+str(lineCounter))
			return lista,token

		else:
			generarError('++ Error: Caracter no reconocido:['+ leerChar(lista) + '] en caracter: '+str(contadorCaracter)+' ,linea: '+str(lineCounter))
			contadorCaracter = contadorCaracter+1
			lista = lista[1:]
		return lista,token

	return lista,token 


def getNextToken():
	global tokenLines,lineCounter,linea
	token=[]
	while tokenLines:
		if not linea:
			tokenLines = tokenLines[1:]
			linea = leerLinea(tokenLines)
			lineCounter= lineCounter+1
		linea,token=analizadorLinea(linea,lineCounter)
		if(token!='null'):
			return token;
		#else:
			#getNextToken()
	return Token('$',lineCounter,'EOF')#final de archivo		

def A_sint():
	global sig_token, lineaSint,linea,tokenLines
	linea = leerLinea(tokenLines)
	
	sig_token=getNextToken()
	lineaSint =sig_token.linea
	p= P(Simbolo(numTabla=0,lexema=None,tipo= None,despl=0,param=[],tipoRetorno=None)) # deduzco que es el axioma , en las diapositivas no pone nada
	
	if sig_token.token != '$':
		errorParse(Token('A_sint',lineaSint,'error'))

def equipara(t):
	global sig_token,lineaSint
	if sig_token.token == t:
		sig_token=getNextToken()
		lineaSint =sig_token.linea
	else:
		errorParse(Token('equipara',lineaSint,'error'))


def errorParse(error):
	#habra que cambiarlo
	eP = 'ErrorSintactico: Error antes de token \''+str(error.token) + '\',linea:' + str(error.linea)
	generarError(eP)
	exit()

# Una función para cada no terminal (y una rama para cada regla)

def E(simbolo):
	if sig_token.token == 'not' or sig_token.token == 'openPar' or sig_token.token == 'chain' or sig_token.token == 'wholeConst' or sig_token.token == 'false' or sig_token.token == 'ID' or sig_token.token == 'true' :
		parse.append(1) 
		t = R(simbolo)
		tt = E1(t)
		return tt
	else:
		errorParse(Token(sig_token.token,lineaSint,'error'))

def E1(simbolo):
	
	if sig_token.token == 'and':
		parse.append(2)
		equipara('and')
		t =R(simbolo)
		tt=E1(t)
		return tt
	elif sig_token.token == 'closePar' or sig_token.token == 'colon' or sig_token.token == 'semicolon': # FOLLOW de E1  =  { ) , ; }
		parse.append(3)
		return simbolo
	else:
		errorParse(Token(sig_token.token,lineaSint,'error'))

def R(simbolo):
	
	if sig_token.token == 'not' or sig_token.token == 'openPar' or sig_token.token =='chain' or sig_token.token =='wholeConst' or sig_token.token =='false' or sig_token.token =='ID' or sig_token.token =='true':
		parse.append(4)
		t= U(simbolo)
		tt = R1(t)
		return tt
	else:
		errorParse(Token(sig_token.token,lineaSint,'error'))

def R1(simbolo):
	
	if sig_token.token == 'equals':
		parse.append(5)
		equipara('equals')
		t = U(simbolo)
		tt = R1(t)
		return tt
	elif sig_token.token == 'notEquals':
		parse.append(6)
		equipara('notEquals')
		t=U(simbolo)
		tt=R1(t)
		return tt
	elif sig_token.token == 'and' or sig_token.token == 'closePar' or sig_token.token == 'colon' or sig_token.token == 'semicolon':
		parse.append(7)
		return simbolo
	else:
		errorParse(Token(sig_token.token,lineaSint,'error'))


def U(simbolo):
	
	if sig_token.token == 'not' or sig_token.token == 'openPar' or sig_token.token =='chain' or sig_token.token =='wholeConst' or sig_token.token =='false' or sig_token.token =='ID' or sig_token.token =='true':
		parse.append(8)
		t =V(simbolo)
		tt =U1(t)
		return tt
	else:
		errorParse(Token(sig_token.token,lineaSint,'error'))

def U1(simbolo):
	if sig_token.token == 'plus':
		parse.append(9)
		equipara('plus')
		t =V(simbolo)
		tt =U1(t)
		return tt
	elif sig_token.token == 'minus':
		parse.append(10)
		equipara('minus')
		t =V(simbolo)
		tt =U1(t)
		return tt
	elif sig_token.token == 'notEquals' or sig_token.token == 'and' or sig_token.token == 'closePar' or sig_token.token == 'colon' or sig_token.token == 'semicolon' or sig_token.token == 'equals':
		parse.append(11)
		return simbolo
	else:
		errorParse(Token(sig_token.token,lineaSint,'error'))

def V(simbolo):
	 
	 if sig_token.token == 'ID':
	 	parse.append(12)
	 	atribute = sig_token.atribute
	 	equipara('ID')
	 	t = V1(simbolo)
	 	t.lexema = atribute
	 	return t
	 elif sig_token.token == 'openPar':
	 	parse.append(13)
	 	equipara('openPar')
	 	t = E(simbolo)
	 	equipara('closePar')
	 	return t
	 elif sig_token.token == 'wholeConst':
	 	parse.append(14)
	 	equipara('wholeConst')
	 	return Simbolo(numTabla=0,lexema=simbolo.lexema,tipo='int',despl=2,param=[],tipoRetorno=None)
	 elif sig_token.token == 'chain':
	 	parse.append(15)
	 	equipara('chain')
	 	return Simbolo(numTabla=0,lexema=simbolo.lexema,tipo='string',despl=64,param=[],tipoRetorno=None)
	 elif sig_token.token == 'true':
	 	parse.append(16)
	 	equipara('true')
	 	return Simbolo(numTabla=0,lexema=simbolo.lexema,tipo='boolean',despl=1,param=[],tipoRetorno=None)
	 elif sig_token.token == 'false':
	 	parse.append(17)
	 	equipara('false')
	 	return Simbolo(numTabla=0,lexema=simbolo.lexema,tipo= 'boolean',despl=1,param=[],tipoRetorno=None)
	 elif sig_token.token == 'not':
	 	parse.append(18)
	 	equipara('not')
	 	equipara('ID')
	 	return Simbolo(numTabla=0,lexema=simbolo.lexema,tipo= 'boolean',despl=1,param=[],tipoRetorno=None)


def V1(simbolo):
	
	if sig_token.token == 'openPar':
	 	parse.append(19)
	 	equipara('openPar')
	 	t =L(simbolo)
	 	equipara('closePar')
	 	return t
	elif sig_token.token == 'autoInc':
	 	parse.append(20)
	 	equipara('autoInc')
	 	return simbolo
	elif sig_token.token == 'notEquals' or sig_token.token == 'and' or sig_token.token == 'closePar' or sig_token.token == 'plus' or sig_token.token == 'colon' or sig_token.token == 'minus' or sig_token.token == 'semicolon' or sig_token.token == 'equals':
		parse.append(21)
		return simbolo
	else:
		errorParse(Token(sig_token.token,lineaSint,'error'))



def S(simbolo):
	
	if sig_token.token == 'ID':
		parse.append(22)
		p = getLexema(TS,sig_token.atribute)
		equipara('ID') # creo que aqui hay que consultar la ts, buscar el id mirar el tipo y contrastar 
		t = S1(simbolo)
		if (t.tipo != p.tipo and t == Simbolo(numTabla=0,lexema=None,tipo= None,despl=0,param=[],tipoRetorno=None)):
			print('malllllll')
		return t
	elif sig_token.token == 'alert':
		parse.append(23)
		equipara('alert')
		equipara('openPar')
		t = E(simbolo)
		equipara('closePar')
		equipara('semicolon')
		return t
	elif sig_token.token == 'input':
		parse.append(24)
		equipara('input')
		equipara('openPar')
		equipara('ID')
		equipara('closePar')
		equipara('semicolon')
		return simbolo
	elif sig_token.token == 'return':
		parse.append(25)
		equipara('return')
		t = X(simbolo)
		equipara('semicolon')
		return t
def S1(simbolo): 
	
	if sig_token.token == 'equal':
		parse.append(26)
		equipara('equal')
		t = E(simbolo)
		equipara('semicolon')
		return t
	elif sig_token.token == 'openPar':
		parse.append(27)
		equipara('openPar')
		t = L(simbolo)
		equipara('closePar')
		equipara('semicolon')
		return t
	else:              
		errorParse(Token(sig_token.token,lineaSint,'error'))


def L(simbolo):
	
	if sig_token.token == 'not' or sig_token.token == 'openPar' or sig_token.token =='chain' or sig_token.token =='wholeConst' or sig_token.token =='false' or sig_token.token =='ID' or sig_token.token =='true':
		parse.append(28)
		t=E(simbolo)
		tt=Q(t)
		return tt
	elif sig_token.token == 'closePar':
		parse.append(29)
		return simbolo
	else:
		errorParse(Token(sig_token.token,lineaSint,'error'))

def Q(simbolo):
	
	if sig_token.token == 'colon':
		parse.append(30)
		equipara('colon')
		t = E(simbolo)
		tt = Q(t)
		return tt
	elif sig_token.token == 'closePar':
		parse.append(31)
		return simbolo
	else :
		errorParse(Token(sig_token.token,lineaSint,'error'))

def X(simbolo):
	
	if sig_token.token == 'not' or sig_token.token == 'openPar' or sig_token.token =='chain' or sig_token.token =='wholeConst' or sig_token.token =='false' or sig_token.token =='ID' or sig_token.token =='true':
		parse.append(32)
		t= E()
		return t
	elif sig_token.token == 'semicolon':
		parse.append(33)
		return simbolo
	else:
		errorParse(Token(sig_token.token,lineaSint,'error'))

def B(simbolo):
	if sig_token.token == 'if':
		parse.append(34)
		equipara('if')
		equipara('openPar')
		t =E(simbolo)

		equipara('closePar')
		tt =S(t)
		return tt
	elif sig_token.token == 'let':
		parse.append(35)
		equipara('let')
		t=T(simbolo)
		t.lexema = sig_token.atribute
		equipara('ID')
		equipara('semicolon')
		addToTS(t)
		return t
	elif sig_token.token == 'alert' or sig_token.token == 'ID' or sig_token.token == 'input' or sig_token.token == 'return':
		parse.append(36)

		t = S(simbolo)
		return t		
	elif sig_token.token == 'do':
	 	parse.append(37)
	 	equipara('do')
	 	equipara('openBraq')
	 	t = C(simbolo)
	 	equipara('closeBraq')
	 	equipara('while')
	 	equipara('openPar')
	 	tt = E(t)
	 	equipara('closePar')
	 	equipara('semicolon')
	 	return tt
	else:
		errorParse(Token(sig_token.token,lineaSint,'error'))

def T(simbolo):
	if sig_token.token == 'number':
		parse.append(38)
		#lexema = sig_token.atribute
		equipara('number')
		
		return Simbolo(numTabla=0,lexema = simbolo.lexema,tipo='int',despl=2,param=[],tipoRetorno=None)
	elif sig_token.token == 'boolean':
		parse.append(39)
		#lexema = sig_token.atribute
		equipara('boolean')
		
		return Simbolo(numTabla=0,lexema =simbolo.lexema,tipo='boolean',despl=1,param=[],tipoRetorno=None)
	elif sig_token.token == 'string':
		parse.append(40)
		#lexema = sig_token.atribute
		equipara('string')
		return Simbolo(numTabla=0,lexema = simbolo.lexema,tipo='string',despl=64,param=[],tipoRetorno=None)
	else:
		errorParse(Token(sig_token.token,lineaSint,'error'))

def F(simbolo):
	
	if sig_token.token == 'function':
		parse.append(41)
		equipara('function')
		t = H(simbolo)
		t.lexema= sig_token.atribute
		t.tipo = 'funcion'
		equipara('ID')
		equipara('openPar')
		tt = A(t)
		print(tt.__dict__)
		equipara('closePar')
		equipara('openBraq')
		ttt = C(tt)
		equipara('closeBraq')
		addToTS(ttt)
		return ttt
	else:
		errorParse(Token(sig_token.token,lineaSint,'error'))


def H(simbolo):
	if sig_token.token == 'boolean' or sig_token.token == 'number' or sig_token.token == 'string':
		parse.append(42)
		t = T(simbolo)
		return t
	elif sig_token.token == 'ID':
		parse.append(43)
		return simbolo
	else:
		errorParse(Token(sig_token.token,lineaSint,'error'))
		
def A(simbolo):

	if sig_token.token == 'boolean' or sig_token.token == 'number' or sig_token.token == 'string':
		parse.append(44)
		t = T(simbolo)
		equipara('ID')
		tt = K(t)
		return tt
	elif sig_token.token == 'closePar':
		parse.append(45)
		return Simbolo
	else:
		errorParse(Token(sig_token.token,lineaSint,'error'))
		
def K(simbolo):
	if sig_token.token == 'colon':
 		parse.append(46)
 		equipara('colon')
 		t =T(simbolo)
 		equipara('ID')
 		tt =K(t)
 		return tt
	elif sig_token.token == 'closePar':
 		parse.append(47)
 		return simbolo
	else:
 		errorParse(Token(sig_token.token,lineaSint,'error'))

def C(simbolo):
	
	if sig_token.token == 'alert' or  sig_token.token == 'do' or  sig_token.token == 'ID' or sig_token.token == 'if' or  sig_token.token =='input' or  sig_token.token =='let' or  sig_token.token =='return':
		
		parse.append(48)
		t=B(simbolo)
		
		tt=C(t)
		return tt
	elif sig_token.token == 'closeBraq':
		parse.append(49)
		return simbolo
	else:
		errorParse(Token(sig_token.token,lineaSint,'error'))

def P(simbolo):
	#print(simbolo.__dict__)
	if sig_token.token == 'alert' or  sig_token.token == 'do' or  sig_token.token == 'ID' or  sig_token.token == 'if' or  sig_token.token =='input' or  sig_token.token =='let' or  sig_token.token =='return':
		parse.append(50)
		t=B(simbolo)
		tt=P(t)
		return tt
	elif sig_token.token == 'function':
		parse.append(51)
		t=F(simbolo)
		tt=P(t)
		return tt
	elif sig_token.token == '$':
		parse.append(52)
		#hemos terminado
		# habra que añadir a TL un dolar al final para saber que hemos acabado el archivo
	else:
		errorParse(Token(sig_token.token,lineaSint,'error'))
		




def main():
	global tokenFile,errorFile,openComment,TSFile,tsAcNumber,tsOgNumber,TS,lastLine,parse, parseFile, tokenLines,lineCounter,linea
	
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
		linea=[]
		#
		# linea = []
		# while tokenLines:
		# 	if not linea:
		# 		tokenLines = tokenLines[1:]
		# 		linea = leerLinea(tokenLines)
		# 		lineCounter= lineCounter+1
		# 	linea,token=analizadorLinea(linea,lineCounter)
		# 	if(token!='null'):
		# 		return token;
	# 	while tokenLines:
	# 		token = getNextToken()
	# 		
			
			
	# # clean up , close files
	# 	writeTS(TS)
	# 	TL.append(Token('$',lastLine)) # se añade para saber que se ha terminado el archivo
		A_sint()
		writeTS(TS)
		writeParse(parse)
	test.close()
	errorFile.close()
	tokenFile.close()
	TSFile.close()


	


if __name__== '__main__':
  	main()