#!/usr/bin/python
import math
import sys

WEEKNUM = int(sys.argv[1])
METHOD = 'logistic'

name_inp = open("team.csv","r")
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

inp = open("games-parsed-week%s.txt"%(WEEKNUM,), "r")
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

power = {}

MU = 1000.0
for team in wins:
    power[team] = MU

stable = False
while not stable:
    newpower = {}
    stable = True
    for team in power:
        played = [power[i] for i in wins[team]]+[power[i] for i in loss[team]]
        numloss = len(loss[team])*1.0
        numplayed = len(loss[team])*1.0+len(wins[team])
        lo = 0
        hi = MU*1000000.0
        while(hi-lo>0.0000001):
            mid = (hi+lo)/2
            if sum([1/(mid/i+1.0) for i in played]) + 2.0/(mid/MU+1.0) > numloss+1.0:
                lo = mid
            else:
                hi = mid
        newpower[team] = lo
        if (abs(newpower[team]-power[team])>0.000001):
            stable = False

    power = newpower

ranks = sorted([(power[i],i) for i in wins if len(wins[i])+len(loss[i])>4])

outp = open("%s_rank_week%s.txt"%(METHOD, WEEKNUM),"w")
for i,j in enumerate(reversed(ranks)):
    outp.write("%s. %s (%s-%s)\n" % (i+1, names[j[1]],len(wins[j[1]]), len(loss[j[1]])))#, int(1200+400*math.log(j[0]/MU)/math.log(2))))

outp.close()

scores = {}
for g in games:
    game = games[g]
    tup1 = (game[1],game[3])
    tup2 = (game[3],game[1])
    if tup1 not in scores:
        scores[tup1] = []
        scores[tup2] = []
    if (power[game[0]]>power[game[2]]):
        scores[tup1].append(1.0)
        scores[tup2].append(0.0)
    elif power[game[2]]>power[game[0]]:
        scores[tup1].append(0.0)
        scores[tup2].append(1.0)

l = [score for score in scores if score[0]>score[1]]
freq = sorted(l, key = lambda x: -len(scores[x]))
highprob = sorted(l, key = lambda x: -sum(scores[x])/len(scores[x]))

#for i in highprob:
#    print "%s wins: %s losses: %s" % (i, sum(scores[i]), len(scores[i])-sum(scores[i]))