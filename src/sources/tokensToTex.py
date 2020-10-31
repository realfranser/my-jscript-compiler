import json
# File Paths
sourceTokenFilePath = 'tokens.json'
with  open(sourceTokenFilePath) as sourceTokenFile:
		data = json.load(sourceTokenFile)
		for i in data['tokens']:
			for k in i['tokenList']:
				print(k['atribute'] + '	&<'+k['element']+', >'+'\\'+'\\')