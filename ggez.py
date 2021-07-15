import requests
import json
from bs4 import BeautifulSoup


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def execute_selenium(driver_path='./chromedriver.exe', headless=True):
    # enable browser logging
    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = {'browser': 'ALL'}
    driver = webdriver.Chrome(desired_capabilities=d)
    # load some site

    driver.get('file:///C:/Dev/ruination_event_stuff/injected_index.html#/')
    # print messages
    
    driver.execute_script("console.log(\"sup bitches\");")

    with open("scenes.json") as jsonfile:
        scenes = json.load(jsonfile)


    for region in scenes:
        for scene in region:
            driver.execute_script("console.log(window.dehashFunction(\"{}\"));".format(scene.get('dialogueKey')))
            dialogue = driver.get_log('browser')[-1]
            scene['dialogue'] = " ".join(dialogue['message'].split(" ")[2::]).strip("\"")

    driver.quit()

    return scenes


def hijack_page():
    res = requests.get("https://frontpage.na.leagueoflegends.com/en_US/channel/lol/home/event/sentinels-hub-2021#/")

    html = res.text
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all('script')
    for script in scripts:
        if script.get('source') is not None and "dist.js" in script.get('source'):
            s.extract()
    
    with open('dist-modified.js', 'r', encoding="utf-8") as jfile:
        injected_script = jfile.read()

    inject_tag = soup.new_tag('script', id='injected')
    inject_tag.string = injected_script
    soup.head.append(inject_tag)

    with open('injected_index.html', 'w', encoding="utf-8") as hfile:
        hfile.write(str(soup))

if __name__ == "__main__":
    hijack_page()
    new_scenes = execute_selenium()
    print(new_scenes[0][0])
    with open('updated_scenes.json', 'w') as jfile:
    	json.dump(new_scenes, jfile, indent=4)