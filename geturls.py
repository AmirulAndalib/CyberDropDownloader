import requests
import os
from bs4 import BeautifulSoup, SoupStrainer


def Extrair_Links(u):
    try:
        url = u
        page = requests.get(url)
        data = page.text
        soup = BeautifulSoup(data, features="html5lib")
        links = []
        if 'cyberdrop' in u.lower():
            for link in soup.find_all(id="file"):
                lis = link.get('href')
                if len(str(lis)) > 30:
                    lis = lis.replace('.nl/', '.cc/')
                    links.append(lis)
        elif 'dmca.gripe' in u.lower():
            for link in soup.find_all('a', {'class': 'download-button'}):
                lis = link.get('href')
                if len(str(lis)) > 30:
                    links.append(lis)
        linksP = list(dict.fromkeys(links))
    except Exception as e:
        print(e)
        return None
    else:
        return linksP
