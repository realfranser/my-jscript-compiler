import json
import argparse
targetFile = 'tokens.json'



delim = [' ','\t']
eol = ['\n']
openComment = False


		
									
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
		

def AnalizadorLexico(lines,state,lexema):
		print(lines[0])
		while lines != None:
			AnalizadorLexico(lines[-1:],state,lexema)
					
					

				


				


						


def main():
	global tokenFile
	parser = argparse.ArgumentParser(add_help=True)
	parser.add_argument('-f', type =str,nargs=1,help='Required filename you want to compile')
	args = parser.parse_args()
	tokenFile = open('t','w')
	with open(args.f[0],'r') as f, open ('error.txt','w') as errorFile:
		analizadorLexico(f.readLines(),0,'')
	

	


if __name__== '__main__':
  	main()