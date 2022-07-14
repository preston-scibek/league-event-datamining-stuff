import json
with open("sg_website_events.json", 'r') as jfile:
    j = json.load(jfile)
res_l = []
for res in sorted(j['result']['data']['hotspots']['nodes'], key=lambda x: x['content_metadata']['publish_date']):
    print(res['reference'][0]['title'], res['reference'][0]['label'], res['locked_subtitle'], res['content_metadata']['publish_date'], sep="|")