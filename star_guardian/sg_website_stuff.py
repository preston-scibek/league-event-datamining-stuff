import json, requests
#with open("sg_website_events.json", 'r') as jfile:
#    j = json.load(jfile)
url = 'https://starguardian.riotgames.com/page-data/en-us/timeline/page-data.json'
#  https://starguardian.riotgames.com/page-data/en-us/content/shadow-of-a-doubt/page-data.json
j = requests.get(url).json()
res_l = []
for res in sorted(j['result']['data']['hotspots']['nodes'], key=lambda x: x['content_metadata']['publish_date']):
    print(res['reference'][0]['title'], res['reference'][0]['label'], res['locked_subtitle'], res['content_metadata']['publish_date'], sep="|")

with open('sg_website_events_backup.json', 'w') as jfile:
    json.dump(j, jfile, indent=4)