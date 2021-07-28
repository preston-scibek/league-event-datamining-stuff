import hashlib
import json
import sys

with open('lines.json', 'r') as l:
	loaded_lines = json.load(l)


def dehash(inp, lines=None):
	if lines is None:
		lines = loaded_lines
	s = "17sentinels_hub_2021.{}".format(inp)
	s = s.encode()
	r = hashlib.md5(s)
	d = r.hexdigest()
	return lines.get(d)


def hash_asset(inp, n=1):
	s = "17{}".format(inp)
	s = s.encode()
	r = hashlib.md5(s)
	d = r.hexdigest()
	if n == 0:
		return d
	return dehash_asset(d, n=0)

if __name__ == "__main__":
	item = sys.argv[1]
	print(dehash(item))