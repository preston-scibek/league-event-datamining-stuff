import json


with open("lines.json", "r") as jfile:
	lines = json.load(jfile)

res = {}

for line in lines:
	res[line[1]] = line[0]

with open("lines.json", "w") as jfile:
	json.dump(res, jfile, indent=4)
