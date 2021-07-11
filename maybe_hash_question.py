def HashString(str):
    hash = 0
    temp = 0
    for character in str:
        hash = (hash << 4) + ord(character.lower())
        temp = hash & 0xf0000000
        if temp != 0:
            hash = hash ^ (temp >> 24)
            hash = hash ^ temp
    return hash


print(HashString("prologue_demacia_s1_scene_10_text"))