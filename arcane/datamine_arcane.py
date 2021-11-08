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


def comp():
    xxx1 = load_lines()
    with open('attempted_bf.json', 'r', encoding='utf-8') as jfile:
        xxx2 = json.load(jfile)

    for line in xxx1.values():
        if line not in xxx2.values():
            print(line)



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
        strr = "global.ui.archive." + champ + "_collection_explore"
        xxx = dehash(strr, lines=loaded_lines)
        if xxx:
            res[strr] = xxx

        strr = "global.ui.archive." + champ + "_collection_unlocks_date"
        xxx = dehash(strr, lines=loaded_lines)
        if xxx:
            res[strr] = xxx

        strr = "global.ui.archive." + champ + "_collection"
        xxx = dehash(strr, lines=loaded_lines)
        if xxx:
            res[strr] = xxx

        strr = "global.ui.archive." + champ + "_collection_scroll"
        xxx = dehash(strr, lines=loaded_lines)
        if xxx:
            res[strr] = xxx

                



    t1 = ['welcome', 'completion']
    t2 = ['title', 'intro', 'cta']
    for t in t1:
        for tt in t2: 
            strr = "global.ui.archive.{}.{}".format(t, tt)
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
        #"global.ui." + e.hoveredRecord + "_of_",
        
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
        "tooltip.client_audio_off",
        "tooltip.audio_on",
        "tooltip.motion_on",
        "tooltip.motion_off",
        "tooltip.audio_off",
    ]
    for strr in globals_strs:
        xxx = dehash(strr, lines=loaded_lines)
        if xxx:
            res[strr] = xxx

    return res


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search Lines')

    parser.add_argument('-s', "--search", type=str, help='search keyword')

    args = parser.parse_args()
    if args.search:
        search_str = args.search if args.search != 'default' else 'jayce_collection.artifact_1.text_1'
        loaded_lines = load_lines()
        print(dehash(search_str, lines=loaded_lines))
    else:
        r = do_shit()
        with open('attempted_bf.json', 'w', encoding="utf-8") as jfile:
            json.dump(r, jfile, indent=4, ensure_ascii=False)


    #comp()
        


