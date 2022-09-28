import requests
import json
from bs4 import BeautifulSoup
import hashlib
import argparse

### GLOBALS 
# all examples are what was used in ../arcane
HASH_PREFIX = "" # example is arcane-nlex-hub-2021
HASH_PREFIX_NUMBER = 17 
URL = ""
HASH_PREFIX = URL.split("event/")[1].split("#")[0]
FILE_NAME = "" # name to add to relevant files

HASHED_KEY_LINES_FILE = "hashed_lines_{FILE_NAME}.json" # example is 'lines_arcane.json'
DEHASHED_KEY_LINES_FILE = "dehashed_lines_{FILE_NAME}.json" # example is "attempted_bf.json"

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
    """ Do all the stuff necessary to link the keys to the lines"""
    loaded_lines = load_lines()
    res = {}
    with open('scenes.json', 'r') as jfile:
        scenes = json.load(jfile)
    return res


def clean_up_scenes():
    from track_asset_path import get_versioned_asset_path
    asset_path = get_versioned_asset_path(URL)

    with open('scenes.json', 'r') as jfile:
        scenes = json.load(jfile)
    with open('groups.json', 'r') as jfile:
        groups = json.load(jfile)

    #with open('speakers_reverse.json', 'r') as jfile:
    #    speakers_named = json.load(jfile)

    for index, scene_list in enumerate(scenes):
        for indexx, scene in enumerate(scene_list):
            bg = scene['bg']
            if 'parsed' not in bg:
                scenes[index][indexx]['bg' + "URL"] = f"{asset_path}parsed-images/obf/bgs/{bg}.jpg"
            
            speakerIcon = scene.get('speakerIcon', None)
            if speakerIcon and 'parsed' not in speakerIcon:
                scenes[index][indexx]['speakerIcon' + "URL"] = f"{asset_path}parsed-images/obf/speaker-icons/{speakerIcon}.png"

            bgPortraitR = scene.get('bgPortraitR', None)
            if bgPortraitR and 'parsed' not in bgPortraitR:
                scenes[index][indexx]['bgPortraitR' + "URL"] = f"{asset_path}parsed-images/obf/bg-portraits/{bgPortraitR}.png"
                #scenes[index][indexx]['bgPortraitR' + "Label"] = speakers_named.get(bgPortraitR, None)
            
            bgPortraitL = scene.get('bgPortraitL', None)
            if bgPortraitL and 'parsed' not in bgPortraitL:
                scenes[index][indexx]['bgPortraitL' + "URL"] = f"{asset_path}parsed-images/obf/bg-portraits/{bgPortraitL}.png"

            for i in range(1, 4):
                # group fails for now , its a collection of the other portraits
                portraits = [f'fgPortraitR{i}', f"fgPortraitL{i}"]#, f'fgPortraitR{i}Group', f"fgPortraitL{i}Group"]
                for portrait in portraits:
                    fgportrait = scene.get(portrait, None)
                    if fgportrait and 'parsed' not in fgportrait:
                        scenes[index][indexx][portrait + "URL"] = f"{asset_path}parsed-images/obf/fg-portraits/{fgportrait}.png"
                        #scenes[index][indexx][portrait + "Label"] = speakers_named.get(fgportrait, None)
                for portrait in [f'fgPortraitR{i}Group', f"fgPortraitL{i}Group"]:
                    group = scene.get(portrait, None)
                    if group and isinstance(group, str):
                        image_list = []
                        for image_id in groups[group]:
                            image_list.append(f"{asset_path}parsed-images/obf/fg-portraits/{image_id}.png")
                        scenes[index][indexx][portrait + "URLS"] = image_list
            scenes[index][indexx] = {k : v for k, v in sorted(scenes[index][indexx].items(), key=lambda q: q[0])}
            
    with open('scenes.json', 'w') as jfile:
        json.dump(scenes, jfile, indent=4, ensure_ascii=False)


def slim_scenes_2(scenes):
	res = {}
	for sublist in scenes:
		for subdict in sublist:
			re_str = r"^(chapter|epilogue|tutorial)_(?:(\d+)_)?(?:act_(\d+)_)?scene_([a-d0-9]+)_(\d+)?_?text$"
			re_str2 = r"^([a-z]+)_(\d+)_scene_([a-d0-9]+)_(\d+)?_?text$"
			re_compiled = re.compile(re_str)
			re_compiled2 = re.compile(re_str2)
			matches = re_compiled.search(subdict.get('dialogueId'))
			matches2 = re_compiled2.search(subdict.get('dialogueId'))
			if matches:
				type_ = matches.group(1)
				chapter =matches.group(2)
				act = matches.group(3)
				scene = matches.group(4)
				choice = matches.group(5)
			elif matches2:
				type_ = 'champ'
				chapter = matches2.group(1)
				act = matches2.group(2)
				scene = matches2.group(3)
				choice = matches2.group(4)
			
			chapter = f"{type_.title()} {chapter if chapter else ''}".strip() if type_ != 'champ' else chapter
			act = f"Act {act}"
			res[chapter] = res.get(chapter, {})
			res[chapter][act] = res[chapter].get(act, {})
			res[chapter][act][subdict['sceneId']] = res[chapter][act].get(subdict['sceneId'], {
				'speaker': subdict['speakerId'],
				'dialogueId': subdict['dialogueId'],
				'response': subdict.get('responses', []),
				'dialogue': subdict.get('dialogue', 'Dialogue is not Available Yet'),
				'next_scene_id': subdict.get('nextSceneId', None),
				'bg_url': subdict.get('bgURL', None)
			})
	for chapter_key, chapter_value in res.items():
		for act_key, act_value in chapter_value.items():
			res[chapter_key][act_key] = {k : v for k, v in sorted(act_value.items(), key=lambda q: int(q[0]) if q[0].isdigit() else int(q[0].split("_")[0][0:-1]))}
		res[chapter_key] = {k : v for k, v in sorted(chapter_value.items(), key=lambda q: q[0].split(" ")[1] if len(q[0].split(" ")) > 1 else q[0])}
	res_dict = {k : v for k, v in sorted(res.items(), key=lambda q: f"ZZZ{q[0]}" if ('Chapter' not in q[0] and 'Epi' not in q[0] and "Tut" not in q[0]) else f"BBB{q[0]}" if "Tut" not in q[0] else f"AAA{q[0]}")}
	
	
	res_text = ""
	for chapter_name, acts in res_dict.items():
		for act_name, scenes in acts.items():
			res_text += (f"{'-'*10}\n{chapter_name.title()} {act_name if 'None' not in act_name else ''}").strip() + "\n"
			prior = None
			prior_bg = None
			for scene_id, lines in scenes.items():
				if not scene_id.isdigit():
					continue
				if prior is not None:
					assert(scene_id == prior)
				if prior_bg != lines['bg_url']:
					res_text += f"{'-'*10}\n"
				prior = lines['next_scene_id']
				prior_bg = lines['bg_url']

				res_text += (f"{lines['speaker']}: {lines['dialogue']}\n")

				if len(lines.get('response')) > 0:
					i = 1
					for index, response in enumerate(lines.get('response')):
						res_text += (f"\t[Option {index + 1}] {response.get('dialogue', 'unknown')}\n")
						i += 1
						box = response
						# follow the option until we break outta the tree
						box['next_scene_id'] = box['nextSceneId']
						while box['next_scene_id'] is not None and not box['next_scene_id'].isdigit():
							box = scenes[box['next_scene_id']]
							res_text += (f"\t{box['speaker']}: {box['dialogue']}\n")

	return res_dict, res_text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search Lines')

    parser.add_argument('-s', "--search", type=str, help='Search a key and see if we can we link it to al ine')
    parser.add_argument('-g', "--get_lines", type=bool, help='Pull down the latest set of lines')
    parser.add_argument("-S", "--clean_up_scenes", type=bool, help="Clean up scenes with various fixes")
    parser.add_argument("-L", "--slim_scenes", type=bool, help="Slim the scenes to a single text reading")

    args = parser.parse_args()
    if args.get_lines:
        save_lines()
    elif args.search:
        search_str = args.search if args.search != 'default' else ''
        loaded_lines = load_lines()
        print(dehash(search_str, lines=loaded_lines))
    elif args.clean_up_scenes:
        clean_up_scenes()
    elif args.slim_scenes:
        with open('scenes.json', 'r') as jfile:
            scenes = json.load(jfile)

        new_scenes, res = slim_scenes_2(scenes)

        with open('scenes_slim.json', 'w', encoding="utf-8") as jfile:
            json.dump(new_scenes, jfile, indent=4, ensure_ascii=False)

        with open('scenes_slim.txt', 'w+') as slimfile:
            slimfile.write(res)
    else:
        r = do_shit()

        # write to file
        with open(DEHASHED_KEY_LINES_FILE, 'w', encoding="utf-8") as jfile:
            json.dump(r, jfile, indent=4, ensure_ascii=False)

        # check missing
        missing = get_missing_keys(p=True)
        for index, val in enumerate(missing):
            r[f"?*({index+1})"] = val

        # write updated output to file
        with open(DEHASHED_KEY_LINES_FILE, 'w', encoding="utf-8") as jfile:
            json.dump(r, jfile, indent=4, ensure_ascii=False)


        


