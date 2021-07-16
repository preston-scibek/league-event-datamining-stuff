import json

def style_scenes():
    # load out scenes file
    with open("updated_scenes.json") as jsonfile:
        scenes = json.load(jsonfile)

    host = "generalbloodsword.com/"
    
    for region in scenes:
        for scene in region:
            chars = [("char{}".format(x), scene.get("char{}".format(x))) for x in range(1,5) if scene.get("char{}".format(x)) is not None]
            speaker = scene.get('speakerKey', '')
            bg = scene.get('bg', '')

            for char in chars:
                scene["{}_image".format(char[0])] = '{}assets/scenery/characters/{}.png'.format(host, char[1])

            scene['bg_image'] = '{}assets/scenery/backgrounds/{}.jpg'.format(host, bg)
            scene['speaker_image'] = '{}assets/scenery/speakers/{}.png'.format(host, "_".join(speaker.split("_")[1::]))

    return scenes

if __name__ == "__main__":
    new_scenes = style_scenes()
    
    # write the output to the file
    with open('updated_scenes_styled.json', 'w') as jfile:
        json.dump(new_scenes, jfile, indent=4)