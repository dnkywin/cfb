import sys

WEEKNUM = int(sys.argv[1])
METHOD = 'logistic'

name_inp = open("data/team.csv","r")
name_data = name_inp.read()
name_inp.close()

names = {}
IDs = {}

for line in name_data.split('\n')[1:]:
    if line:
        datum = line.split(',')
        name, num = datum[1][1:-1],int(datum[0])
        names[num] = name
        IDs[name] = num

games = {}
wins = {}
loss = {}

inp = open("data/games-parsed-week%s.txt"%(WEEKNUM,), "r")
gamedata = inp.read()
inp.close()

for line in gamedata.split("\n"):
    if line:
        datum = line.split()
        games[datum[0]] = [int(i) for i in datum[1:]]

for game in games:
    res = games[game]
    if res[0] not in wins:
        wins[res[0]] = []
        loss[res[0]] = []
    if res[2] not in wins:
        wins[res[2]] = []
        loss[res[2]] = []

    if res[1]>res[3]:
        wins[res[0]].append(res[2])
        loss[res[2]].append(res[0])
    elif res[1]<res[3]:
        loss[res[0]].append(res[2])
        wins[res[2]].append(res[0])


remove_fcs = False
if remove_fcs:
    for team in wins.keys():
        if len(wins[team])+len(loss[team])<5:
            for t in wins[team]:
                loss[t].remove(team)
            for t in loss[team]:
                wins[t].remove(team)
            del wins[team],loss[team]