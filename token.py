import json
import argparse
targetFile = 'tokens.json'



delim = [' ','\t']
eol = ['\n']
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
		word = ''
		estado = 0
		with open(file,'r') as f:
			lines = f.readlines()
			for line in lines:
				print('siguiente linea')
				counter =0
				while counter in range(len(line)):
					print(counter)
					print('siguiente caracter '+line[counter])
					if estado == 0:
						if line[counter] in delim:
							print('------delimitador-------')
						elif line[counter] in eol:
							print('/////final de linea//////')
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
							print('Errorororororororororo')
							#tratamiento de errores y elementos inesperados
						word=line[counter]
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
							estado = 6

						else:
							Error('barra sin asterico')	
					elif estado == 6:
						if line[counter] == '*':
							estado = 7

						else:
							estado =7 

					elif estado ==7:
						if line[counter] == '/':
							estado =0 

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
							Error('Necesita otro &')
					elif estado ==10: 
						if line[counter] != "'":
							estado = 10
							word+=line[counter]
						else:
							estado=0
							generarToken('chain',word)
							counter = counter-1
					elif estado==11:
						if line[counter] == '=':
							estado = 0
							generarToken('relOp','equals')
						else:
							estado =0
							counter = counter-1
							generarToken('asigOp','equal')
					counter = counter +1

					
					
					
					
					

				


				


						


def main():
	global tokenFile
	parser = argparse.ArgumentParser(add_help=True)
	parser.add_argument('-f', type =str,nargs=1,help='Required filename you want to compile')
	args = parser.parse_args()
	tokenFile = file = open('t','w') 
	analizadorLexico(args.f[0])
	

	


if __name__== '__main__':
  	main()