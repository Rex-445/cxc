import sys, os






def ResetPlayerData():
    with open("data/Player.txt", 'w+') as f:
            #Player Name
            f.write("PlayerName: " + "Defualt" + "\n")
            #Player Name
            f.write("Level: " + "1" + "\n")
            #Player Name
            f.write("Icon: " + "Ryu_Head" + "\n")
            #Player Name
            f.write("Favourite Champion: " + "None" + "\n")
            #Player Name
            f.write("Boarder: " + "Boarder1" + "\n")

            f.close()

ResetPlayerData()

    
f = open("data/Player.txt",'r')
data = f.read()
f.close()
data = data.split('\n')
data2 = []
for row in data:
    data2.append(row)
    
player_name = data2[0].split(':')[1].replace(" ", "")
level = data2[1].split(':')[1].replace(" ", "")
icon = data2[2].split(':')[1].replace(" ", "")
fav_champ = data2[3].split(':')[1].replace(" ", "")
boarder = data2[4].split(':')[1].replace(" ", "")

def SavePlayerData(name="Defualt", level=1, icon="Ryu_Head", fav_champ="None", boarder="Boarder2"):
    global player_name
    player_name = name
    level = level
    icon = icon
    fav_champ = fav_champ
    boarder = boarder
    
    with open("data/Player.txt", 'w+') as f:
            #Player Name
            f.write("PlayerName: " + name + "\n")
            #Player Name
            f.write("Level: " + str(level) + "\n")
            #Player Name
            f.write("Icon: " + icon + "\n")
            #Player Name
            f.write("Favourite Champion: " + fav_champ + "\n")
            #Player Name
            f.write("Boarder: " + boarder + "\n")

            f.close()
            





