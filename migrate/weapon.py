import json
import requests
from bs4 import BeautifulSoup


def parseType(info, item):
    type = info.find('td').text.lower()
    item['type'] = type
    return item

def parseDamage(info, item):
    damageType = info.find('small').text
    damage = info.find('td').text.replace(damageType, '')
    item['info']['damage'] = damage
    item['info']['damage_type'] = damageType.lower()

    return item

def parseUseAmmo(info, item):
    ammo = info.find('td').text.lower()
    item['info']['ammo'] = ammo
    return item

def parseKnockback(info, item):
    knock = info.find('span', class_='kb').text.replace(info.find('span', class_='knockback').text, '').lower()
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


def weaponInfoParser(funcType, info, item):
    func = {
        'type': parseType,
        'uses_ammo' : parseUseAmmo,
        'damage' : parseDamage,
        'knockback' : parseKnockback,
        'critical_chance' : parseCriticalChance,
        'use_time' : parseUseTime,
        'velocity' : parseVelocity,
        'rarity' : parseRarity,
        'sell' : parseSell
    }

    method = func.get(funcType)
    if method:
        return method(info, item)
    else:
        print(f"{funcType} is  not define func")


def parseWeaponInfo(url):
    item = {'info':{}}
    weaponeUrl = 'https://terraria.gamepedia.com' + url
    request = requests.get(weaponeUrl)
    parse = BeautifulSoup(request.text, 'html.parser')
    itembox = parse.find('div', class_='infobox item')
    infobox = itembox.find('table', class_='stat')
    infos = infobox.find_all('tr')
    for info in infos:
        indexType = info.find('th').text.lower().replace(" ", "_")
        item = weaponInfoParser(indexType, info, item)
    print(item)


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
