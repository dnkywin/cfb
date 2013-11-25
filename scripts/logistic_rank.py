#!/usr/bin/python
import math
from parsed_game_reader import games, wins, loss, WEEKNUM
from team_reader import names, IDs

METHOD = 'logistic'

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
        hi = MU*1000.0
        while(hi-lo>0.0001):
            mid = (hi+lo)/2
            if sum([1/(mid/i+1.0) for i in played]) + 2.0/(mid/MU+1.0) > numloss+1.0:
                lo = mid
            else:
                hi = mid
        newpower[team] = lo
        if (abs(newpower[team]-power[team])>0.001):
            stable = False

    power = newpower

ranks = sorted([(power[i],i) for i in wins if len(wins[i])+len(loss[i])>4])

outp = open("ranks/logistic/%s_rank_week%s.txt"%(METHOD, WEEKNUM),"w")
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