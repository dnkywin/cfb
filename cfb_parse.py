WEEKNUM = 13
inp = open("team-game-statistics-week%s.csv" % (WEEKNUM,),"r")
data = inp.read()
inp.close()

TEAMID,GAMEID,PTSID = 0,1,35

games = {}

for line in data.split('\n')[1:]:
    if line:
        datum = line.split(',')
        teamid, gameid, pts = int(datum[TEAMID]),datum[GAMEID],int(datum[PTSID])
        if gameid not in games:
            games[gameid] = []
        games[gameid]+=[teamid,pts]

#games["1320074920131107"] = [IDs["Oregon"], 10, IDs["Stanford"], 33]
#games["1283902183191107"] = [IDs["Oklahoma"], 10, IDs["Baylor"], 33]
#games["0796002820130914"][3] = 33
outp = open("games-parsed-week%s.txt"%(WEEKNUM,),"w")

for game in games:
    res = games[game]
    outp.write("%s %s %s %s %s\n" % ((game,)+tuple(res)))
outp.close()