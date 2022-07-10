import re, time
urls = set()
with open("debug.log", "r") as debug_file:
    for line in debug_file:
        compiled = re.compile(r'(https://frontpage.na.leagueoflegends.com/en_US/channel/[a-z\-A-Z\\\\/0-9_\.]+' +
            '|https://lolstatic-a.akamaihd.net/frontpage/apps/prod/[a-z_\-A-Z\\\\/0-9\.]+' +
            '|https://static.rgpub.io/[a-z\-A-Z\\\\/0-9_\.]+)')
        m = compiled.search(line)
        if m:
            urls.add(m.group(1))

timestr = time.strftime("%Y%m%d-%H%M%S")
with open(f'urls_{timestr}.txt', 'w') as urls_file:
    for url in urls:
        urls_file.write(f"{url}\n")
