import re, requests, os
import json
from track_asset_path import get_versioned_asset_path
from datamine import URL

import jsbeautifier
import subprocess
import concurrent.futures

def request_get(url):
    print(f"downloading asset for {url}")
    path = "assets/" + url.split("assets/")[1].split("?")[0]
    dir_path = "/".join(path.split("/")[0:-1])
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(path, 'wb') as f:
            for chunk in r:
                f.write(chunk)
        return True
    else:
        print(f"download failed for {url}")
        return False


def function():
    
    assets = []

    asset_path = get_versioned_asset_path(URL)
    #print(asset_path)
    asset_path = "https://lolstatic-a.akamaihd.net/frontpage/apps/prod/worlds-hub-2022/en_US/1d30b2f1028dfada7bf6d9bdd8edbae077301b5d/assets/"
    r = requests.get(f"{asset_path}dist.js")
    assert(r.status_code == 200)

    js = jsbeautifier.beautify(f"\n{r.text}")
    with open('dist.js', 'w') as jfile:
        jfile.writelines(js)

    for line in js.split("\n"):
        if "png" in line or "webm" in line or "jpg" in line:
            regex_str = r'^.*"((?:parsed-)?(?:images|video).*(?:png|jpg|webm).*)"[^:]?.*$'
            m = re.search(regex_str, line)
            if m and m.group(1):
                #print(f"{asset_path}{m.group(1)}")
                assets.append(f"{asset_path}{m.group(1)}")


    fails = []
    success = []
    
    print(assets)
    with open('temp.json', 'w') as jfile:
        json.dump(assets, jfile, indent=4)
    with concurrent.futures.ProcessPoolExecutor(max_workers=32) as executor:
        print('frog')
        for url, status in zip(assets, executor.map(request_get, assets)):
            if status:
                success.append(url)
            else:
                fails.append(url)

    with open("failed_downloads.json", "w+") as jfile:
        json.dump(fails, jfile, indent=4)
    with open("success_downloads.json", "w+") as jfile:
        json.dump(success, jfile, indent=4)

    total_assets = len(assets)
    print(f"Total Assets: {total_assets}\nFails: {len(fails)}\nSuccesses: {len(success)}")
    return len(assets), len(fails), len(success)

if __name__ == "__main__":
    function()