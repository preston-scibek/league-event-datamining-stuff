import json
from dehash_lines import dehash, hash_asset

def style_scenes(scenes=None, lines=None):
    if scenes is None:
        # load out scenes file
        with open("updated_scenes_styled.json", 'r') as jsonfile:
            scenes = json.load(jsonfile)

    
    for region in scenes:
        for scene in region:
            if scene.get('dialogueKey'):
                scene['dialogue'] = dehash(scene['dialogueKey'], lines=lines)
            if scene.get('descriptionKey'):
                scene['description'] = dehash(scene['descriptionKey'], lines=lines)
            responses = scene.get('responses')
            if responses:
                for response in responses:
                    if response.get('dialogueKey'):
                        response['dialogue'] = dehash(response['dialogueKey'], lines=lines)

    return scenes


def style_scenes_asset(scenes, host=None):
    """Append the assets to each scene"""
    for region in scenes:
        for scene in region:
            chars = [("char{}".format(x), scene.get("char{}".format(x))) for x in range(1,5) if scene.get("char{}".format(x)) is not None]
            speaker = scene.get('speakerKey', '')
            bg = scene.get('bg', '')

            for char in chars:
                scene["{}_image".format(char[0])] = '{}images/scenery/characters/{}.png'.format(host, hash_asset(char[1]))

            scene['bg_image'] = '{}images/scenery/backgrounds/{}.jpg'.format(host, hash_asset(bg, n=0))

            hardcodeds = {
                    "solari-fanatic-1": "solari-soldier",
                    "solari-fanatic-2": "solari-soldier",
                    "viegos-voice": "viego",
                    "viego-s-voice": "viego",
                    "lunari-commoners-1-2": "lunari-commoner-1",
                    "lunari-commoners-1---2": "lunari-commoner-1",
            }

            speaker = hardcodeds.get("-".join(speaker.split("_")[1::]), "-".join(speaker.split("_")[1::]))
            scene['speaker_image'] = '{}images/scenery/speakers/{}.png'.format(host, hash_asset(speaker, n=0))

    return scenes



if __name__ == "__main__":
    new_scenes = style_scenes()
    
    # write the output to the file
    with open('updated_scenes_styled.json', 'w', encoding='utf-8') as jfile:
        json.dump(new_scenes, jfile, indent=4, ensure_ascii=False)