import hashlib
import json
import sys

with open('lines.json', 'r') as l:
	lines = json.load(l)


def dehash(inp):
	s = "17sentinels_hub_2021.{}".format(inp)
	s = s.encode()
	r = hashlib.md5(s)
	d = r.hexdigest()
	return lines.get(d)


if __name__ == "__main__":
	item = sys.argv[1]
	print(dehash(item))