import json
import requests
import re
import pymongo
from bs4 import BeautifulSoup


def parseType(info, item):
    type = info.find('td').text.lower()
    item['type'] = type
    return item


def parseDamage(info, item):
    damageType = info.find('small')
    if(damageType is not None):
        damageType = damageType.text
        damage = info.find('td').text.replace(damageType, '')
        item['info']['damage'] = damage
        item['info']['damage_type'] = damageType.lower()
    else:
        damage = info.find('td').text
        item['info']['damage'] = damage
        item['info']['damage_type'] = None

    return item


def parseUseAmmo(info, item):
    ammo = info.find('td').text.lower()
    item['info']['ammo'] = ammo
    return item


def parseKnockback(info, item):
    knock = info.find('span', class_='kb').text.replace(
        info.find('span', class_='knockback').text, '').lower()
    item['info']['knock_back'] = knock
    return item


def parseCriticalChance(info, item):
    item['info']['critical_chance'] = info.find('td').text
    return item


def parseUseTime(info, item):
    usetime = info.find('td').text.replace(info.find('small').text, '').lower()
    item['info']['use_time'] = usetime
    return item


def parseVelocity(info, item):
    velocity = info.find('td').text
    item['info']['velocity'] = velocity
    return item


def parseRarity(info, item):
    # no use
    return item


def parseSell(info, item):
    # no use
    return item

def createItem(item):
    
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['terraria']
    mycol = mydb["item"]
    x = mycol.insert_one(item)
    print(x.inserted_id)
    return x


def weaponInfoParser(funcType, info, item):
    func = {
        'type': parseType,
        'uses_ammo': parseUseAmmo,
        'damage': parseDamage,
        'knockback': parseKnockback,
        'critical_chance': parseCriticalChance,
        'use_time': parseUseTime,
        'velocity': parseVelocity,
        'rarity': parseRarity,
        'sell': parseSell
    }

    method = func.get(funcType)
    if method:
        return method(info, item)
    else:
        print(f"{funcType} is  not define func")
        return item


def parseWeaponCrafting(parse, item):
    craftTable = parse.find('div', class_='crafts')
    item['craft'] = {}
    craftList = []
    if(craftTable is None):
        print("None")
        return item
    craftType = parse.find_all('h3')
    patternUse = 'Used in'
    patternRecipe = 'Recipe'
    for type in craftType:
        if(re.search(patternUse, type.text) is not None):
            craftList.append('use_in')
        if(re.search(patternRecipe, type.text) is not None):
            craftList.append('recipe')

    craftElements = craftTable.find('td', class_='ingredients').find_all('li')
    craftStations = craftTable.find('td', class_='station').find_all('img')
    for craft in craftList:
        print(craft)
        # craft ingredients
        item['craft'][craft] = {}
        item['craft'][craft]['ingredients'] = []
        for element in craftElements:
            obj = {}
            obj['img'] = element.find('img')['src']
            obj['element'] = element.text
            item['craft'][craft]['ingredients'].append(obj)
        # craft station
        item['craft'][craft]['stations'] = []
        for station in craftStations:
            obj = {}
            obj['img'] = station['src']
            obj['element'] = station['alt']
            item['craft'][craft]['stations'].append(obj)
    
    return item


def parseWeaponInfo(url):
    item = {'info': {}, 'craft': {}}
    weaponeUrl = 'https://terraria.gamepedia.com' + url
    request = requests.get(weaponeUrl)
    parse = BeautifulSoup(request.text, 'html.parser')
    itembox = parse.find('div', class_='infobox item')
    infobox = itembox.find('table', class_='stat')
    infos = infobox.find_all('tr')
    # parse basic info
    for info in infos:
        indexType = info.find('th').text.lower().replace(" ", "_")
        item = weaponInfoParser(indexType, info, item)
    # parse crafting tree
    item = parseWeaponCrafting(parse, item)
    return item


url = 'https://terraria.gamepedia.com/Weapons'
request = requests.get(url)
if request.status_code == requests.codes.ok:
    html = BeautifulSoup(request.text, 'html.parser')
    itemblocks = html.find_all('div', class_='itemlist')
    for block in itemblocks:
        items = block.find_all('li')
        for item in items:
            weaponUrl = item.span.span.a['href']
            print("-------------------------------------------")
            print(f"parse weapon {weaponUrl}")
            print("-------------------------------------------")
            weapon = parseWeaponInfo(weaponUrl)
            print(weapon)
            if weapon is not None:
                result = createItem(weapon)
                print(result)

                
# weapon = parseWeaponInfo('/Flare_Gun')
# print(weapon)
            
