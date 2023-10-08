from riotwatcher import LolWatcher, ApiError
import urllib.request, json
import urllib.error
import json
import config
import championIds

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
game_list = []
# list of recorded players
player_list = []
# total games played
total_games = 0
# dict of champion data to be added
champ_data = {"champName" : {"wins": 0, "bans": 0, "gamesPlayed": 0}}

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
    match_queue.extend(watcher.match.matchlist_by_puuid(my_region, puuid, type = "ranked"))
    #print (match_queue)
    #print (watcher.match.by_id(my_region, match_queue[0])["info"]["participants"][0]["summonerName"])
    #anaylize_game(match_queue[0])
    #match_queue.pop(0)
    #anaylize_game(match_queue[0])

    while len(match_queue) != 0 and len(game_list) < 100:
        anaylize_game(match_queue[0])
        if len(match_queue) == 0:
            break
        match_queue.pop(0)
    
def anaylize_game (game_id):
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
    game = watcher.match.by_id(my_region, game_id)
    if get_current_patch()[0:5] != game["info"]["gameVersion"][0:5]:
        match_queue.clear()
        return
    game_list.append(game_id)
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
            champ_data[champ_name] = {"wins": 0, "bans": 0, "gamesPlayed": 0}
        if participant["win"] == True:
            champ_data[champ_name]["wins"] =  champ_data[champ_name]["wins"] + 1
            champ_data[champ_name]["gamesPlayed"] = champ_data[champ_name]["gamesPlayed"] + 1
        else:
            champ_data[champ_name]["gamesPlayed"] += 1
    #print(idToNames.keys())
    #ban loop
    for ban in ban_list:
        id = str(ban["championId"])
        champ_name = ""
        if id == "-1":
            continue
        if id in idToNames.keys():
            champ_name = idToNames[id]
            #print(champ_name)
        if champ_name not in champ_data.keys():
            champ_data[champ_name] = {"wins": 0, "bans": 0, "gamesPlayed": 0}
        champ_data[champ_name]["bans"] = champ_data[champ_name]["bans"] + 1
    
def get_challenger():
    return watcher.league.challenger_by_queue(my_region, queue = "RANKED_SOLO_5x5")

def driver():
    #build players queue and list 
    #start the core loop of the program 
    #end conditions of the program 
    #   60000 game anaylized 
    #conditions to look for 
    #   on previous patch 
    #       drop all matches on previous patch and move to next person
    starting_set = get_challenger()
    for player in starting_set['entries']:
        player_list.append(player["summonerName"])
    player_queue = player_list
    i = 0
    while len(player_queue) != 0 and i < 5: #len(game_list) < 100:
        collect_match_data(player_queue[0])
        print(player_queue[0])
        #print(len(game_list))
        player_queue.pop(0)
        i= i + 1
        
def main():
    print("Hello World!")
    #collect_match_data("afrodude34")
    #get_current_patch()
    driver()
    print(sorted(champ_data.items()))

if __name__ == "__main__":
    main()

#print(watcher.match.by_id(my_region, to_enqueue[0])["metadata"]["participants"][0])
    #print(watcher.match.by_id(my_region, match_queue[0])["info"]["participants"][0]["summonerName"])
    #temp = watcher.match.by_id(my_region, match_queue[0])["info"]["participants"]
    #for participant in temp:
    #    print(participant["summonerName"])