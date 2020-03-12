import json
import requests
from bs4 import BeautifulSoup


url = 'https://terraria.gamepedia.com/Weapons'
request = requests.get(url)
if request.status_code == requests.codes.ok:
    html = BeautifulSoup(request.text, 'html.parser')
    lists = html.find_all('div', class_='main-heading')
    for list in lists:
        print(list.div.div.text)