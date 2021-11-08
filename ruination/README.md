# ruination-event-stuff


## datamine_single_file.py

All this file requires is the python requirements to be installed and the scenes.json file that is in this repo.  
This file will then construct a json record that contains the image assets links as well as the dialogue for the scenes.  





## ggez.py

powershell `python ./ggez.py`

### How It Works

1. Utilizes requests to download https://frontpage.na.leagueoflegends.com/en_US/channel/lol/home/event/sentinels-hub-2021#/  
2. Utilizes BeautifulSoup to loop through the script tags and when it finds dist.js , delete it
3. Inject a modified dist.js that assigns the hashmap to window.dehashFunction
4. Save this modified html to a local file
5. Using Chrome Selenium launch this html page
6. Loop through each scene in scenes.json and executes `console.log(window.dehashFunction(<dialogueKey>))`
7. Take that log and add it to the scene dict
8. Return the list of scene dicts
9. Write the updated secnes to a new json file


### Requires
dist-modified.js  
scenes.json  
updated_scenes_styled.json - added in image assets (credit to u/LordredstoneNr1 for these)  
`pip install -r requirements.txt`  

## FILES

### JSON 
lines.json - json file of the dialoge lines and ids  
scenes.json - json file storing the results  
speakers.json - json file storing the speakers  
characters.json - json file storing the characters that show up  
assets.json - json file with the asset mapping - https://lolstatic-a.akamaihd.net/frontpage/apps/prod/sentinels-hub-2021/en_US/08edf12f55c2dfb944d448da4a234b384321ec73  
journal.json - rookie's jounral converted to json  
partial_revhash.json - file containing a partial reverse hash table for the lines  
lines_dehashed.json - file containing the lines for the above reverse hash table  
champ_entries.json - file containing the json for the characters (incomplete)

### JS
decode.js - base64 decode of the dialogue mapping  
getLines.js - js file to pull out the dialogue lines  
dist-modified.js - our modified version of riots dist.js to utilize the hashing of the dialogueKeys

### PY

get_lines.py - pulls the dialogue lines from riot  
get_speakers.py - writes the lists of speakers/characters to json files  
fix_hashes.py - loops through updated_scenes_styled.json and ensures the dehashed values are accurated  
dehash_lines.py - takes a cmdline argument, appends the approrriate data, converts it to its md5 hash and returns the line associated with it  
convert_hashed_to_dehashed.py - adhoc function to convert a set of strings to lines given their hashes  
style_scenes.py - update scenes with assets  


### HTML
decode.html - simple html file to run decode.js
