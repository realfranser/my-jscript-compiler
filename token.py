import json
import argparse
targetfile = 'tokens.json'
tokenFile = 't'


delim = [' ','\t']
eol = ['\n']
def generarToken(tokenCode,atribute):
	file = open(tokenFile,W)
	token = '<' + tokencode + ',' + atribute + '>'
	file.write(token)

def analizadorLexico():
	with open(targetfile) as f,open(tokenFile,'w') as t:
		tokens = json.load(f)
		f.close
		word = ''
		estado = 0
		with open(file,'r') as f:
			line = f.readline()
			while line:
				for	i in line:
					if estado == 0:
						if i in delim:
							continue
						elif i in eol:
							break
						elif i.isdigit:
							estado = 1
						elif i.isalpha:
        				
							 estado=2
						elif i=='+':
							estado = 3
						elif i=='-':
							estado=4
						elif i == '/':
							estado = 5
						elif i == '(':
							generarToken(separator,openPar)
						elif i == ')':
							generarToken(separator,closePar)
						elif i == '{':
							generarToken(separator,openBraq)
						elif i == '}':
							generarToken(separator,closeBraq)	 
						elif i == '!':
							estado = 8
						elif i == '&':
							estado = 9
						elif i=="'":
							estado = 10
						elif i=='=':
							estado = 11	
						elif i==';':
							generarToken('separator','semicolon')
						elif i == ',':
							generarToken(separator,colon)
						else:
							print('hola')
							#tratamiento de errores y elementos inesperados
						word=i
					elif estado ==	1:
						if i.isdigit:
							estado=1
							word+=i
							continue
						else:
							estado=0
							generarToken(wholeConst,numero)
							i--
							continue
					elif estado ==	 2:
						if i.isdigit() or i.isalpha or i =='_':
							estado=2
							word+=i
							continue
						else:
							estado=0
							generarToken(ID,posicionTablaSimbolos)
							i--
							continue
				    elif estado ==3:
						if i == '+':
							estado = 0
							generarToken(autoIncOp,autoinc)
						else:
							estado =0
							generarToken(aritOp,plus)
							i--
							continue
				    elif estado == 4:
						if i == '-':
							estado = 0
							generarToken(autoDecOp,autodec)
						else:
							estado =0
							generarToken(aritOp,minus)
							i--
							continue
					elif estado ==5:
						if i =='*':
							estado = 6
							continue
						else:
							Error('barra sin asterico')	
					elif estado == 6:
						if i == '*':
							estado = 7
							continue
						else:
							estado =7 
							continue
					elif estado ==7:
						if i == '/':
							estado =0 
							continue
						elif i == '*':
							continue
						else:
							estado = 6
							continue
					elif estado ==8:
						if i == '=':
							estado =0
							generarToken(relOp,notEquals)
							continue
						else:
							estado = 0
							generarToken(logOp,not)#revisar palabras reservadas
							continue
					elif estado ==9: 
						if i == '&':
							estado=0
							generarToken(logOp,and)
							break
						else:
							Error('Necesita otro &')
					elif estado ==10: 
						if i != "'":
							estado = 10
							word+=i
						else:
							estado=0
							generarToken(chain,posicionTablaSimbolos)
							continue

					elif estado==11:
						if i == '=':
							estado = 0
							generarToken(relOp,equals)
						else:
							estado =0
							i--
							generarToken(asigOp,equal)
							continue
					
					
					
					
					

				


				


						


def main():
	parser = argparse.ArgumentParser(add_help=True)
	parser.add_argument('-f', type =str,nargs=1,help='Required filename you want to compile')
	args = parser.parse_args()
	analizadorLexico(args.f[0])


if __name__== '__main__':
  	main()