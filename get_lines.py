import requests
import json
from bs4 import BeautifulSoup


def get_lines():
    res = requests.get("https://frontpage.na.leagueoflegends.com/en_US/channel/lol/home/event/sentinels-hub-2021#/")

    html = res.text
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all('script', attrs={"type": "text/i18n"})
    res_json = {}
    for script in scripts:
        text = script.string
        _id = script.get('id')
        res_json[_id] = text
    return res_json

def get_host():
    res = requests.get("https://frontpage.na.leagueoflegends.com/en_US/channel/lol/home/event/sentinels-hub-2021#/")
    html = res.text
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all('script')
    for script in scripts:
        # loop through thes cripts and delete dist.js
        if script.get('src') is not None and "dist.js" in script.get('src'):
            return script.get('src').split('dist.js')[0]
    return 'nothing found'

if __name__ == "__main__":
    res_json = get_lines()
    with open('lines.json', 'w', encoding='utf-8') as jfile:
        json.dump(res_json, jfile, indent=4, ensure_ascii=False)