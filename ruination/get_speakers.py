import json

with open("scenes.json", "r") as jfile:
	regions = json.load(jfile)


speakers = set()
characters = set()

for region in regions:
	for scene in region:
		speakers.add(scene.get('speakerKey', ''))
		characters.add(scene.get('char1', ''))
		characters.add(scene.get('char2', ''))
		characters.add(scene.get('char3', ''))
		characters.add(scene.get('char4', ''))

with open('speakers.json', 'w') as jfile:
	json.dump(list(speakers), jfile, indent=4)
with open('characters.json', 'w') as jfile:
	json.dump(list(characters), jfile, indent=4)