import requests
import json
from bs4 import BeautifulSoup

from datamine_marketing import URL

def get_versioned_asset_path(url=URL):
    # load the page we need to get shit from
    res = requests.get(url)

    html = res.text
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all('script')
    for script in scripts:
        # loop through thes cripts and delete dist.js
        if script.get('src') is  None and script.get('type') == "text/javascript":
            s = script.extract()
            if s is not None:
                x = str(s).split("versionedAssetPath: '")
                if len(x) > 1:
                    y = x[1].split("'")[0]  
                    return y


if __name__ == "__main__":
    asset_path = get_versioned_asset_path()
    print(f"Asset path = {asset_path}")
    with open("asset_path_marketing.json", "r+") as jfile:
        old_path = json.load(jfile)

    if asset_path != old_path.get('asset_path'):
        # do some shit

        with open("../../DiscordBot/.env.json", "r") as envfile:
             params = json.load(envfile)

        DISCORD_WEBHOOK = params['explore']['DISCORD_WEBHOOK'][1]
        data = {"content" :f"Asset path = {asset_path}"}
        res_post = requests.post(DISCORD_WEBHOOK, data=data)
        print(res_post.text)

    with open("asset_path_marketing.json", "w") as jfile:
            json.dump({"asset_path": asset_path}, jfile)
