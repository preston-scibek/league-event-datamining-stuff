import re, requests, os, json

from track_asset_path import get_versioned_asset_path
from datamine import URL

import jsbeautifier

assets = []

asset_path = get_versioned_asset_path(URL)
r = requests.get(f"{asset_path}/dist.js")
assert(r.status_code == 200)

js = jsbeautifier.beautify(f"\n{r.text}")
with open('dist.js', 'w') as jfile:
    jfile.writelines(js)

for line in js.split("\n"):
    if "png" in line or "webm" in line or "jpg" in line:
        regex_str = r'^.*"((?:images|video).*(?:png|jpg|webm).*)"[^:]?.*$'
        m = re.search(regex_str, line)
        if m and m.group(1):
            #print(f"{asset_path}{m.group(1)}")
            assets.append(f"{asset_path}{m.group(1)}")
fails = []
success = []
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
        success.append(url)
    else:
        print(f"download failed for {url}")
        fails.append(url)

print(f"\n\n\n\nfailed downloads are: \n {json.dumps(fails)}\n\n\n")
