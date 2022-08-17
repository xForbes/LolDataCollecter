from riotwatcher import LolWatcher, ApiError
import urllib.request, json
import json
import config

api_key = config.lol_api_key
watcher = LolWatcher(api_key)
my_region = 'na1'
with urllib.request.urlopen("http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/champion.json") as url:
    champData = json.loads(url.read().decode())
with urllib.request.urlopen("https://ddragon.leagueoflegends.com/api/versions.json") as url:
    patch_number = json.load(url)

# queue of matches to be processed
match_queue = {}
# queue of players to be processed
player_queue = {}
# list of recorded games
game_list = {}
# list of recorded players
player_list = {}

def get_puuid (player_name):
    """
    This method will return the puuid of the player.
    ----------
    player_name : str
        The name of a player 
    Returns (Type: str)
    ----------
    Returns the unique puuid of said player
    """
    pid = watcher.summoner.by_name(my_region, player_name)
    return pid['puuid']

def get_current_patch():
    print(patch_number[0])
    return patch_number[0]

def collect_matches (player_name):
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
    to_enqueue = watcher.match.matchlist_by_puuid(my_region, puuid, type = "ranked")
    print (to_enqueue)
    print(watcher.match.by_id(my_region, to_enqueue[0])["info"]["gameVersion"])

def main():
    print("Hello World!")
    collect_matches("afrodude34")
    get_current_patch()

if __name__ == "__main__":
    main()