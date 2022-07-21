import json

def slim_scenes(scenes):
    for index1, l1 in enumerate(scenes):
        for index2, l2 in enumerate(l1):
                scenes[index1][index2] = "{}: {}: {}".format(l2.get('dialogueId', ""), l2.get('speakerId', ""), l2.get('dialogue', l2.get('description')))
    return scenes

if __name__ == "__main__":
	with open('scenes.json', 'r') as jfile:
		scenes = json.load(jfile)

	new_scenes = slim_scenes(scenes)

	with open('scenes_slim.json', 'w', encoding="utf-8") as jfile:
		json.dump(new_scenes, jfile, indent=4, ensure_ascii=False)