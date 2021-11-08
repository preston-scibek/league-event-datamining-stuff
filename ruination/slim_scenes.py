import json

def slim_scenes(scenes):
	for k,v in scenes.items():
		for i, vv in enumerate(v):
			scenes[k][i] = "{}: {}".format(vv.get('speaker', ""), vv.get('dialogue', vv.get('description')))
	return scenes

if __name__ == "__main__":
	with open('datamine.json', 'r') as jfile:
		scenes = json.load(jfile)

	new_scenes = slim_scenes(scenes)

	with open('datamine_slim.json', 'w', encoding="utf-8") as jfile:
		json.dump(new_scenes, jfile, indent=4, ensure_ascii=False)