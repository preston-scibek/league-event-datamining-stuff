import json

with open('lines.json', 'r') as l:
	lines = json.load(l)

with open('partial_revhash.json', 'r') as p:
	revhash = json.load(p)


res = {}

for k, v in revhash.items():
	res[k] = lines.get(v, 'val dne')

with open('lines_dehashed.json', 'w') as ld:
	json.dump(res, ld, indent=4)	