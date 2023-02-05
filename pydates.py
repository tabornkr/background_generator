import datetime

x = datetime.datetime.now()
# print(x)
# day=2023-01-29
# print(x.time())


import requests
from bs4 import BeautifulSoup as bs



import requests
from bs4 import BeautifulSoup as bs

URL = 'https://www.ycombinator.com/?p=3'
# https://news.ycombinator.com///?p=3

req = requests.get(URL)
soup = bs(req.text, 'html.parser')
links = soup.select('.titleline')
subtext = soup.select('.subtext')

titles = soup.find_all('div', attrs={'class', 'head'})

print(links)

    # for i in range(4, 19):
    #     if page > 1:
    #         print(f"{(i - 3) + page * 15}" + titles[i].text)
    #     else:
    #         print(f"{i - 3}" + titles[i].text)