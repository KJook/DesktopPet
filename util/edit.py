import json
import requests
import os

def init_icon(url, name):
    path = './resourses/webicon'
    m_path = './resourses/webicon/favicon.ico'
    file_path = os.path.join(path, name + '.ico')
    if os.path.exists(file_path):
        return 0, file_path
    try:
        print(url)
        response = requests.get(url, stream=True, timeout=(1, 3))  # stream=True必须写上
        print("request")
    except:
        return -1, m_path
    chunk_size = 1024  # 每次下载的数据大小
    try:
        if response.status_code == 200:  # 判断是否响应成功
            with open(file_path, 'wb') as file:  # 显示进度条
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
            return 0, file_path
        else:
            return 2, m_path
    except Exception as e:
        return 1, m_path



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

    