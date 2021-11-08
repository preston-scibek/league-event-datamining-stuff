hash_prefix_1 = "arcane-nlex-hub-2021"
url = "https://frontpage.na.leagueoflegends.com/en_US/channel/lol/home/event/arcane-nlex-hub-2021"

import requests
import json
from bs4 import BeautifulSoup


def get_lines(url=""):
    res = requests.get(url)

    html = res.text
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all('script', attrs={"type": "text/i18n"})
    res_json = {}
    for script in scripts:
        text = script.string
        _id = script.get('id')
        res_json[_id] = text
    return res_json


def save_lines():
	res_json = get_lines(url="")
	with open('lines_arcane.json', 'w', encoding='utf-8') as jfile:
		json.dump(res_json, jfile, indent=4, ensure_ascii=False)

def load_lines():
	with open('lines_arcane.json', 'r', encoding='utf-8') as jfile:
		return json.load(jfile)

import hashlib
import json
import sys


def dehash(inp, lines=None):
	if lines is None:
		lines = loaded_lines
	s = "{}{}.{}".format(17, hash_prefix_1.replace("-", "_"), inp)
	s = s.encode()
	r = hashlib.md5(s)
	d = r.hexdigest()
	return lines.get(d)


import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Search Lines')

	parser.add_argument('-s', "--search", type=str, help='search keyword')

	args = parser.parse_args()

	search_str = args.search if args.search is not None else 'jayce_collection.artifact_1.text_1'


	loaded_lines = load_lines()
	print(dehash(search_str, lines=loaded_lines))

