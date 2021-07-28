import requests
import hashlib
import json
import sys

from bs4 import BeautifulSoup

def dehash(inp, lines):
	s = "17sentinels_hub_2021.{}".format(inp)
	s = s.encode()
	r = hashlib.md5(s)
	d = r.hexdigest()
	return lines.get(d)

def dehash_asset(inp, n=1):
	s = "17{}".format(inp)
	s = s.encode()
	r = hashlib.md5(s)
	d = r.hexdigest()
	if n == 0:
		return d
	return dehash_asset(d, n=0)

def style_scenes(scenes=None, lines=None):
    if scenes is None:
        # load out scenes file
        with open("updated_scenes_styled.json", 'r') as jsonfile:
            scenes = json.load(jsonfile)

    
    for region in scenes:
        for scene in region:
            if scene.get('dialogueKey'):
                scene['dialogue'] = dehash(scene['dialogueKey'], lines=lines)
            if scene.get('descriptionKey'):
                scene['description'] = dehash(scene['descriptionKey'], lines=lines)
            responses = scene.get('responses')
            if responses:
                for response in responses:
                    if response.get('dialogueKey'):
                        response['dialogue'] = dehash(response['dialogueKey'], lines=lines)
    return scenes


def style_scenes_asset(scenes, host=None):
    for region in scenes:
        for scene in region:
            chars = [("char{}".format(x), scene.get("char{}".format(x))) for x in range(1,5) if scene.get("char{}".format(x)) is not None]
            speaker = scene.get('speakerKey', '')
            bg = scene.get('bg', '')

            for char in chars:
                scene["{}_image".format(char[0])] = '{}images/scenery/characters/{}.png'.format(host, dehash_asset(char[1]))

            scene['bg_image'] = '{}images/scenery/backgrounds/{}.jpg'.format(host, dehash_asset(bg, n=0))
            scene['speaker_image'] = '{}images/scenery/speakers/{}.png'.format(host, dehash_asset("-".join(speaker.split("_")[1::]), n=0))

    return scenes

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
    # download lines
    with open('scenes.json', 'r') as jfile:
        scenes = json.load(jfile)

    lines = get_lines()
    styled_scenes = style_scenes(scenes, lines)
    styled_scenes_assets = style_scenes_asset(styled_scenes, host=get_host())

    with open('datamine.json', 'w', encoding="utf-8") as jfile:
        json.dump(styled_scenes_assets, jfile, indent=4, ensure_ascii=False)