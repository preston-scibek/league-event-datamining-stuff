import requests
import json
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

HOST = "generalbloodsword.com/"

def execute_selenium(driver_path='./chromedriver.exe', headless=True):
    # enable browser logging
    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = {'browser': 'ALL'}
    driver = webdriver.Chrome(desired_capabilities=d)

    # load our custom page
    driver.get('file:///C:/Dev/ruination_event_stuff/injected_index.html#/')
    
    # load out scenes file
    with open("scenes.json") as jsonfile:
        scenes = json.load(jsonfile)
    # loop through the arrays
    for region in scenes:
        for scene in region:
            
            # execute the dehashing function
            # log the output
            # credit u/LordredstoneNr1 for the idea to pin this function in the dist file and to then log the output
            driver.execute_script("console.log(window.dehashFunction(\"{}\"));".format(scene.get('dialogueKey')))
            # grab the last browser output which is our dialogue
            dialogue = driver.get_log('browser')[-1]
            # get the actuall log mesasage then strip out irrelevant shit
            scene['dialogue'] = " ".join(dialogue['message'].split(" ")[2::]).strip("\"")

            responses = scene.get('responses')
            if responses:
                for response in responses:
                    # execute the dehashing function
                    # log the output
                    # credit u/LordredstoneNr1 for the idea to pin this function in the dist file and to then log the output
                    driver.execute_script("console.log(window.dehashFunction(\"{}\"));".format(response.get('dialogueKey')))
                    # grab the last browser output which is our dialogue
                    dialogue = driver.get_log('browser')[-1]
                    # get the actuall log mesasage then strip out irrelevant shit
                    response['dialogue'] = " ".join(dialogue['message'].split(" ")[2::]).strip("\"")

        
    miscs = ['journal.event_begin.copy']
    misc_entries = {}
    for misc in miscs:
        driver.execute_script("console.log(window.dehashFunction(\"{}\"));".format(misc))
        # grab the last browser output which is our dialogue
        dialogue = driver.get_log('browser')[-1]
        # get the actuall log mesasage then strip out irrelevant shit
        misc_entries[misc] = " ".join(dialogue['message'].split(" ")[2::]).strip("\"")


    regions = ['demacia', 'noxus_a', 'noxus_b', 
        'freljord_a', 'freljord_b', 'ionia_a', 'ionia_b', 'targon_a', 'targon_b', 
        'shurima', 'piltover_zaun', 'bilgewater_a', 'bilgewater_b', 'ixtal_a', 'ixtal_b',
        'shadow_isles']
    things = ["journal.{}.copy", "journal.{}.date"]
    region_entries = []
    for region in regions:
        temp_dict = {}
        for item in things:
            copy = item.format(region)
            driver.execute_script("console.log(window.dehashFunction(\"{}\"));".format(copy))
            # grab the last browser output which is our dialogue
            dialogue = driver.get_log('browser')[-1]
            # get the actuall log mesasage then strip out irrelevant shit
            temp_dict[copy] = " ".join(dialogue['message'].split(" ")[2::]).strip("\"")
        region_entries.append(temp_dict)


    keys = [
        "journal.week_{}.date",
        "journal.week_{}.copy",
        "journal.week_{}.unlock_note",
        "journal.week_{}.upgrade_name",
        "journal.week_{}.upgrade_description",
        "journal.key_upgrade{}.date",
        "journal.key_upgrade{}.copy",
        "journal.key_upgrade{}.unlock_note",
        "journal.key_upgrade{}.upgrade_name",
        "journal.key_upgrade{}.upgrade_description"
    ]
    journal_entries = []
    for i in range(1, 5):
        temp_dict = {}
        for item in keys:
            copy = item.format(i)
            driver.execute_script("console.log(window.dehashFunction(\"{}\"));".format(copy))
            # grab the last browser output which is our dialogue
            dialogue = driver.get_log('browser')[-1]
            # get the actuall log mesasage then strip out irrelevant shit
            temp_dict[copy] = " ".join(dialogue['message'].split(" ")[2::]).strip("\"")
            temp_dict['journal-poster'] = '{}assets/chapter-posters/journal-poster-week-{}.png'.format(HOST, i)
            temp_dict['poster'] = '{}assets/chapter-posters/week-{}.jpg'.format(HOST, i)
        journal_entries.append(temp_dict)

    # bbBi var f , for the rest of these, i cba to add all the cases right now
    champs = ['olaf', 'graves', 'gwen', 'lucian', 'senna', 'riven', 'irelia', 'akshan', 'pyke', 'vayne', 'diana']
    sentinels = ['sentinel_{}.profile.subtitle', 'sentinel_{}.profile.v1.mechanics_summary', 'sentinel_{}.profile.v1.mechanics_details']
    champ_entries = []
    for champ in champs:
        temp_dict = {}
        for item in sentinels:
            copy = item.format(champ)
            driver.execute_script("console.log(window.dehashFunction(\"{}\"));".format(copy))
            # grab the last browser output which is our dialogue
            dialogue = driver.get_log('browser')[-1]
            # get the actuall log mesasage then strip out irrelevant shit
            temp_dict[copy] = " ".join(dialogue['message'].split(" ")[2::]).strip("\"")
        champ_entries.append(temp_dict)

    driver.quit()

    return scenes, journal_entries, champ_entries, region_entries, misc_entries

def style_scenes(scenes):
    host = HOST
    
    for region in scenes:
        for scene in region:
            chars = [("char{}".format(x), scene.get("char{}".format(x))) for x in range(1,5) if scene.get("char{}".format(x)) is not None]
            speaker = scene.get('speakerKey', '')
            bg = scene.get('bg', '')

            for char in chars:
                scene["{}_image".format(char[0])] = '{}assets/scenery/characters/{}.png'.format(host, char[1])

            scene['bg_image'] = '{}assets/scenery/backgrounds/{}.jpg'.format(host, bg)
            scene['speaker_image'] = '{}assets/scenery/speakers/{}.png'.format(host, "_".join(speaker.split("_")[1::]))

    return scenes


def hijack_page():
    # load the page we need to get shit from
    res = requests.get("https://frontpage.na.leagueoflegends.com/en_US/channel/lol/home/event/sentinels-hub-2021#/")

    html = res.text
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all('script')
    for script in scripts:
        # loop through thes cripts and delete dist.js
        if script.get('source') is not None and "dist.js" in script.get('source'):
            s.extract()
    # load our modified dist.js
    with open('dist-modified.js', 'r', encoding="utf-8") as jfile:
        injected_script = jfile.read()

    # inject that into the html 
    inject_tag = soup.new_tag('script', id='injected')
    inject_tag.string = injected_script
    soup.head.append(inject_tag)

    # save that page to be utilized with selenium
    with open('injected_index.html', 'w', encoding="utf-8") as hfile:
        hfile.write(str(soup))

if __name__ == "__main__":
    hijack_page()
    new_scenes, journal_entries, champ_entries, region_entries, misc_entries = execute_selenium()
    
    # write the output to the file
    new_scenes = style_scenes(new_scenes)
    with open('update_scenes_styled.json', 'w') as jfile:
    	json.dump(new_scenes, jfile, indent=4)
    # write the output to the file
    with open('journal.json', 'w') as jfile:
        json.dump(journal_entries + region_entries + [misc_entries], jfile, indent=4)
    # write the output to the file
    with open('champ_entries.json', 'w') as jfile:
        json.dump(champ_entries, jfile, indent=4)
