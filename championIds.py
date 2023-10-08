import urllib.request, json

with urllib.request.urlopen("https://ddragon.leagueoflegends.com/cdn/13.19.1/data/en_US/champion.json") as url:
    champData = json.loads(url.read().decode())

def setUp():
    idToName = {}
    for champ in champData["data"]:
        idToName[champData["data"][champ]["key"]] = champData["data"][champ]["name"]
    
    return idToName