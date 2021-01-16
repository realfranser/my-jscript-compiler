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
	def __init__(self,token,linea):
		self.token = token
		self.linea = linea

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


def addToTS(numTabla=0,lexema=None,tipo= None,despl=0,param=[],tipoRetorno = None):
	if getLexema(TS,lexema) == False:
		TS.append(Simbolo(numTabla,lexema,tipo,despl,param,tipoRetorno)) # ACTUALIZAR !!! en caso de que ya exista actualizar el valor
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
							tt = Token(atribute,linea)
							TL.append(Token(atribute,linea))
							found = True
							break
			if found == False:
				pos = addToTS(0,atribute) ################# Editar cuando hagamos semantico
				token = '<ID,' + str(pos) + '>\n' ## el Analizador Lexico añade los lexemas de tipo ID a la Tabla de Símbolos
				tt = Token('ID',linea)
				TL.append(Token('ID',linea))
				

		else:	
			token = '<' + tokenCode + ',' + atribute + '>\n'
			if(tokenCode == 'chain' or tokenCode == 'wholeConst'):
				tt = Token(tokenCode,linea)
				TL.append(Token(tokenCode,linea))
			else:
				tt = Token(atribute,linea)
				TL.append(Token(atribute,linea))

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
			if(openComment == False):
					print('!! Atención: */ comentario en bloque cerrado en caracter: '+
															str(cerradoEnCaracter)+' ,linea: '+str(lineCounter))
			if not lista and openComment and (lastLine == lineCounter+1):
					generarError('++ Error: /* comentario en bloque no se cierra')
					return lista,token

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

		elif leerChar(lista)== '\'':
			cadena = '\"'
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
				if(openComment == True):
					print('!! Atención: /* comentario en bloque no se cierra, abierto en caracter: '+
																str(aperturaEnCaracter)+ ' ,linea: ' + str(lineCounter))

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
	return Token('$',lineCounter)#final de archivo		

def A_sint():
	global sig_token, lineaSint,linea,tokenLines
	linea = leerLinea(tokenLines)
	token=getNextToken()
	sig_token=token.token
	lineaSint =token.linea
	p= P() # deduzco que es el axioma , en las diapositivas no pone nada
	print(p)
	if sig_token != '$':
		errorParse(Token('A_sint',lineaSint))

def equipara(t):
	global sig_token,lineaSint
	if sig_token == t:
		token=getNextToken()
		sig_token=token.token
		lineaSint =token.linea
	else:
		errorParse(Token('equipara',lineaSint))


def errorParse(error):
	#habra que cambiarlo
	eP = 'ErrorSintactico: Error antes de token \''+str(error.token) + '\',linea:' + str(error.linea)
	generarError(eP)
	exit()

# Una función para cada no terminal (y una rama para cada regla)

def E():
	print('estoy en e')
	if sig_token == 'not' or sig_token == 'openPar' or sig_token == 'chain' or sig_token == 'wholeConst' or sig_token == 'false' or sig_token == 'ID' or sig_token == 'true' :
		parse.append(1) 
		R()
		E1()
	else:
		errorParse(Token(sig_token,lineaSint))

def E1():
	global sig_token
	print('estoy en e1')
	if sig_token == 'and':
		parse.append(2)
		equipara('and')
		r =R()
		e1=E1()
		if(r.tipo != e1.tipo): # no se si es asi
			print('error solo para booleanos')
			return Simbolo(0,None,'err',0,[],None)

	elif sig_token == 'closePar' or sig_token == 'colon' or sig_token == 'semicolon': # FOLLOW de E1  =  { ) , ; }
		parse.append(3)
		return Simbolo(0,None,'None',0,[],None)
	else:
		errorParse(Token(sig_token,lineaSint))

def R():
	print('estoy en r')
	if sig_token == 'not' or sig_token == 'openPar' or sig_token =='chain' or sig_token =='wholeConst' or sig_token =='false' or sig_token =='ID' or sig_token =='true':
		parse.append(4)
		u = U()
		r1 = R1()
		print(u.tipo)
		print(r1.tipo)
		if(u.tipo != r1.tipo): # no se si es asi
			print('Error en R creo que es de booleano algo asi')
			return Simbolo(0,None,'err',0,[],None)

		return Simbolo(0,None,'boolean',1,[],None)
	else:
		errorParse(Token(sig_token,lineaSint))

def R1():
	global sig_token
	print('estoy en r1')
	if sig_token == 'equals':
		parse.append(5)
		equipara('equals')
		u = U()
		r1 = R1()
		if(u.tipo != r1.tipo): # no se si es asi
			print('Error en R1 no son del msimo tipo')
			return Simbolo(0,None,'err',0,[],None)

		return Simbolo(0,None,r1.tipo,r1.despl,[],None)

	elif sig_token == 'notEquals':
		parse.append(6)
		equipara('notEquals')
		u=U()
		r1=R1()
		if(u.tipo != r1.tipo): # no se si es asi
			print('Error en R1 no son del msimo tipo')
			return Simbolo(0,None,'err',0,[],None)

		return Simbolo(0,None,r1.tipo,r1.despl,[],None)

	elif sig_token == 'and' or sig_token == 'closePar' or sig_token == 'colon' or sig_token == 'semicolon':
		parse.append(7)
		return Simbolo(0,None,'None',0,[],None)
	else:
		errorParse(Token(sig_token,lineaSint))


def U():
	print('estoy en u')
	if sig_token == 'not' or sig_token == 'openPar' or sig_token =='chain' or sig_token =='wholeConst' or sig_token =='false' or sig_token =='ID' or sig_token =='true':
		parse.append(8)
		v =V()
		u1 =U1()
		print(v.tipo)
		print(u1.tipo)
		#if v.tipo != u1.tipo:
			#print('error solo se suman tipos iguales u')
			#return Simbolo(0,None,'err',0,[],None)
		return Simbolo(0,None,v.tipo,v.despl,[],None)

	else:
		errorParse(Token(sig_token,lineaSint))

def U1():
	global sig_token
	print('estoy en u1')
	print(sig_token)
	if sig_token == 'plus':
		parse.append(9)
		equipara('plus')
		v =V()
		u1 =U1()
		if v.tipo != u1.tipo:
			print('error solo se suman tipos iguales u1')
			return Simbolo(0,None,'err',0,[],None)
		return Simbolo(0,None,u1.tipo,u1.despl,[],None)
	elif sig_token == 'minus':
		parse.append(10)
		equipara('minus')
		v =V()
		u1 =U1()
		if v.tipo != u1.tipo:
			print('error solo se suman tipos iguales')
			return Simbolo(0,None,'err',0,[],None)
		return Simbolo(0,None,u1.tipo,u1.despl,[],None)

	elif sig_token == 'notEquals' or sig_token == 'and' or sig_token == 'closePar' or sig_token == 'colon' or sig_token == 'semicolon' or sig_token == 'equals':
		parse.append(11)
		return Simbolo(0,None,'None',0,[],None)
	else:
		errorParse(Token(sig_token,lineaSint))

def V():
	 print('estoy en v')
	 print(sig_token)
	 if sig_token == 'ID':
	 	parse.append(12)
	 	equipara('ID')
	 	v1 = V1()
	 	return Simbolo(0,None,'None',0,[],None)
	 elif sig_token == 'openPar':
	 	parse.append(13)
	 	equipara('openPar')
	 	e = E()
	 	equipara('closePar')
	 	return Simbolo(0,None,e.tipo,e.despl,[],None)

	 elif sig_token == 'wholeConst':
	 	parse.append(14)
	 	equipara('wholeConst')
	 	return Simbolo(0,None,'int',2,[],None)
	 elif sig_token == 'chain':
	 	parse.append(15)
	 	equipara('chain')
	 	return Simbolo(0,None,'chain',64,[],None)# no se si esta bien el desp mb = 1
	 elif sig_token == 'true':
	 	parse.append(16)
	 	equipara('true')
	 	return Simbolo(0,None,'boolean',1,[],None)
	 elif sig_token == 'false':
	 	parse.append(17)
	 	equipara('false')
	 	return Simbolo(0,None,'boolean',1,[],None)
	 elif sig_token == 'not':
	 	parse.append(18)
	 	equipara('not')
	 	equipara('ID')
	 	return Simbolo(0,None,'boolean',1,[],None)# no se si es asi supongo que es un booleano


def V1():
	#print(sig_token)
	if sig_token == 'openPar':
	 	parse.append(19)
	 	equipara('openPar')
	 	l =L()
	 	equipara('closePar')
	 	return Simbolo(0,None,'None',0,l.param,None)
	elif sig_token == 'autoInc':
	 	parse.append(20)
	 	equipara('autoInc')
	 	return Simbolo(0,None,'int',2,[],None) # no se si es asi supongo que es un entero
	elif sig_token == 'notEquals' or sig_token == 'and' or sig_token == 'closePar' or sig_token == 'plus' or sig_token == 'colon' or sig_token == 'minus' or sig_token == 'semicolon' or sig_token == 'equals':
		parse.append(21)
		return Simbolo(0,None,'None',0,[],None)
	else:
		errorParse(Token(sig_token,lineaSint))



def S():
	print('Estoy en s')
	if sig_token == 'ID':
		parse.append(22)
		equipara('ID')
		s1 = S1()
		if(s1.tipo != 'int'): # revisar va a estar mal
			print('asignado tipo erroneo regla S')
			return Simbolo(0,None,'err',0,[],None)

		return Simbolo(0,None,'ok',0,[],None)
	elif sig_token == 'alert':
		parse.append(23)
		equipara('alert')
		equipara('openPar')
		e = E()
		equipara('closePar')
		equipara('semicolon')
		return Simbolo(0,None,'ok',0,[],None)
	elif sig_token == 'input':
		parse.append(24)
		equipara('input')
		equipara('openPar')
		equipara('ID')
		equipara('closePar')
		equipara('semicolon')
		return Simbolo(0,None,'ok',0,[],None)
	elif sig_token == 'return':
		parse.append(25)
		equipara('return')
		x = X()
		equipara('semicolon')
		return Simbolo(0,None,'ok',x.despl,[],None)
def S1(): 
	print('estoy en s1')
	if sig_token == 'equal':
		parse.append(26)
		equipara('equal')
		e = E()
		equipara('semicolon')
		return Simbolo(0,None,e.tipo,e.despl,[],None)
	elif sig_token == 'openPar':
		parse.append(27)
		equipara('openPar')
		l = L()
		equipara('closePar')
		equipara('semicolon')
		return Simbolo(0,None,'None',0,l.param,None)
	else:              
		errorParse(Token(sig_token,lineaSint))


def L():
	#print(sig_token)
	if sig_token == 'not' or sig_token == 'openPar' or sig_token =='chain' or sig_token =='wholeConst' or sig_token =='false' or sig_token =='ID' or sig_token =='true':
		parse.append(28)
		e =E()
		q =Q()
		param = []
		param.append([e.tipo,0])
		param.append(q.param)
		return Simbolo(0,None,'None',0,param,None)
	elif sig_token == 'closePar':
		parse.append(29)
		return Simbolo(0,None,'None',0,[],None)
	else:
		errorParse(Token(sig_token,lineaSint))

def Q():
	#print(sig_token)
	if sig_token == 'colon':
		parse.append(30)
		equipara('colon')
		e = E()
		q = Q()
		param = []
		param.append([e.tipo,0])
		param.append(q.param)
	elif sig_token == 'closePar':
		parse.append(31)
		return Simbolo(0,None,'None',0,[],None)
	else :
		errorParse(Token(sig_token,lineaSint))

def X():
	#print(sig_token)
	if sig_token == 'not' or sig_token == 'openPar' or sig_token =='chain' or sig_token =='wholeConst' or sig_token =='false' or sig_token =='ID' or sig_token =='true':
		parse.append(32)
		e= E()
		return Simbolo(0,None,e.tipo,e.despl,[],None)
	elif sig_token == 'semicolon':
		parse.append(33)
		return Simbolo(0,None,'None',0,[],None)
	else:
		errorParse(Token(sig_token,lineaSint))

def B():
	print('estoy en b')
	if sig_token == 'if':
		parse.append(34)
		equipara('if')
		equipara('openPar')
		e =E()
		if e.tipo != 'boolean':
			print('error el if solo puede ser boolean')
		equipara('closePar')
		s =S()
		if s.tipo == 'err':
			print('sentencia condicional incorrecta')
		return Simbolo(0,None,s.tipo,0,[],None)
	elif sig_token == 'let':
		parse.append(35)
		equipara('let')
		t=T()
		equipara('ID')
		equipara('semicolon')
		return Simbolo(0,None,'None',0,[],None) # no se si es asi
	elif sig_token == 'alert' or sig_token == 'ID' or sig_token == 'input' or sig_token == 'return':
		parse.append(36)
		s = S()
		if s.tipo == 'err':
			print('error sentencia incorrecta regla B ')
		return Simbolo(0,None,s.tipo,0,[],None)
	elif sig_token == 'do':
	 	parse.append(37)
	 	equipara('do')
	 	equipara('openBraq')
	 	c = C()
	 	equipara('closeBraq')
	 	equipara('while')
	 	equipara('openPar')
	 	e = E()
	 	if e.tipo != 'boolean':
	 		print('error en while , no es un booleano')
	 	equipara('closePar')
	 	equipara('semicolon')
	 	return Simbolo(0,None,'None',0,[],None)
	else:
		errorParse(Token(sig_token,lineaSint))

def T():
	#print(sig_token)
	if sig_token == 'number':
		parse.append(38)
		equipara('number')
		return Simbolo(0,None,'int',2,[],None)
	elif sig_token == 'boolean':
		parse.append(39)
		equipara('boolean')
		return Simbolo(0,None,'boolean',1,[],None)
	elif sig_token == 'string':
		parse.append(40)
		equipara('string')
		return Simbolo(0,None,'chain',64,[],None)
	else:
		errorParse(Token(sig_token,lineaSint))

def F():
	#print(sig_token)
	if sig_token == 'function':
		parse.append(41)
		equipara('function')
		h = H()
		equipara('ID')
		equipara('openPar')
		a = A()
		equipara('closePar')
		equipara('openBraq')
		c = C()
		equipara('closeBraq')
		if(h.tipo == c.tipo):
			return Simbolo(0,None,'ok',0,[],None)
		else:
			return Simbolo(0,None,'err',0,[],None)
	else:
		errorParse(Token(sig_token,lineaSint))


def H():
	#print(sig_token)
	if sig_token == 'boolean' or sig_token == 'number' or sig_token == 'string':
		parse.append(42)
		t = T()
		return Simbolo(0,None,t.tipo,t.despl,[],None)
	elif sig_token == 'ID':
		parse.append(43)
		return Simbolo(0,None,'None',0,[],None)
	else:
		errorParse(Token(sig_token,lineaSint))
		
def A():
	#print(sig_token)
	if sig_token == 'boolean' or sig_token == 'number' or sig_token == 'string':
		parse.append(44)
		t = T()
		equipara('ID')
		k = K()
		params = []
		params.append([t.tipo,0])
		for s in k.params:
			params.append([s,0])
		return Simbolo(0,None,'None',0,params,None)
	elif sig_token == 'closePar':
		parse.append(45)
		return Simbolo(0,None,'None',0,[],None)
	else:
		errorParse(Token(sig_token,lineaSint))
		
def K():
	#print(sig_token)
	if sig_token == 'colon':
 		parse.append(46)
 		equipara('colon')
 		t =T()
 		equipara('ID')
 		k =K()
 		params=[]
 		params.append([t.tipo,0])
 		for s in k.params:
 			params.append([s,0])
 		return Simbolo(0,None,'None',0,params,None)
	elif sig_token == 'closePar':
 		parse.append(47)
 		return Simbolo(0,None,'None',0,[],None)
	else:
 		errorParse(Token(sig_token,lineaSint))

def C():
	#print(sig_token)
	if sig_token == 'alert' or  sig_token == 'do' or  sig_token == 'ID' or sig_token == 'if' or  sig_token =='input' or  sig_token =='let' or  sig_token =='return':
		parse.append(48)
		B()
		C()
		return Simbolo(0,None,'None',0,[],None)
	elif sig_token == 'closeBraq':
		parse.append(49)
		return Simbolo(0,None,'None',0,[],None)
	else:
		errorParse(Token(sig_token,lineaSint))

def P():
	#print(sig_token)
	if sig_token == 'alert' or  sig_token == 'do' or  sig_token == 'ID' or  sig_token == 'if' or  sig_token =='input' or  sig_token =='let' or  sig_token =='return':
		parse.append(50)
		B()
		P()
	elif sig_token == 'function':
		parse.append(51)
		F()
		P()
	elif sig_token == '$':
		parse.append(52)
		#hemos terminado
		# habra que añadir a TL un dolar al final para saber que hemos acabado el archivo
	else:
		errorParse(Token(sig_token,lineaSint))
		




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
	# 		print(token)
			
			
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