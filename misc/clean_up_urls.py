
urls = set()
with open('urls.txt', 'r') as f:
    for line in f.readlines():
        urls.add(line)
urls = list(urls)
urls.sort()
with open('urls.txt', 'w') as f:
    f.writelines(urls)