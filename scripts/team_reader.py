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