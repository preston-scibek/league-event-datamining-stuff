hash_prefix_1 = "arcane-nlex-hub-2021"
url = "https://frontpage.na.leagueoflegends.com/en_US/channel/lol/home/event/arcane-nlex-hub-2021"
url2 = "https://frontpage.na.leagueoflegends.com/en_US/channel/lol/home/event/arcane-lexp-hub-2021"
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


def save_lines(file_name="lines_arcane.json"):
    res_json = get_lines(url=url)
    with open('lines_arcane.json', 'w', encoding='utf-8') as jfile:
        json.dump(res_json, jfile, indent=4, ensure_ascii=False)

def load_lines():
    with open('lines_arcane.json', 'r', encoding='utf-8') as jfile:
        return json.load(jfile)

import hashlib
import json
import sys


def dehash(inp, lines=None, hash_prefix=hash_prefix_1):
    if lines is None:
        lines = loaded_lines
    s = "{}{}.{}".format(17, hash_prefix.replace("-", "_"), inp)
    s = s.encode()
    r = hashlib.md5(s)
    d = r.hexdigest()
    return lines.get(d)


def comp():
    xxx1 = load_lines()
    with open('attempted_bf.json', 'r', encoding='utf-8') as jfile:
        xxx2 = json.load(jfile)

    missing = []
    for line in xxx1.values():
        if line not in xxx2.values():
            missing.append(line)
    return missing



def do_shit(n=10):
    loaded_lines = load_lines()
    res = {}
    champs = ['jayce', 'caitlyn', 'vi', 'jinx']
    for champ in champs:
        for record in range(1, n+1):
            for page in range(1, n+1):
                for section in range(1, n+1):
                    for text in range(1, n+1):
                        strr = "{}_collection.record_{}.page_{}.section_{}.text_{}".format(champ, record, page, section, text)
                        xxx = dehash(strr, lines=loaded_lines)
                        if xxx:
                            res[strr] = xxx
        for artifact in range(1, n+1):
            for text in range(1, n+1):
                strr = "{}_collection.artifact_{}.text_{}".format(champ, artifact, text)
                xxx = dehash(strr, lines=loaded_lines)
                if xxx:
                    res[strr] = xxx

        for k in range(1, n+1):
            strr = "{}_collection.nav.artifact_{}.title".format(champ, k)
            xxx = dehash(strr, lines=loaded_lines)
            if xxx:
                res[strr] = xxx
        
        suffixes = ["_collection_explore",  "_collection_unlocks_date", "_collection", "_collection_scroll", "_collection_unlocks"]
        for suffix in suffixes:
            strr = "global.ui.archive." + champ + suffix
            xxx = dehash(strr, lines=loaded_lines)
            if xxx:
                res[strr] = xxx
        strr = champ + "_collection.nav.top_title"
        xxx = dehash(strr, lines=loaded_lines)
        if xxx:
            res[strr] = xxx

        for k in range(1, 4):
            strr = "{}_collection.nav.record_{}.title".format(champ, k)
            xxx = dehash(strr, lines=loaded_lines)
            if xxx:
                res[strr] = xxx

    t1 = ['welcome', 'completion']
    t2 = ['title', 'intro', 'cta']
    for t in t1:
        for tt in t2: 
            strr = "global.ui.archive.{}.{}".format (t, tt)
            xxx = dehash(strr, lines=loaded_lines)
            if xxx:
                res[strr] = xxx
        for text in range(1, n+1):
            strr = "global.ui.archive.{}.text_{}".format(t, text)
            xxx = dehash(strr, lines=loaded_lines)
            if xxx:
                res[strr] = xxx

    globals_strs = [
        "global.ui.scroll_to_read",
        "global.ui.record_",
        "global.ui.info_cta",
        "global.ui.back_to_archive",
        "global.ui.close_record",
        "global.ui.next",
        "global.ui.previous",
        "global.ui.finish_close",
        "global.ui.section_of",
        "global.ui.move_left",
        "global.ui.archive.explore_archive",
        "global.ui.move_right",
        
        "global.ui.now_reading", 
        
        "tooltip.client_audio_off",
        "tooltip.audio_on",
        "tooltip.motion_on",
        "tooltip.motion_off",
        "tooltip.audio_off",
        
        "ui.learn_more",
        
        "intro.cta",
        
        "tutorial.title",
        "tutorial.text_1",
        "tutorial.text_2",
        "tutorial.footer",



    ]
    for strr in globals_strs:
        xxx = dehash(strr, lines=loaded_lines)
        if xxx:
            res[strr] = xxx


    for i in range(1, 4):
        for k in range(1, 4):
            strr = "global.ui.{}_of_{}".format(i, k)
            xxx = dehash(strr, lines=loaded_lines)
            if xxx:
                res[strr] = xxx
        strr = "global.ui.record_{}".format(i, k)
        xxx = dehash(strr, lines=loaded_lines)
        if xxx:
            res[strr] = xxx
    
    ll = get_lines(url=url2)


    strss = [
    "labels.owned",
    "nav.side_button.avatar_creator",
    "nav.side_button.event_website",
    "nav.side_button.rxa_website",
    "nav.side_button.watch_arcane",
    "preseason.content_title_1",
    "preseason.content_title_2",
    "season_end.title",
    "season_end.body",
    "season_end.content_title_1",
    "season_end.content_title_2",
    "ui.learn_more",
    "ui.learn_more",
    "nav.archives_button",

    ]
    for strr in strss:
        xxx = dehash(strr, lines=ll, hash_prefix="arcane-lexp-hub-2021")
        if xxx:
            res[strr] = xxx

    for champ in champs:
        strr = "collection." + champ + ".body"
        xxx = dehash(strr, lines=ll, hash_prefix="arcane-lexp-hub-2021")
        if xxx:
            res[strr] = xxx
        strr = "collection." + champ + ".cta"
        xxx = dehash(strr, lines=ll, hash_prefix="arcane-lexp-hub-2021")
        if xxx:
            res[strr] = xxx
    return res


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search Lines')

    parser.add_argument('-s', "--search", type=str, help='search keyword')
    parser.add_argument('-g', "--get_lines", type=bool, help='get_lines')


    args = parser.parse_args()
    if args.get_lines:
        save_lines()
    elif args.search:
        search_str = args.search if args.search != 'default' else 'jayce_collection.artifact_1.text_1'
        loaded_lines = load_lines()
        print(dehash(search_str, lines=loaded_lines))
    else:
        r = do_shit()
        
        missing = comp()
        for index, val in enumerate(missing):
            r["?"*(index+1)] = val
        with open('attempted_bf.json', 'w', encoding="utf-8") as jfile:
            json.dump(r, jfile, indent=4, ensure_ascii=False)


        


