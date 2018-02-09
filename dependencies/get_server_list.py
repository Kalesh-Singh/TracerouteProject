import json

data = json.load(open('dependencies/data.json'))

with open('dependencies/server_list.txt', 'w') as server_list:
	for university in data:
		server = university["web_pages"][0][:-1].split('//')[-1]
		server_list.write(server + '\n')

				
