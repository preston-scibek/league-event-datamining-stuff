import re, requests, os

from track_asset_path import do_shit
assets = []

asset_path = do_shit("https://frontpage.na.leagueoflegends.com/en_US/channel/lol/home/event/arcane-nlex-hub-2021#/intro")

with open('dist.js', 'r') as jfile:
    for line in jfile.readlines():
        if "png" in line or "webm" in line or "jpg" in line:
            regex_str = r'^.*"((?:images|video).*(?:png|jpg|webm).*)"[^:].*$'
            m = re.search(regex_str, line)
            if m and m.group(1):
                #print(f"{asset_path}{m.group(1)}")
                assets.append(f"{asset_path}{m.group(1)}")



for asset in assets:
    print(f"downloading asset for {asset}")
    url = asset
    path = "assets/" + url.split("assets/")[1].split("?")[0]
    dir_path = "/".join(path.split("/")[0:-1])
    #print(url)
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(path, 'wb') as f:
            for chunk in r:
                f.write(chunk)


asset_path = do_shit()

with open('lexp.js', 'r') as jfile:
    for line in jfile.readlines():
        if "png" in line or "webm" in line or "jpg" in line:
            regex_str = r'^.*"((?:images|video).*(?:png|jpg|webm).*)"[^:].*$'
            m = re.search(regex_str, line)
            if m and m.group(1):
                #print(f"{asset_path}{m.group(1)}")
                assets.append(f"{asset_path}{m.group(1)}")



for asset in assets:
    print(f"downloading asset for {asset}")
    url = asset
    path = "assets/" + url.split("assets/")[1].split("?")[0]
    dir_path = "/".join(path.split("/")[0:-1])
    #print(url)
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(path, 'wb') as f:
            for chunk in r:
                f.write(chunk)