
urls = set()
with open('urls_20220805-154117.txt', 'r') as f:
    for line in f.readlines():
        urls.add(line)
urls = list(urls)
urls.sort()
with open('urls_20220805-154117.txt', 'w') as f:
    f.writelines(urls)