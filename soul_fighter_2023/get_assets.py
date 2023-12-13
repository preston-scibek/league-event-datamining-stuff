import re, requests, os, json
import jsbeautifier

#https://akamai.embed.rgpub.io//wwpub-lol-soul-fighter-embed-2023/_nuxt/app.js?3a5a1e98e3f0aa4cbbc6

url = "https://akamai.embed.rgpub.io//wwpub-lolsoul-fighter-embed-2023/_nuxt/"
url = "https://embed.rgpub.io/mgs-soul-fighter-2023/metagame?"
url = "https://prod.embed.rgpub.io/wwpub-lol-soul-fighter-embed-2023/"
assets = []
asset_path = url + "app.js"


urls = []
# LOL 
asset_path = 'https://assetcdn.rgpub.io/public/live/bundle-offload/7df87236-402e-487a-9b60-e3016ad27fe4/64b9a8e6fcae86000882534e/app.f4c802.js'
download_url = 'https://assetcdn.rgpub.io/public/live/bundle-offload/7df87236-402e-487a-9b60-e3016ad27fe4/64b9a8e6fcae86000882534e/'

urls.appen((asset_path, download_url))
# UnityFS 5.x.x 2021.3.9f1
# https://embed.rgpub.io/mgs-soul-fighter-2023/webgl/StreamingAssets/aa/WebGL# UnityEngine.AddressableAssets.Addressables.RuntimePath
# https://embed.rgpub.io/mgs-soul-fighter-2023/webgl/StreamingAssets/aa/catalog.json # m_InternalIds

# https://embed.rgpub.io/mgs-soul-fighter-2023/webgl/StreamingAssets/aa/WebGL/motioncomicscene_scenes_all_bdc73d18d8fe5578dc4381539596e44a.bundle
# https://embed.rgpub.io/mgs-soul-fighter-2023/webgl/StreamingAssets/aa/WebGL/samira_assets_all_cb4f970a2d567e130c2524551b015f86.bundle
# https://embed.rgpub.io/mgs-soul-fighter-2023/webgl/StreamingAssets/aa/WebGL/jhin_tut_assets_all_1e273e69472f8626fb550fe2c2ca55a7.bundle

# TFT Soul Fighter?
asset_path = "https://assetcdn.rgpub.io/public/live/bundle-offload/3f5b23ef-a7d0-4849-a975-085eac949cfc/64b95e2ac2fa25000844d255/app.9afd6c.js"
download_url  = "https://assetcdn.rgpub.io/public/live/bundle-offload/3f5b23ef-a7d0-4849-a975-085eac949cfc/64b95e2ac2fa25000844d255/"
urls.appen((asset_path, download_url))

def get_assets(asset_path, download_url):
    r = requests.get(asset_path)
    assert(r.status_code == 200)

    js = jsbeautifier.beautify(f"\n{r.text}")
    with open('dist.js', 'w') as jfile:
        jfile.writelines(js)

    for line in js.split("\n"):
        if "png" in line or "webm" in line or "jpg" in line:
            regex_str = r'^.*"((_\/lib).*(?:png|jpg|webm).*)"[^:]?.*$'
            m = re.search(regex_str, line)
            if m and m.group(1):
                print(f"{download_url}{m.group(1)}")
                assets.append(f"{download_url}{m.group(1)}")

    fails = []
    success = []
    import subprocess
    import concurrent.futures

    def request_get(url):
        print(f"downloading asset for {url}")
        path = "assets/" + url.split("lib-embed/")[1].split("?")[0]
        dir_path = "/".join(path.split("/")[0:-1])
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
            with open(path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
            return True
        else:
            print(f"download failed for {url}")
            return False

    with concurrent.futures.ProcessPoolExecutor(max_workers=32) as executor:
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


for asset_path, download_url in urls:
    get_assets(asset_path, download_url)
