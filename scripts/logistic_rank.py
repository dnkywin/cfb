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

outp = open("ranks/%s/%s_rank_week%s.txt"%(METHOD,METHOD, WEEKNUM),"w")
for i,j in enumerate(reversed(ranks)):
    outp.write("%s. %s (%s-%s)\n" % (i+1, names[j[1]],len(wins[j[1]]), len(loss[j[1]])))#, int(1200+400*math.log(j[0]/MU)/math.log(2))))

outp.close()