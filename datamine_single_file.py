import requests
import hashlib
import json
import sys

from bs4 import BeautifulSoup
from collections import OrderedDict
from itertools import chain

def order_scenes(scenes):
    #The canon order is Demacia > Freljord > Noxus > Ionia > Targon > P/Z > Ixtal > Bilge > Shurima > Shadow Isles

    order = ['demacia', 'freljord', 'noxus', 'ionia', 'targon', 'piltover', 'ixtal', 'bilgewater', 'shurima', 'shadow', 'induction', 'key']
    new_scenes = OrderedDict()
    for item in order:
        new_scenes[item] = []

    for chapter in scenes:
        dk = chapter[0].get('dialogueKey', chapter[0].get('nameKey'))
        loc = dk.split("scene")[0].split("_")[-2]
        chapter = (loc, chapter)
        region = [x for x in order if x in dk][0]


        new_scenes[region].append(chapter)
        new_scenes[region] = sorted(new_scenes[region], key=lambda x: x[0])

    for key, value in new_scenes.items():
        new_scenes[key] = list(chain.from_iterable([x[1] for x in value]))
    return new_scenes

def dehash(inp, lines):
    """Dehash inp and return the dialogue from lines that corresponds"""
    s = "17sentinels_hub_2021.{}".format(inp)
    s = s.encode()
    r = hashlib.md5(s)
    d = r.hexdigest()
    return lines.get(d)


def hash_asset(inp, n=1):
    """Hash inp n+1 times"""
    s = "17{}".format(inp)
    s = s.encode()
    r = hashlib.md5(s)
    d = r.hexdigest()
    if n == 0:
        return d
    return hash_asset(d, n=0)

def style_scenes(scenes=None, lines=None):
    """Append the dialogue options to each scene"""
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
    """Append the assets to each scene"""
    for region in scenes:
        for scene in region:
            chars = [("char{}".format(x), scene.get("char{}".format(x))) for x in range(1,5) if scene.get("char{}".format(x)) is not None]
            speaker = scene.get('speakerKey', '')
            bg = scene.get('bg', '')

            for char in chars:
                scene["{}_image".format(char[0])] = '{}images/scenery/characters/{}.png'.format(host, hash_asset(char[1]))

            scene['bg_image'] = '{}images/scenery/backgrounds/{}.jpg'.format(host, hash_asset(bg, n=0))

            hardcodeds = {
                    "solari-fanatic-1": "solari-soldier",
                    "solari-fanatic-2": "solari-soldier",
                    "viegos-voice": "viego",
                    "viego-s-voice": "viego",
                    "lunari-commoners-1-2": "lunari-commoner-1",
                    "lunari-commoners-1---2": "lunari-commoner-1",
            }

            speaker = hardcodeds.get("-".join(speaker.split("_")[1::]), "-".join(speaker.split("_")[1::]))
            scene['speaker_image'] = '{}images/scenery/speakers/{}.png'.format(host, hash_asset(speaker, n=0))

    return scenes


def get_lines():
    """Get the up to date lines"""
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
    """Get the up to date asset path"""
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

    ordered_scenes = order_scenes(styled_scenes_assets)
    with open('datamine.json', 'w', encoding="utf-8") as jfile:
        json.dump(ordered_scenes, jfile, indent=4, ensure_ascii=False)