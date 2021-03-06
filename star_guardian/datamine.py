import requests
import json
from bs4 import BeautifulSoup
import hashlib
import argparse

### GLOBALS 
# all examples are what was used in ../arcane
HASH_PREFIX = "star-guardians-metagame-hub-2022" # example is arcane-nlex-hub-2021
HASH_PREFIX_NUMBER = 17 
URL = "https://frontpage.na.leagueoflegends.com/en_US/channel/lol/home/event/star-guardians-metagame-hub-2022#/"
HASH_PREFIX = URL.split("event/")[1].split("#")[0]

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
    #print(s)
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
    with open('scenes.json', 'r') as jfile:
        scenes = json.load(jfile)
    for index, scene_list in enumerate(scenes):
        for indexx, scene in enumerate(scene_list):
            speaker_id = scene.get('speakerId', None)
            if speaker_id:
                text = dehash(speaker_id, lines=loaded_lines)
                if text:
                    res[speaker_id] = text
            strr = scene['dialogueId']
            text = dehash(strr, lines=loaded_lines)
            if text:
                res[strr] = text
                scenes[index][indexx]['dialogue'] = text
            for indexxx, response in enumerate(scene.get('responses', [])):
                strr = response['dialogueId']
                text = dehash(strr, lines=loaded_lines)
                if text:
                    res[strr] = text
                    scenes[index][indexx]['responses'][indexxx]['dialogue'] = text
    with open('scenes.json', 'w') as jfile:
        json.dump(scenes, jfile, indent=4, ensure_ascii=False)

    spakers = [
        "student",
        "rell",
        "kaisa",
        "man",
        "woman",
        "taliyah",
        "ekko",
        "sebastien",
        "akali",
        "chiizu",
        "umi",
        "ina",
        "aru",
        "waku",
        "morgana",
        "unknown",
        "syndra",
        "zoe",
        "fiddlesticks",
        "prof_okamoto",
        "quinn",
        "valor",
        "narrator",
        "nilah",
        "dark_star",
        "sona",
        "noodle_bill",
        "security",
        "harp",
        "mall_mascot",
        "ahri",
        "miss_fortune",
        "dahlia",
        "dark_herald",
        "civilian",
        "shop_owner",
        "kid",
        "gamer",
        "hardcore_gamer",
        "skeeball_machine",
        "rakan",
        "past_ekko",
        "claggor",
        "kaisa_and_akali",
        "prof_ikari",
        "strange_machine",
        "school_bell",
        "prof_chuba",
        "students",
        "another_student",
        "a_third_student",
        "monster",
    ]

    champs = [
        "ahri",
        "morgana",
        "miss-fortune",
        "taliyah",
        "zoe",
        "akali",
        "sona",
        "nilah",
        "ekko",
        "quinn",
        "syndra",
        "rell",
        "kaisa"
    ]

    for i in range(0, 5):
        strr = f"guardian_story.act_{i}.title"
        text = dehash(strr, lines=loaded_lines)
        if text:
            res[strr] = text
        
        strr = f"guardian.level_{i}"
        text = dehash(strr, lines=loaded_lines)
        if text:
            res[strr] = text
        
        strr = f"guardian.points_progress_label.to_level_{i}"
        text = dehash(strr, lines=loaded_lines)
        if text:
            res[strr] = text

        strr = f"main_story.act_{i}.title"
        text = dehash(strr, lines=loaded_lines)
        if text:
            res[strr] = text
        
        for j in range(0, 5):
            strr = f"main_story.chapter{i}.act_{j}.subtitle"
            text = dehash(strr, lines=loaded_lines)
            if text:
                res[strr] = text

            strr = f"main_story.chapter{i}.act_{j}.story_locked"
            text = dehash(strr, lines=loaded_lines)
            if text:
                res[strr] = text


        strr = f"main_story.epilogue.act_{i}.subtitle"
        text = dehash(strr, lines=loaded_lines)
        if text:
            res[strr] = text

        strr = f"main_story.epilogue.act_{i}.story_locked"
        text = dehash(strr, lines=loaded_lines)
        if text:
            res[strr] = text
        
        for champ in champs:
            strr = f"guardian_story.{champ}{i}.subtitle"
            text = dehash(strr, lines=loaded_lines)
            if text:
                res[strr] = text

            strr = f"guardian.reward.level_{i}.{champ}"
            text = dehash(strr, lines=loaded_lines)
            if text:
                res[strr] = text
        
            strr = f"guardian.title.{champ}"
            text = dehash(strr, lines=loaded_lines)
            if text:
                res[strr] = text
    
    full_strs = [
        "tooltip.event_faq",
        "guardian_story.date_locked",
        "guardian_story.act.mission_locked",
        "main_story.act.mission_locked",
        "ui.learn_more",
        "ui.learn_more",
        "tutorial.step_of_total",
        "tutorial.step_0",
        "tutorial.step_1_title",
        "tutorial.step_1",
        "tutorial.step_2_title",
        "tutorial.step_2",
        "tutorial.step_3_title",
        "tutorial.step_3",
        "tutorial.step_4_title",
        "tutorial.step_4",
        "tutorial.step_5_title",
        "tutorial.step_5",
        "tutorial.step_6",
        "main_story.watch",
        "main_story.starlight",
        "main_story.watch",
        "nav.info",
        "nav.tutorial",
        "tutorial.skip_all",
        "info.section_1.heading",
        "info.section_1.subheading",
        "info.section_1.goal_1.description",
        "info.section_1.goal_1.award",
        "info.section_1.goal_2.description",
        "info.section_1.goal_2.award",
        "info.section_1.goal_3.description",
        "info.section_1.goal_3.award",
        "info.section_1.goal_4.description",
        "info.section_1.goal_4.award",
        "info.section_2.heading",
        "info.section_2.subheading",
        "info.section_2.goal_1.description",
        "info.section_2.goal_1.award",
        "info.section_2.goal_2.description",
        "info.section_2.goal_2.award",
        "info.section_2.goal_3.description",
        "info.section_2.goal_3.award",
        "info.section_2.goal_4.description",
        "info.section_2.goal_2.award",
        "info.section_2.goal_5.description",
        "info.section_2.goal_5.award",
        "nav.main_story",
        "nav.guardian_stories",
        "story.spacebar_to_continue",
        "tutorial.skip_all",
        "nav.countdown_day",
        "nav.countdown_days",
        "nav.countdown_hour",
        "nav.countdown_hours",
        "tooltip.motion_on",
        "tooltip.motion_off",
        "tooltip.sound_on",
        "tooltip.sound_off",
        "tooltip.client_audio_off"
    ]
    for strr in full_strs:
        text = dehash(strr, lines=loaded_lines)
        if text:
            res[strr] = text
    return res


def clean_up_scenes():
    from track_asset_path import get_versioned_asset_path
    asset_path = get_versioned_asset_path(URL)

    with open('scenes.json', 'r') as jfile:
        scenes = json.load(jfile)
    with open('groups.json', 'r') as jfile:
        groups = json.load(jfile)

    with open('speakers_reverse.json', 'r') as jfile:
        speakers_named = json.load(jfile)

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
                scenes[index][indexx]['bgPortraitR' + "Label"] = speakers_named.get(bgPortraitR, None)
            
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
                        scenes[index][indexx][portrait + "Label"] = speakers_named.get(fgportrait, None)
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
        from slim_scenes import slim_scenes_2
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
            #print(val)

        # write updated output to file
        with open(DEHASHED_KEY_LINES_FILE, 'w', encoding="utf-8") as jfile:
            json.dump(r, jfile, indent=4, ensure_ascii=False)


        


