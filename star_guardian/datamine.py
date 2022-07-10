import requests
import json
from bs4 import BeautifulSoup
import hashlib
import argparse

### GLOBALS 
# all examples are what was used in ../arcane
HASH_PREFIX = "star-guardian-hub-2022" # example is arcane-nlex-hub-2021
HASH_PREFIX_NUMBER = 17 
URL = "https://frontpage.na.leagueoflegends.com/en_US/channel/lol/home/event/star-guardian-hub-2022" # example is https://frontpage.na.leagueoflegends.com/en_US/channel/lol/home/event/arcane-nlex-hub-2021
URL = "https://frontpage.na.leagueoflegends.com/en_US/channel/lol/home/event/star-guardians-marketing-hub-2022#/"
HASHED_KEY_LINES_FILE = "hashed_lines_star_guardian.json" # example is 'lines_arcane.json'
DEHASHED_KEY_LINES_FILE = "dehashed_lines_star_guardian.json" # example is "attempted_bf.json"

def get_lines(url=URL):
    """ Get the Text Lines from the URL """
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

def save_lines(url=URL, file_name=HASHED_KEY_LINES_FILE):
    """ Save the lines to a file """
    res_json = get_lines(url=url)
    with open(file_name, 'w', encoding='utf-8') as jfile:
        json.dump(res_json, jfile, indent=4, ensure_ascii=False)

def load_lines(file_name=HASHED_KEY_LINES_FILE):
    """ Load lines from the file """
    with open(file_name, 'r', encoding='utf-8') as jfile:
        return json.load(jfile)

def dehash(inp, lines=None, hash_prefix=HASH_PREFIX, hash_prefix_number=HASH_PREFIX_NUMBER):
    """ Get the line corresponding to the unhashed key, in the hashmap"""
    if lines is None:
        lines = loaded_lines
    s = "{}{}.{}".format(hash_prefix_number, hash_prefix.replace("-", "_"), inp)
    s = s.encode()
    r = hashlib.md5(s)
    d = r.hexdigest()
    return lines.get(d)

def get_missing_keys(file_name=DEHASHED_KEY_LINES_FILE, p=False):
    """Compare the lines we've matched to their keys, to the lines we haven't"""
    xxx1 = load_lines()
    with open(file_name, 'r', encoding='utf-8') as jfile:
        xxx2 = json.load(jfile)

    missing = []
    for line in xxx1.values():
        if line not in xxx2.values():
            missing.append(line)
    return missing

def do_shit(n=40):
    """ Do all the stuff neseccary to link the keys to the lines"""
    loaded_lines = load_lines()
    res = {}
    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search Lines')

    parser.add_argument('-s', "--search", type=str, help='Search a key and see if we can we link it to al ine')
    parser.add_argument('-g', "--get_lines", type=bool, help='Pull down the latest set of lines')


    args = parser.parse_args()
    if args.get_lines:
        save_lines()
    elif args.search:
        search_str = args.search if args.search != 'default' else ''
        loaded_lines = load_lines()
        print(dehash(search_str, lines=loaded_lines))
    else:
        r = do_shit()

        # write to file
        with open(DEHASHED_KEY_LINES_FILE, 'w', encoding="utf-8") as jfile:
            json.dump(r, jfile, indent=4, ensure_ascii=False)

        # check missing
        missing = get_missing_keys(p=True)
        for index, val in enumerate(missing):
            r["?"*(index+1)] = val
            print(val)

        # write updated output to file
        with open(DEHASHED_KEY_LINES_FILE, 'w', encoding="utf-8") as jfile:
            json.dump(r, jfile, indent=4, ensure_ascii=False)


        


