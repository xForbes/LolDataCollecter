from riotwatcher import LolWatcher, ApiError
import urllib.request, json
import urllib.error
import json
import config
import championIds
import asyncio
import aiohttp
import time 

api_key = config.lol_api_key
watcher = LolWatcher(api_key)
my_region = 'na1'
with urllib.request.urlopen("http://ddragon.leagueoflegends.com/cdn/12.15.1/data/en_US/champion.json") as url:
    champData = json.loads(url.read().decode())
with urllib.request.urlopen("https://ddragon.leagueoflegends.com/api/versions.json") as url:
    patch_number = json.load(url)

idToNames = championIds.setUp()
# queue of matches to be processed
match_queue = []
# queue of players to be processed
player_queue = []
# list of recorded games
game_list = set()
# list of recorded players
player_list = set()
# total games played
total_games = 0
# dict of champion data to be added
champ_data = {"champName" : {"wins": 0, "totalbans": 0, "gamesbanned": 0, "gamesPlayed": 0}}

REQUESTS_PER_SECOND = 20  # Adjust this according to your API rate limits
REQUEST_INTERVAL = 1.0 / REQUESTS_PER_SECOND

def get_puuid (player_name):
    """
    This method will return the puuid of the player. currently need since I do not have a key to decrypt the puuid from matches.
    ----------
    player_name : str
        The name of a player 
    Returns (Type: str)
    ----------
    Returns the unique puuid of said player
    """
    try:
        puuid = watcher.summoner.by_name(my_region, player_name)['puuid']
    except:
        print("error")
        return 
    time.sleep(1.25)
    return puuid
    #pid = watcher.summoner.by_name(my_region, player_name)['puuid']
    #return pid['puuid']

def get_current_patch():
    return patch_number[0]

def collect_match_data (player_name):
    """
    This method will return a list of the game played by said player on the current patch.
    ----------
    player_name : str
        The name a the queue type you're interested in
    Returns (Type: int)
    ----------
    Returns a list of the played matches on the current patch
    """
    puuid = get_puuid(player_name) 
    if puuid == None :
        return
    match_queue.extend(watcher.match.matchlist_by_puuid(my_region, puuid, type = "ranked",count = 100))
    #clean match_queue
    for game in match_queue:
        if game in game_list:
            match_queue.remove(game)
    time.sleep(1.25)
    #print (match_queue)
    #print (watcher.match.by_id(my_region, match_queue[0])["info"]["participants"][0]["summonerName"])
    #anaylize_game(match_queue[0])
    #match_queue.pop(0)
    #anaylize_game(match_queue[0])
    while match_queue:#and len(game_list) < 100:
        analyze_game(match_queue.pop(0))
        print(total_games)
        time.sleep(1.25)
    
def analyze_game (game_id):
    """
    This method will return a list of the game played by said player on the current patch.
    ----------
    game_id : str
        the game id from the games queue
    Returns (Type: ???)
    ----------
    No return: adds data directly to file
    """
    if game_id in game_list:
        return
    try:
        game = watcher.match.by_id(my_region, game_id)
    except:
        print("error")
        return
    if get_current_patch()[0:5] != game["info"]["gameVersion"][0:5]:
        match_queue.clear()
        print("Obadoba")
        return
    game_list.add(game_id)
    temp = game["info"]
    ban_list = temp["teams"][0]["bans"]
    ban_list.extend(temp["teams"][1]["bans"])

    #loop through each player
    #at the moment print it
    #for participant in temp["participants"]:
        #print(participant["summonerName"] + " " + participant["championName"] + " " + str(participant["championId"]) + " " + str(participant["win"]))
    #print(ban_list)

    #win/loss loop
    for participant in temp["participants"]:
        id = str(participant["championId"])
        champ_name = ""
        if id in idToNames.keys():
            champ_name = idToNames[id]
            #print(champ_name)
        if champ_name not in champ_data.keys():
            champ_data[champ_name] = {"wins": 0, "totalbans": 0, "gamesbanned": 0,  "gamesPlayed": 0}
        if participant["win"] == True:
            champ_data[champ_name]["wins"] =  champ_data[champ_name]["wins"] + 1
            champ_data[champ_name]["gamesPlayed"] = champ_data[champ_name]["gamesPlayed"] + 1
        else:
            champ_data[champ_name]["gamesPlayed"] += 1
    #print(idToNames.keys())
    #ban loop
    gameBans = set()
    for ban in ban_list:
        id = str(ban["championId"])
        champ_name = ""
        if id == "-1":
            continue
        if id in idToNames.keys():
            champ_name = idToNames[id]
            #print(champ_name)
        if champ_name not in champ_data.keys():
            champ_data[champ_name] = {"wins": 0, "totalbans": 0, "gamesbanned": 0, "gamesPlayed": 0}
        champ_data[champ_name]["totalbans"] = champ_data[champ_name]["totalbans"] + 1
        if champ_name not in gameBans:
            champ_data[champ_name]["gamesbanned"] = champ_data[champ_name]["gamesbanned"] + 1
            gameBans.add(champ_name)
        else:
            continue
    increment()

    #add players that might not be in the list
    for player in game['info']['participants']:
        if player['summonerName'] not in player_list:
            player_list.add(player['summonerName'])
            player_queue.append(player['summonerName'])

def increment():
    global total_games
    total_games = total_games+1
    
def get_challenger():
    return watcher.league.challenger_by_queue(my_region, queue = "RANKED_SOLO_5x5")

def driver():
    #build players queue and list 
    #start the core loop of the program 
    #end conditions of the program 
    #   60000 game anaylized 
    #conditions to look for 
    #   on previous patch 
    #   drop all matches on previous patch and move to next person
    starting_set = get_challenger()
    time.sleep(1.25)
    for player in starting_set['entries']:
        player_list.add(player["summonerName"])
    player_queue.extend(player_list)
    while len(player_queue) != 0 and total_games < 10000: #len(game_list) < 10:
        collect_match_data(player_queue[0])
        #print(player_queue[0])
        player_list.add(player_queue.pop(0))
        with open('stats.json','w') as f:
            json_string = json.dumps(sorted(champ_data.items()))
            f.write(json_string)
        
def main():
    print(time.time())
    print("Hello World!")
    #collect_match_data("x minus t")
    #get_current_patch()
    driver()
    #print(sorted(champ_data.items()))
    with open('stats.json','w') as f:
        json_string = json.dumps(sorted(champ_data.items()))
        f.write(json_string)
    print(len(game_list))
    print(time.time())
    


if __name__ == "__main__":
    main()

#print(watcher.match.by_id(my_region, to_enqueue[0])["metadata"]["participants"][0])
    #print(watcher.match.by_id(my_region, match_queue[0])["info"]["participants"][0]["summonerName"])
    #temp = watcher.match.by_id(my_region, match_queue[0])["info"]["participants"]
    #for participant in temp:
    #    print(participant["summonerName"])