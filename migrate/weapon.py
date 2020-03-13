import json
import requests
from bs4 import BeautifulSoup



def parseWeaponInfo(url):
    weaponeUrl = 'https://terraria.gamepedia.com' + url
    request = requests.get(weaponeUrl)
    info = BeautifulSoup(request.text, 'html.parser')
    item = info.find_all('div', class_='infobox item')[0]
    name = item.div.text
    info = item.find_all('table', class_='stat')
    for i in info:
        print('-----------------------------')
        print(i)
        print('-----------------------------')


# url = 'https://terraria.gamepedia.com/Weapons'
# request = requests.get(url)
# if request.status_code == requests.codes.ok:
#     html = BeautifulSoup(request.text, 'html.parser')
#     itemblocks = html.find_all('div', class_='itemlist')
#     for block in itemblocks:
#         items = block.find_all('li')
#         for item in items:
#             print(item.span.span.a['href'])

parseWeaponInfo('/Palladium_Repeater')




    