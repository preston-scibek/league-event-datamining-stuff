import json
from collections import OrderedDict
from itertools import chain

def order_scenes(scenes):
	#The canon order is Demacia > Freljord > Noxus > Ionia > Targon > P/Z > Ixtal > Bilge > Shurima > Shadow Isles

	order = ['demacia', 'freljord', 'noxus', 'ionia', 'targon', 'piltover', 'ixtal', 'bilgewater', 'shurima', 'shadow', 'induction', 'key']
	new_scenes = OrderedDict()
	for item in order:
		new_scenes[item] = []

	for chapter in scenes:
		dk = chapter[0].get('dialogueKey', chapter[0].get('nameKey'))
		loc = dk.split("scene")[0].split("_")[-2]
		chapter = (loc, chapter)
		region = [x for x in order if x in dk][0]


		new_scenes[region].append(chapter)
		new_scenes[region] = sorted(new_scenes[region], key=lambda x: x[0])

	for key, value in new_scenes.items():
		new_scenes[key] = list(chain.from_iterable([x[1] for x in value]))
	return new_scenes

if __name__ == "__main__":
	with open('datamine.json', 'r') as jfile:
		scenes = json.load(jfile)

	new_scenes = order_scenes(scenes)

	with open('datamine.json', 'w', encoding="utf-8") as jfile:
		json.dump(new_scenes, jfile, indent=4, ensure_ascii=False)