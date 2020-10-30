import json
import argparse
targetFile = 'tokens.json'



delim = [' ','\t']
eol = ['\n']
openComment = False

def estadoCode(estado,word):
	if estado == 1:
		return 'wholeConst'
	if estado == 2:
		return 'reservedWord'
	if estado == 3:
		return 'aritOp'
	if estado == 5: 
		return 'aritOp'	
	if estado == 8:
		return 'logOp'	 
	if estado == 10:
		if word[len(word)-1]!="'":
			print('string no finalizado en la ultima linea')
			return 'error'
		else:
			return 'cadena'	
		
									
def generarToken(tokenCode,atribute):
	with  open(targetFile) as f:
		data = json.load(f)
		print("generando token:"+atribute)
		if tokenCode == 'reservedWord':#buscar en token.json
			print('palabra reservada?')
			for i in data['tokens']:
				if (i['tokenCode'] == 'reservedWord'):
					for k in i['tokenList']:
						print(k['atribute'] + ' == ' + atribute)
						if k['atribute']==atribute:
							print('found')
							token = '<' + atribute + ',>\n'
							break
						else:
							token = '<ID,' + atribute + '>\n'
		else:	
			token = '<' + tokenCode + ',' + atribute + '>\n' 
		
		tokenFile.write(token)
		

def analizadorLexico(file):
		global openComment
		word = ''
		estado = 0
		contLinea=1
		with open(file,'r') as f, open ('error.txt','w') as errorFile:
			lines = f.readlines()
			for line in lines:
				print('siguiente linea')
				counter =0
				while counter in range(len(line)):
					print(counter)
					print('siguiente caracter '+line[counter])
					if estado == 0:
						if openComment == True:
							counter=counter-1
							estado = 6
						elif line[counter] in delim:
							print('------delimitador-------')
						elif line[counter] in eol:
							print('/////final de linea//////')
							contLinea = contLinea +1
							break
						elif line[counter].isdigit() == True:
							estado = 1
						elif line[counter].isalpha() == True:
							estado=2
						elif line[counter] == '+':
							estado = 3
						elif line[counter] == '-':
							estado=4
						elif line[counter] == '/':
							estado = 5
						elif line[counter] == '(':
							generarToken('separator','openPar')
						elif line[counter] == ')':
							generarToken('separator','closePar')
						elif line[counter] == '{':
							generarToken('separator','openBraq')
						elif line[counter] == '}':
							generarToken('separator','closeBraq')	 
						elif line[counter] == '!':
							estado = 8
						elif line[counter] == '&':
							estado = 9
						elif line[counter]=="'":
							estado = 10
						elif line[counter]=='=':
							estado = 11	
						elif line[counter]==';':
							generarToken('separator','semicolon')
						elif line[counter] == ',':
							generarToken('separator','colon')
						else:
							elementoForaneo = True
							causaError = 'error elemento foraneo: '+line[counter]+ ' linea: ' + str(contLinea) + '\n'
							errorFile.write(causaError)
						
						word=line[counter]
						if(counter==len(line)-1) and (line==lines[len(lines)-1]):
							if word == '&' or word == '=' or word == "'":
								causaError = 'error: '+word+ ' linea: ' + str(contLinea) + '\n'
								errorFile.write(causaError)
							elif elementoForaneo == True:
								counter = counter+1
								continue
							else:
								generarToken(estadoCode(estado),word)
						counter = counter+1
						elementoForaneo = False
						continue
					elif estado ==	1:
						if line[counter].isdigit()==True:
							print('es digito ')
							estado=1
							word+=line[counter]
						else:
							estado=0
							counter =counter-1
							print('final digitos')
							generarToken('wholeConst',word)		
					elif estado == 2:
						if line[counter].isdigit() == True  or line[counter].isalpha() == True or line[counter] =='_':
							estado=2
							word+=line[counter]
						else:
							estado=0
							counter = counter-1
							print('final caracteres y numeros y esas cosas nazis')
							generarToken('reservedWord',word)							
					elif estado == 3:
						if line[counter] == '+':
							estado = 0
							generarToken('autoIncOp','autoinc')
						else:
							estado =0
							generarToken('aritOp','plus')
							counter = counter-1
					elif estado == 4:
						if line[counter] == '-':
							estado = 0
							generarToken('autoDecOp','autodec')
						else:
							estado =0
							generarToken('aritOp','minus')
							counter = counter-1
					elif estado ==5:
						if line[counter] =='*':
							openComment=True
							estado = 6
							counter=counter+1
							continue
						else:
							Error('barra sin asterico')	
					elif estado == 6:
						if line[counter] == '*':
							estado = 7
						elif line[counter] in eol:
							contLinea = contLinea +1
							estado = 0
							break
						else:
							estado =6 
					elif estado ==7:
						if line[counter] == '/':
							openComment=False
							estado =0 
							counter=counter+1
							continue
						elif line[counter] == '*':
							counter = counter +1
							continue
						else:
							estado = 6
					elif estado ==8:
						if line[counter] == '=':
							estado =0
							generarToken('relOp','notEquals')
						else:
							estado = 0
							counter = counter -1
							generarToken('logOp','not')#revisar palabras reservadas
					elif estado ==9: 
						if line[counter] == '&':
							estado=0
							generarToken('logOp','and')
						else:
							estado = 0
							print('----------------------------')
							causaError = 'error: ' +word+ ' Expected: &&' + ' linea: ' + str(contLinea) + '\n'
							errorFile.write(causaError)
							continue
					elif estado ==10: 
						if line[counter] != "'":
							estado = 10
							word+=line[counter]
						else:
							estado=0
							word+=line[counter]
							generarToken('chain',word)
					elif estado==11:
						if line[counter] == '=':
							estado = 0
							generarToken('relOp','equals')
						else:
							estado =0
							counter = counter-1
							generarToken('asigOp','equal')
					counter = counter +1
					if(counter==len(line)) and (line==lines[len(lines)-1]):
						tokenCode = estadoCode(estado,word)
						if tokenCode == 'error':
							continue
						generarToken(tokenCode,word)	
		
		f.close()
		errorFile.close()
					
					
					
					
					

				


				


						


def main():
	global tokenFile
	parser = argparse.ArgumentParser(add_help=True)
	parser.add_argument('-f', type =str,nargs=1,help='Required filename you want to compile')
	args = parser.parse_args()
	tokenFile = file = open('t','w') 
	analizadorLexico(args.f[0])
	

	


if __name__== '__main__':
  	main()