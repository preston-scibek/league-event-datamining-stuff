import json

from fix_hashes import style_scenes, style_scenes_asset
from get_lines import get_lines, get_host


if __name__ == "__main__":
    # download lines
    with open('scenes.json', 'r') as jfile:
        scenes = json.load(jfile)

    lines = get_lines()
    styled_scenes = style_scenes(scenes, lines)
    styled_scenes_assets = style_scenes_asset(styled_scenes, host=get_host())

    with open('datamine.json', 'w', encoding="utf-8") as jfile:
        json.dump(styled_scenes_assets, jfile, indent=4, ensure_ascii=False)