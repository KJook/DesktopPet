import json

def addWebSite(title, url):
    if title == "" or url == "":
        return
    with open('conf.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    webSites = data['web']
    for i in webSites:
        if i['title'] == title:
            return
    webSites.append({
        "title": title,
        "url": url
    })
    with open('conf.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)

def delWebSite(name):
    with open('conf.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    webSites = data['web']
    for i in webSites:
        if i['title'] == name:
            webSites.remove(i)
            with open('conf.json', 'w', encoding='utf-8') as f:
                json.dump(data, f)
            return 0
    return 1    

    