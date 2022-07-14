import requests
import json, time
from bs4 import BeautifulSoup

from datamine import URL

def exists(url=URL):
    # load the page we need to get shit from
    res = requests.get(url)
    print(res.text)
    html = res.text
    return not "body></body>" in html


if __name__ == "__main__":
    while True:

        if exists():
            
            DISCORD_WEBHOOK = params['explore']['DISCORD_WEBHOOK'][1]
            data = {"content" :f"metagame site is filled"}
            res_post = requests.post(DISCORD_WEBHOOK, data=data)
            break
        else:
            print("Not up")
        time.sleep(60*5) #(5 min sleep)