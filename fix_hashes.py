import json
from dehash_lines import dehash

def style_scenes():
    # load out scenes file
    with open("updated_scenes_styled.json", 'r') as jsonfile:
        scenes = json.load(jsonfile)

    
    for region in scenes:
        for scene in region:
            if scene.get('dialogueKey'):
                scene['dialogue'] = dehash(scene['dialogueKey'])
            if scene.get('descriptionKey'):
                scene['description'] = dehash(scene['descriptionKey'])
            responses = scene.get('responses')
            if responses:
                for response in responses:
                    if response.get('dialogueKey'):
                        response['dialogue'] = dehash(response['dialogueKey'])

    return scenes


if __name__ == "__main__":
    new_scenes = style_scenes()
    
    # write the output to the file
    with open('updated_scenes_styled.json', 'w', encoding='utf-8') as jfile:
        json.dump(new_scenes, jfile, indent=4, ensure_ascii=False)