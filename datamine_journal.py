import json
from dehash_lines import dehash

from fix_hashes import style_scenes, style_scenes_asset
from get_lines import get_lines, get_host


def journal(lines, host):
    miscs = ['journal.event_begin.copy']
    misc_entries = {}
    for misc in miscs:
        misc_entries[misc] = dehash(misc)


    regions = ['demacia', 'noxus_a', 'noxus_b', 
        'freljord_a', 'freljord_b', 'ionia_a', 'ionia_b', 'targon_a', 'targon_b', 
        'shurima', 'piltover_zaun', 'bilgewater_a', 'bilgewater_b', 'ixtal_a', 'ixtal_b',
        'shadow_isles']
    things = ["journal.{}.copy", "journal.{}.date"]
    region_entries = []
    for region in regions:
        temp_dict = {}
        for item in things:
            copy = item.format(region)
            temp_dict[copy] = dehash(copy)
        region_entries.append(temp_dict)


    keys = [
        "journal.week_{}.date",
        "journal.week_{}.copy",
        "journal.week_{}.unlock_note",
        "journal.week_{}.upgrade_name",
        "journal.week_{}.upgrade_description",
    ]
    journal_entries = []
    for i in range(1, 5):
        temp_dict = {}
        for item in keys:
            copy = item.format(i)
            temp_dict[copy] = dehash(copy)
        journal_entries.append(temp_dict)


    keys = [
        "journal.key_upgrade.{}.date",
        "journal.key_upgrade.{}.copy",
        "journal.key_upgrade.{}.unlock_note",
        "journal.key_upgrade.{}.upgrade_name",
        "journal.key_upgrade.{}.upgrade_description",
    ]
    key_upgrade_entires = []
    for i in range(1, 5):
        temp_dict = {}
        for item in keys:
            copy = item.format("a{}".format(i))
            temp_dict[copy] = dehash(copy)
        key_upgrade_entires.append(temp_dict)

    for i in range(1, 9):
        temp_dict = {}
        for item in keys:
            copy = item.format("b{}".format(i))
            temp_dict[copy] = dehash(copy)
        key_upgrade_entires.append(temp_dict)
    return [misc_entries, region_entries, journal_entries, key_upgrade_entires]
if __name__ == "__main__":
    with open('journal_single.json', 'w', encoding="utf-8") as jfile:
        json.dump(journal(get_lines(), get_host), jfile, indent=4, ensure_ascii=False)