#!/usr/bin/python
import math
from parsed_game_reader import games, wins, loss, WEEKNUM
from team_reader import names, IDs

METHOD = 'naive_SOS'

power = {}

for team in wins:
    power[team] = len(wins[team])*1.0 / (len(wins[team])+len(loss[team]))

stable = False
tol = 0.00001
while not stable:
    newpower = {}
    stable = True
    for team in power:
        newpower[team] = len(wins[team])*1.0
        for other in wins[team]:
            newpower[team] += power[other]
        for other in loss[team]:
            newpower[team] += power[other]
        newpower[team]/=len(wins[team])+len(loss[team])
    power = newpower

ranks = sorted([(power[i],i) for i in wins if len(wins[i])+len(loss[i])>4])

outp = open("ranks/%s/%s_rank_week%s.txt"%(METHOD,METHOD, WEEKNUM),"w")
for i,j in enumerate(reversed(ranks)):
    outp.write("%s. %s (%s-%s)\n" % (i+1, names[j[1]],len(wins[j[1]]), len(loss[j[1]])))
outp.close()