from riotwatcher import LolWatcher, ApiError
import pandas as pd

api_key = 'RGAPI-cf9dd47f-04ac-448f-a031-8215ecb67722'#Replace this with your API
watcher = LolWatcher(api_key)
my_region = 'oc1'
acc = 'RagingDragNinja'

def get_wr(name,region):
    try:
        me = watcher.summoner.by_name(region,name)
        my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])
        win_rate = (my_ranked_stats[0]['wins']/(my_ranked_stats[0]['losses']+my_ranked_stats[0]['wins']))
        return round(win_rate*100)
    except IndexError:
        return -1
 
me = watcher.summoner.by_name(my_region,acc)

matches = watcher.match.matchlist_by_account('oc1',me['accountId'])['matches']

fileinput = ""

for j in range(50):

    players = watcher.match.by_id('oc1',matches[j]['gameId'])['participantIdentities']#players for match j
    
    for i in range(5):
        fileinput = fileinput + str(get_wr(players[i]['player']['summonerName'],my_region)) + ","

    fileinput = fileinput + watcher.match.by_id('oc1',matches[j]['gameId'])['teams'][0]['win']+ "\n"#print if match j for team 1 is win/loss

    for i in range(5,10):
        fileinput = fileinput + str(get_wr(players[i]['player']['summonerName'],my_region)) + ","

    fileinput = fileinput + watcher.match.by_id('oc1',matches[j]['gameId'])['teams'][1]['win']+ "\n"#print if match j for team 2 is win/loss

    print(j*2 + 2,"%")

file = open("data.csv","a")
file.write(fileinput)
file.close()
