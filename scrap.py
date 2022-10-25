import requests
from bs4 import BeautifulSoup
import re


def ScrapBlogs(urls):

    response = requests.get(str(urls)).text.encode('utf8').decode('ascii', 'ignore')
    soup = BeautifulSoup(response, 'html.parser')
    find_all_a = soup.find_all("a")
    urls=set()

    for x in find_all_a:
        if 'https' not in  x['href'] and \
            "/tag/" not in x['href'] and \
            "/?source" not in x['href'] and \
            "/plans?" not in x['href'] and \
            not re.match("/@\w*[a-zA-Z0-9]\?", x['href']):
            urls.add(x['href'])

    url_list = list(urls)
    return url_list[1:7]

