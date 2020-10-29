
import json
import argparse
targetfile = 'tokens.json'
tokenFile = 't'



def tokenizer(file):

	with open(targetfile) as f,open(tokenFile,'w') as t:
		tokens = json.load(f)
		f.close
		with open(file,'r') as f:
			line = f.readline()
			for i in tokens['tokens']:
				for j in i['tokenList']:
					k = line.split(' ')[0]
					p = k[:-1]
					print(p)
					print(j['element'])
					if(j['element']==k):
						print('found')
						write='<' + i['tokenCode']+','+j['atribute']+'>'
						t.write(write)
						


def main():
	parser = argparse.ArgumentParser(add_help=True)
	parser.add_argument('-f', type =str,nargs=1,help='Required filename you want to compile')
	args = parser.parse_args()
	tokenizer(args.f[0])


if __name__== '__main__':
  	main()