import json
with open('speakers_named.json', 'r') as jfile:
    s = json.load(jfile)

new = {}
for speaker, assets in s.items():
    for asset in assets:
        new[asset] = speaker
with open('speakers_reverse.json', 'w+') as jfile:
    json.dump(new, jfile, indent=4)