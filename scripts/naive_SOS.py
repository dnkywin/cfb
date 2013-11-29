#!/usr/bin/python
import math
from parsed_game_reader import games, wins, loss, WEEKNUM, print_rank
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

print_rank(ranks)