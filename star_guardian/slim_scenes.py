import json, re

def slim_scenes_2(scenes):
	res = {}
	for sublist in scenes:
		for subdict in sublist:
			re_str = r"^(chapter|epilogue|tutorial)_(?:(\d+)_)?(?:act_(\d+)_)?scene_([a-d0-9]+)_(\d+)?_?text$"
			re_str2 = r"^([a-z]+)_(\d+)_scene_([a-d0-9]+)_(\d+)?_?text$"
			re_compiled = re.compile(re_str)
			re_compiled2 = re.compile(re_str2)
			matches = re_compiled.search(subdict.get('dialogueId'))
			matches2 = re_compiled2.search(subdict.get('dialogueId'))
			if matches:
				type_ = matches.group(1)
				chapter =matches.group(2)
				act = matches.group(3)
				scene = matches.group(4)
				choice = matches.group(5)
			elif matches2:
				type_ = 'champ'
				chapter = matches2.group(1)
				act = matches2.group(2)
				scene = matches2.group(3)
				choice = matches2.group(4)
			
			chapter = f"{type_.title()} {chapter if chapter else ''}".strip() if type_ != 'champ' else chapter
			act = f"Act {act}"
			res[chapter] = res.get(chapter, {})
			res[chapter][act] = res[chapter].get(act, {})
			res[chapter][act][subdict['sceneId']] = res[chapter][act].get(subdict['sceneId'], {
				'speaker': subdict['speakerId'],
				'dialogueId': subdict['dialogueId'],
				'response': subdict.get('responses', []),
				'dialogue': subdict.get('dialogue', 'Dialogue is not Available Yet'),
				'next_scene_id': subdict.get('nextSceneId', None),
				'bg_url': subdict.get('bgURL', None)
			})
	for chapter_key, chapter_value in res.items():
		for act_key, act_value in chapter_value.items():
			res[chapter_key][act_key] = {k : v for k, v in sorted(act_value.items(), key=lambda q: int(q[0]) if q[0].isdigit() else int(q[0].split("_")[0][0:-1]))}
		res[chapter_key] = {k : v for k, v in sorted(chapter_value.items(), key=lambda q: q[0].split(" ")[1] if len(q[0].split(" ")) > 1 else q[0])}
	res = {k : v for k, v in sorted(res.items(), key=lambda q: f"ZZZ{q[0]}" if ('Chapter' not in q[0] and 'Epi' not in q[0] and "Tut" not in q[0]) else f"BBB{q[0]}" if "Tut" not in q[0] else f"AAA{q[0]}")}
	return res

if __name__ == "__main__":
	with open('scenes.json', 'r') as jfile:
		scenes = json.load(jfile)

	new_scenes = slim_scenes_2(scenes)

	with open('scenes_slim.json', 'w', encoding="utf-8") as jfile:
		json.dump(new_scenes, jfile, indent=4, ensure_ascii=False)

	res = ""
	for chapter_name, acts in new_scenes.items():
		for act_name, scenes in acts.items():
			res += (f"\n{chapter_name} {act_name}\n")
			prior = None
			prior_bg = None
			for scene_id, lines in scenes.items():
				if not scene_id.isdigit():
					continue
				if prior is not None:
					assert(scene_id == prior)
				if prior_bg != lines['bg_url']:
					res += f"{'-'*10}\n"
				prior = lines['next_scene_id']
				prior_bg = lines['bg_url']

				res += (f"{lines['speaker']}: {lines['dialogue']}\n")

				if len(lines.get('response')) > 0:
					i = 1
					for index, response in enumerate(lines.get('response')):
						res += (f"\t[Option {index + 1}] {response.get('dialogue', 'unknown')}\n")
						i += 1
						box = response
						# follow the option until we break outta the tree
						box['next_scene_id'] = box['nextSceneId']
						while box['next_scene_id'] is not None and not box['next_scene_id'].isdigit():
							box = scenes[box['next_scene_id']]
							res += (f"\t{box['speaker']}: {box['dialogue']}\n")
	with open('story_slim.txt', 'w+') as slimfile:
		slimfile.write(res)