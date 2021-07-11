import hashlib, json

"""
[
    "[Sentinel Headquarters. Far off the coast of Valoran.]",
    "759965dfe277348f9053cc2e507b413e"
  ], prologue_demacia_s1_scene_10_text
  """

res = "759965dfe277348f9053cc2e507b413e"

with open ("scenes.json") as jfile:
    scenes = json.load(jfile)

for l in scenes:
    for s in l:
        if hashlib.md5(b"en." + s.get("dialogueKey", "").encode()).hexdigest() == res:
            print(s)