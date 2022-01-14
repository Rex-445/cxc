from champion import Champion

#Characters
from Ken import *
from Ryu import *
from Bison import *
from Cammy import *
from Akuma import *
from monk import *
from FeiLong import *
from ChunLi import *
from AntiRyu import *


def Char_Ryu(pos=[0,0], outfit=""):
    ryu = Ryu("Ryu")
    ryu.__init__self__(10, 10, 150, 100, ryu.defualt[0]+outfit+".png")
    ryu.__init__self__(10, 4, 150, 150, ryu.defualt[1]+outfit+".png")
    ryu.__init__self__(10, 10, 150, 150, "sprites/Ryu/Ryu_glow.png")
    ryu.__init__self__(row=2, col=4, width=150, height=150, img="sprites/burn.png")
    ryu.__init__aura__(10, 10, 150, 100, ryu.defualt[0] + "_Aura.png")
    ryu.__init__aura__(10, 1, 150, 150, ryu.defualt[0] + "_Aura2.png")
    return ryu

def Char_AntiRyu(pos=[0,0], outfit=""):
    antiRyu = AntiRyu("Anti-Ryu")
    antiRyu.__init__self__(10, 10, 150, 100, antiRyu.defualt[0]+outfit+".png")
    antiRyu.__init__self__(10, 4, 150, 150, antiRyu.defualt[1]+outfit+".png")
    antiRyu.__init__self__(row=2, col=4, width=150, height=150, img="sprites/burn.png")
    return antiRyu

def Char_Ken(pos=[0,0], outfit=""):
    ken = Ken("Ken")
    ken.__init__self__(10, 10, 150, 100, ken.defualt[0]+outfit+".png")
    ken.__init__self__(10, 2, 150, 150, ken.defualt[1]+outfit+".png")
    ken.__init__self__(row=2, col=4, width=150, height=150, img="sprites/burn.png")
    return ken

def Char_Bison(pos=[0,0], outfit=""):
    bison = Bison("M.Bison")
    bison.__init__self__(10, 10, 150, 100, bison.defualt[0]+outfit+".png")
    bison.__init__self__(10, 4, 150, 100, bison.defualt[1]+outfit+".png")
    bison.__init__self__(row=2, col=4, width=150, height=150, img="sprites/burn.png")
    return bison

def Char_Cammy(pos=[0,0], outfit=""):
    cammy = Cammy("Cammy")
    cammy.__init__self__(10, 10, 150, 100, cammy.defualt[0]+outfit+".png")
    cammy.__init__self__(10, 5, 150, 100, cammy.defualt[1]+outfit+".png")
    cammy.__init__self__(row=2, col=4, width=150, height=150, img="sprites/burn.png")
    return cammy

def Char_FeiLong(pos=[0,0], outfit=""):
    feiLong = FeiLong("Fei'Long")
    feiLong.__init__self__(10, 10, 150, 150, feiLong.defualt[0]+outfit+".png")
    feiLong.__init__self__(10, 10, 150, 150, feiLong.defualt[1]+outfit+".png")
    feiLong.__init__self__(row=2, col=4, width=150, height=150, img="sprites/burn.png")
    feiLong.__init__aura__(10, 10, 150, 150, feiLong.defualt[0] + "_Glow.png")
    feiLong.__init__aura__(10, 10, 150, 150, feiLong.defualt[0] + "_Glow2.png")
    return feiLong

def Char_ChunLi(pos=[0,0], outfit=""):
    chunLi = ChunLi("Chun'Li")
    chunLi.__init__self__(10, 10, 150, 150, chunLi.defualt[0]+outfit+".png")
    chunLi.__init__self__(10, 10, 150, 150, chunLi.defualt[1]+outfit+".png")
    chunLi.__init__self__(row=2, col=4, width=150, height=150, img="sprites/burn.png")
    return chunLi

def Char_Akuma(pos=[0,0], outfit=""):
    akuma = Akuma("Akuma")
    akuma.__init__self__(10, 10, 150, 100, akuma.defualt[0]+".png")
    akuma.__init__self__(10, 10, 150, 150, akuma.defualt[1]+".png")
    akuma.__init__self__(row=2, col=4, width=150, height=150, img="sprites/burn.png")
    return akuma

#Supports
def Sup_Monk(pos=[0,0], outfit=""):
    monk = Monk("Monk")
    monk.__init__self__(10, 7, 80, 80, monk.defualt[0]+outfit+".png")
    monk.__init__self__(10, 7, 80, 80, monk.defualt[1]+outfit+".png")
    monk.__init__self__(row=2, col=4, width=150, height=150, img="sprites/burn.png")
    return monk

def Check_Champs(champ, pos=[0,100], skin=""):
    if champ == "Ryu":
        return Char_Ryu(pos=pos, outfit=skin)
    if champ == "Anti-Ryu":
        return Char_AntiRyu(pos=pos, outfit=skin)
    if champ == "Ken":
        return Char_Ken(pos=pos, outfit=skin)
    if champ == "M.Bison":
        return Char_Bison(pos=pos, outfit=skin)
    if champ == "Cammy":
        return Char_Cammy(pos=pos, outfit=skin)
    if champ == "Akuma":
        return Char_Akuma(pos=pos, outfit=skin)
    if champ == "Monk":
        return Sup_Monk(pos=pos, outfit=skin)
    if champ == "Fei'Long":
        return Char_FeiLong(pos=pos, outfit=skin)
    if champ == "Chun'Li":
        return Char_ChunLi(pos=pos, outfit=skin)
    
def Craft_Champions(champ1, champ2):
    player1 = Check_Champs(champ1, skin="")
    if champ1 == champ2:
        player2 = Check_Champs(champ2, skin="Outfit")
    else:
        player2 = Check_Champs(champ2, skin="")

    return player1, player2

