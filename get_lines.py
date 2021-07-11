import requests
import json
from bs4 import BeautifulSoup

res = requests.get("https://frontpage.na.leagueoflegends.com/en_US/channel/lol/home/event/sentinels-hub-2021#/")

html = res.text
soup = BeautifulSoup(html, "html.parser")
scripts = soup.find_all('script', attrs={"type": "text/i18n"})
res_json = {}
for script in scripts:
	text = script.text
	_id = script.get('id')
	res_json[_id] = text

with open('lines.json', 'w') as jfile:
	json.dump(res_json, jfile, indent=4)