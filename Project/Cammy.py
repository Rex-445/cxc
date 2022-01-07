import sys, pickle, pyglet, random, time, math
from ball import *
from champion import Champion


def preload_image(image):
    img = pyglet.image.load("sprites/" + image + ".png")
    return img

class Cammy(Champion):
    def __init__(self, name):
        super().__init__(name)
        self.defualtSpeed = .3
        self.frameSpeed = .3
        self.oldSpeed = 0
        self.hitBoxOffset = -40
        self.x = 0
        self.gameStart = True
        self.slideDirection = 0 

        self.pos = [0,0,0]
        
        self.defualt2 = [name+"_mirror", name+"_2_mirror"]

        self.width, self.height = (79, 79)
        self.hitBox = [0,0, 30,30]
        self.body = [30,0,50,85]
        self.shadowOffset = [50,-5]
        self.alignmentOffset = [20,0]
        

        #Vairations
        self.variation_images = [pyglet.sprite.Sprite(preload_image("Cammy/variation_A")), pyglet.sprite.Sprite(preload_image("Cammy/variation_B"))]
        self.variation_names = ["Renegade", "Commando"]
        self.variation_description = [self.variation_names[0] + ": Cammy gains 'Brutal Strike' crippling her opponents by reducing their damage dealt by a certain amount",
                                      self.variation_names[1] + ": Cammy has access to multiple command grabs. You can style with this by slipping them into a combo"]

        #Biography
        self.main_description = ["Cammy, uses her strong body and flexibility to counter and supress her opponents.",
                            "She has multiple skills that mixes up with other of her abilities. She also has a ",
                            "hand full of command grabs and can parry opponents easily"]
        
        self.description = ""

        for d in self.main_description:
            self.description += d
        
        #Dialogues
        self.talkTo = []
        self.respondTo = []

        #Projectiles
        self.spawnFrame = 0
        self.balls = []
        self.vfx = []

        #Dialogues
        self.talkTo = [["Ken", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"], ["Ken", "B", "Audio/Champs/"+self.name+"/Dialogues/B.wav"],
                       ["Ken", "H", "Audio/Champs/"+self.name+"/Dialogues/H.wav"], ["M.Bison", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"],
                       ["M.Bison", "G", "Audio/Champs/"+self.name+"/Dialogues/G.wav"], ["Ryu", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"],
                       ["Ryu", "B", "Audio/Champs/"+self.name+"/Dialogues/B.wav"], ["Cammy", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"],
                       ["Ryu", "D", "Audio/Champs/"+self.name+"/Dialogues/D.wav"], ["Akuma", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"],
                       ["Anti-Ryu", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"], ["Anti-Ryu", "H", "Audio/Champs/"+self.name+"/Dialogues/H.wav"],
                       ["Anti-Ryu", "I", "Audio/Champs/"+self.name+"/Dialogues/I.wav"]]
        
        self.respondTo = [["Ryu", "B", "Audio/Champs/"+self.name+"/Dialogues/H.wav"], ["Ryu", "F", "Audio/Champs/"+self.name+"/Dialogues/D.wav"],
                          ["Ken", "B", "Audio/Champs/"+self.name+"/Dialogues/I.wav"], ["Ken", "B", "Audio/Champs/"+self.name+"/Dialogues/H.wav"],
                          ["Ken", "B", "Audio/Champs/"+self.name+"/Dialogues/G.wav"], ["Ken", "C", "Audio/Champs/"+self.name+"/Dialogues/D.wav"],
                          ["Ken", "C", "Audio/Champs/"+self.name+"/Dialogues/F.wav"], ["Ken", "D", "Audio/Champs/"+self.name+"/Dialogues/H.wav"],
                          ["Ken", "D", "Audio/Champs/"+self.name+"/Dialogues/G.wav"], ["Ken", "D", "Audio/Champs/"+self.name+"/Dialogues/D.wav"],
                          ["M.Bison", "A", "Audio/Champs/"+self.name+"/Dialogues/D.wav"], ["M.Bison", "A", "Audio/Champs/"+self.name+"/Dialogues/E.wav"],
                          ["M.Bison", "A", "Audio/Champs/"+self.name+"/Dialogues/L.wav"], ["M.Bison", "A", "Audio/Champs/"+self.name+"/Dialogues/C.wav"],
                          ["M.Bison", "B", "Audio/Champs/"+self.name+"/Dialogues/E.wav"], ["M.Bison", "B", "Audio/Champs/"+self.name+"/Dialogues/J.wav"],
                          ["M.Bison", "B", "Audio/Champs/"+self.name+"/Dialogues/E.wav"], ["M.Bison", "G", "Audio/Champs/"+self.name+"/Dialogues/D.wav"],
                          ["M.Bison", "J", "Audio/Champs/"+self.name+"/Dialogues/A.wav"], ["M.Bison", "J", "Audio/Champs/"+self.name+"/Dialogues/C.wav"],
                          ["M.Bison", "J", "Audio/Champs/"+self.name+"/Dialogues/K.wav"], ["M.Bison", "M", "Audio/Champs/"+self.name+"/Dialogues/D.wav"],
                          ["M.Bison", "M", "Audio/Champs/"+self.name+"/Dialogues/M.wav"], ["M.Bison", "O", "Audio/Champs/"+self.name+"/Dialogues/O.wav"],
                          ["M.Bison", "O", "Audio/Champs/"+self.name+"/Dialogues/L.wav"], ["Cammy", "A", "Audio/Champs/"+self.name+"/Dialogues/B.wav"],
                          ["Cammy", "A", "Audio/Champs/"+self.name+"/Dialogues/G.wav"], ["Anti-Ryu", "A", "Audio/Champs/"+self.name+"/Dialogues/D.wav"],
                          ["Anti-Ryu", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"], ["Anti-Ryu", "H", "Audio/Champs/"+self.name+"/Dialogues/J.wav"],
                          ["Anti-Ryu", "H", "Audio/Champs/"+self.name+"/Dialogues/L.wav"], ["Anti-Ryu", "H", "Audio/Champs/"+self.name+"/Dialogues/O.wav"],
                          ["Anti-Ryu", "H", "Audio/Champs/"+self.name+"/Dialogues/D.wav"], ["Anti-Ryu", "G", "Audio/Champs/"+self.name+"/Dialogues/L.wav"],
                          ["Anti-Ryu", "H", "Audio/Champs/"+self.name+"/Dialogues/P.wav"]]

        #Combination
        self.skill = [["bfA", "Spin Knuckle"], ["bfSK", "Cannon Drill"], ["dbK", "Leg Suplex"], ["dfSK", "Shun' Po"],
                      ["fbSK", "Super Cannon Drill"]]

        
        #Audio
        self.voiceFrame = 0
        self.sound = pyglet.media.load("Audio/Champs/Ryu/dragon_ball.wav", streaming=False)
        self.voiceCD = 0
        self.wins= [["First_Wins", ["Audio/Champs/"+self.name+"/Wins/first_win.wav"]],["End_Game", ["Audio/Champs/"+self.name+"/Wins/end_gameA.wav",
                                                                                           "Audio/Champs/"+self.name+"/Wins/end_gameB.wav",
                                                                                           "Audio/Champs/"+self.name+"/Wins/end_gameC.wav",
                                                                                           "Audio/Champs/"+self.name+"/Wins/end_gameD.wav"]],
                    ["Low_Health_Win", ["Audio/Champs/Ryu/Wins/low_health_win.wav"]]]
        
        self.championTaunt = {"M.Bison": self.LoadAllFilesFromDirectory("Audio/Champs/"+self.name+"/Wins/M.Bison"),

                              "Ken": self.LoadAllFilesFromDirectory("Audio/Champs/"+self.name+"/Wins/Ken")}
        

        ################ Animations ###############
        #Standing
        self.frames1 = [0, 0, 1, 2, 3, 3, 4]
        #Walking
        self.frames2 = [5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10]
        #Weak Punch
        self.frames3 = [35, 36, 36, 35]
        #Medium Punch
        self.frames4 = [35, 37, 37, 37, 35]
        #Strong Punch A
        self.frames15 = [40, 40, 38, 38, 38, 39]
        #Strong Punch B
        self.frames19 = [40, 40, 41]
        #Strong Punch C
        self.frames26 = [42, 43, 43, 44]
        #Crouch
        self.frames7 = [16]
        #Crouch Weak Punch
        self.frames8 = [17, 18, 18, 17]
        #Crouch Medium Punch
        self.frames9 = [20, 21, 21, 21, 22, 22, 22, 22, 23, 23]
        #Jump
        self.frames10 = [12, 13, 13, 13, 13, 13, 13, 13, 14]
        #Land
        self.frames11 = [15, 16, 16]
        #Getting Hit
        self.frames12 = [123, 123, 123, 123, 123]
        #Getting Hit
        self.frames13 = [127, 127, 127, 127, 127]
        #Getting Hit
        self.frames14 = [128, 128, 128, 128, 128, 128, 128, 128]
        #Falling Bounce
        self.frames16 = [132, 132, 132, 133]
        #Lying
        self.frames17 = [134, 134, 134, 134, 134, 134, 134, 134, 134, 134]
        #Back Spring
        self.frames17B = [134, 134, 134, 134, 109, 109, 114, 114, 115, 115, 116, 116, 117, 117]
        #Weak Kick
        self.frames20 = [49, 50, 50]
        #Medium Kick
        self.frames21 = [51, 52, 52, 53, 53, 53]
        #Crouch Weak Kick
        self.frames22 = [24, 25, 25, 24]
        #Crouch Medium Kick 
        self.frames23 = [30, 30, 31, 32, 33, 34, 30, 30]
        #Cannon Drill(Start)
        self.frames24 = [79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 80, 81]
        #Cannon Drill(Mid)
        self.frames25A = [82, 83, 84, 85, 86, 87]
        #Cannon Drill(End)
        self.frames25B = [88, 89, 89]
        self.frames25C = [93, 93, 94, 94, 95, 95, 95]
        self.freezeInAir = False
        self.kickLoop = 5
        #Spin Knuckle(Start)
        self.frames27 = [96, 96, 97, 97, 98]
        #Spin Knuckle(Air)
        self.frames40 = [98, 99, 98, 99, 98, 99]
        #Spin Knuckle(End)
        self.frames41 = [100, 101, 102, 102, 103]
        #Command Grab (Start)
        self.grabChain = 19.1
        self.frames42 = [42, 43, 43, 44, 44, 44]
        #Command Grab A(Start)
        self.frames43 = [15, 15, 15, 118]
        #Command Grab A(Caught)
        self.frames44 = [118, 119, 119, 120, 120, 121, 121]


        
        #Blocking Frames
        self.frames29 = [45, 46, 47, 48]
        self.frames29B = [61, 61, 61, 61, 61, 61, 61, 62, 64, 64, 64]
        self.blockWait = 0

        
        #Win - To - Sub Animation Win
        self.frames30 = [96, 96, 96, 96]
        #Sub Animation Win
        self.frames31 = [136, 137, 138, 138, 138, 139]
        #Sub Animation Win 2A
        self.frames32 = [75, 76, 77, 78]
        #Sub Animation Win 2A (Loop)
        self.frames33 = [41]
        
        #Brutal Strike
        self.frames34 = [110, 110, 110, 110, 110, 110, 110, 110, 110, 111, 112, 112, 112, 113]
        self.frames34_forcesX = [0, 0, 0, 0, 0, 0, 5, 0, 0, 4, 0, 5, 5, 4]
        self.frames34_forcesY = [0, 0, 0, 0, 0, 0, 16, 16, 16, 8, 16, 0, 8, 0]

        #Start Game (Dialogues)
        #Respond from taunt
        self.frames35 = [0]
        #Idle Response
        self.frames35B = [143, 143, 143, 144, 144, 144, 143, 143, 143, 144,144, 144, 143, 143, 143,
                          144, 144, 144, 143, 143, 143, 144, 144, 144, 143, 143, 143]
        #Taunt
        self.frames36 = [138, 138, 137, 137, 136, 136, 135, 135]
        #Taunt IDLE
        self.frames36B = [138, 138, 138, 138, 138, 138, 138, 138, 138, 138]
        
        #Throw (Catching)
        self.frames37 = [43, 44, 44, 44]
        #Throw (Caught)
        self.frames38 = [44, 104, 104, 104, 105, 105, 105, 106, 106, 106, 107, 107, 107, 108]
        self.catchFrames = [23, 23.3, 23.3, 23.3, 23.3, 23.3, 23.3, 23.8, 23.8, 23.8, 23.8, 23.8, 23.8, 23.8]
        #Throw (Getting Caught)
        self.frames39 = [128, 127, 126, 132]

        #Shun' Po (Start)
        self.frames45 = [61, 62, 63, 64, 64, 64, 63, 62, 61]
        #Shun' Po -> Air Attack (Leap) -> Punch
        self.frames45B = [110, 110, 110, 122]
        #Shun' Po -> Air Attack (First) -> Punch
        self.frames45C = [67, 68, 68, 69, 69]
        #Shun' Po -> Air Attack (Second) -> Punch
        self.frames45D = [70, 71, 71, 72, 72, 72, 67]

        #Shun' Po
        #Shun' Po -> Air Attack (First) -> Kick
        self.frames46 = [75, 75, 76, 76, 77, 77, 78, 78, 78]
        #Shun' Po -> Air Attack (Second) -> Kick
        self.frames46B = [73, 74, 74, 75, 75, 13]

        #character frames
        self.cell = []
        self.flip = []
        self.targetCell = self.cell
        self.targetFrame = self.frames1
        self.row = 0
        self.col = 0
        self.sounds = ["sounds/020.wav"]
        self.sndTimer = 1
        self.frame = 0
        self.direction = 1
        self.dvx = 0
        self.dvy = 0
        
    def _jump(self):
        if not self.jump:
            self.jump = True
            self.vel[1] = self.jumpHeight
            self.frame = 0
            self.Play("Audio/jump.wav")
            self.action = -1
            self.targetFrame = self.frames10
            
    def _height(self):
        if not self.jump:
            self.jump = True
            self.vel[1] = self.jumpHeight

    def _skill(self, skill):
        self.mixup = ""
        #Leg Suplex
        if skill == "Leg Suplex" and self.stamina > 40:
            if self.state == "Grounded" or self.state == "Crouch":
                self.stamina -= 40
                self.state = "Skill"
                self.action = 19
                self.frame = 0
                self.grabChain = 19.1

        #Cannon Drill
        if skill == "Cannon Drill" or skill == "Super Cannon Drill":
            if skill == "Cannon Drill" and self.rageBar >= 200:
                if self.state == "Grounded" or self.state == "Crouch" or self.state == "BlockHit":
                    self.rageBar -= 200
                    self.state = "Skill"
                    self.frame = 0
                    self.action = 17     
                    self.invincible = True 
                    self.Play("Audio/Champs/Ryu/special.wav")
                    choice = random.choice(["Audio/Champs/Cammy/cannon_drillA.wav", "Audio/Champs/Cammy/cannon_drillB.wav"])
                    self.PlayVoice(choice)
                    self.superSkill = True
                    self.vfx.append(Ball(pos=(self.pos[0] - 20, self.pos[1] - 20), name="VFX", loop=False, destroy=3, width=225, height=225,
                                          speed=.2, img="sprites/special.png", row=4, col=2))
            if skill == "Super Cannon Drill" and self.rageBar >= 0:
                if self.state == "Grounded" or self.state == "Crouch" or self.state == "BlockHit":
                    self.rageBar -= 200
                    self.state = "Skill"
                    self.frame = 0
                    self.action = 31
                    self.invincible = True
                    self.Play("Audio/Champs/Ryu/special.wav")
                    choice = random.choice(["Audio/Champs/Cammy/cannon_drillA.wav", "Audio/Champs/Cammy/cannon_drillB.wav"])
                    self.PlayVoice(choice)
                    self.superSkill = True
                    self.vfx.append(Ball(pos=(self.pos[0] - 20, self.pos[1] - 20), name="VFX", loop=False, destroy=3, width=225, height=225,
                                          speed=.2, img="sprites/special.png", row=4, col=2))
                
        #Spin Knuckle
        if skill == "Spin Knuckle" and self.stamina > 50:                
            if self.state == "Grounded" or self.state == "Crouch":
                self.stamina -= 50
                self.state = "Skill"      
                self.frame = 0
                self.action = 12
                
        #Shun' Po
        if skill == "Shun' Po" and self.stamina > 40 and self.targetVariation == self.variation_names[1]:                
            if self.state == "Grounded" or self.state == "Crouch":
                self.stamina -= 40
                self.state = "Skill"      
                self.frame = 0
                self.action = 30

    #Audio
    def Play(self, file):
        self.sound = pyglet.media.load(file, streaming=False)
        self.sound.play()

    def Win(self):
        self.action = 20
        
    def Update_Alignment(self):
        #Update Alignment
        self.x = 0
        self.y = 0
        self.attacking_actions = [2, 2.5, 3, 3.5, 9, 10, 10.5, 11, 11.5, 12, 17.3, 12.5, 13, 13.5, 14, 14.5, 19, 21, 22, 30, 31]
        try:
            if self.direction == 1:
                self.x = self.pos[0] + self.alignX[self.targetFrame[int(self.frame)]] + -5
                self.y = self.pos[1] + self.alignY[self.targetFrame[int(self.frame)]]
                
            if self.direction == -1:
                self.x = self.pos[0] - self.alignX[self.targetFrame[int(self.frame)]] + 140
                self.y = self.pos[1] + self.alignY[self.targetFrame[int(self.frame)]]
        except:
            pass
        
        if self.action not in self.attacking_actions:
            self.hitBox[0] = 10000
            self.hitBox[1] = 10000
         
    def Update(self):
        if self.opponent != None:
            if self.oldSpeed == 0:
                self.oldSpeed = self.opponent.frameSpeed
                
        if self.pause <= 0:
            self.frame += self.frameSpeed
            self.hitCD -= .09
            self.key_combo_time += .1
            if self.key_combo_time > 5:
                self.key_combo = ""
                
            self.UpdateActions()

            self.Check_Combo()

            #Updating Combos
            if self.voiceCD > 0:
                self.voiceCD -= .1

            #Falling and Jumping
            self.UpdatePhysics()

            if self.talking:
                if self.gameStart:
                    self.gameStart = False
                    self.action = -4
            if self.talking == False:
                if self.gameStart:
                    self.gameStart = False
                    self.action = -4.5

            #Animations
            #Idle
            if self.action == 0:
                self.targetFrame = self.frames1
                if self.frame >= len(self.frames1) - 1:
                    self.frame = 0

            #Walk
            if self.action == 1:
                self.targetFrame = self.frames2
                if self.frame >= len(self.frames2) - 1:
                    self.frame = 0

            #Weak Punch
            if self.action == 2:
                self.targetFrame = self.frames3
                if self.frame >= len(self.frames3) - 1:
                    self.frame = 0
                    self.action = 0
                    
            #Weak Punch Crouch
            if self.action == 2.5:
                self.targetFrame = self.frames8
                if self.frame >= len(self.frames8) - 1:
                    self.frame = 0
                    self.action = 0
                    self.state = "Grounded"

            #Medium Punch
            if self.action == 3:
                self.targetFrame = self.frames4
                if self.frame >= len(self.frames4) - 1:
                    self.frame = 0
                    self.action = 0
                    
            #Medium Punch Crouch
            if self.action == 3.5:
                self.targetFrame = self.frames9
                if self.frame >= len(self.frames9) - 1:
                    self.frame = 0
                    self.action = 0
                    self.state = "Grounded"
                    
            #Crouch
            if self.action == 4:
                self.targetFrame = self.frames7
                self.force = [0,0]
                if self.frame >= len(self.frames7) - 1:
                    self.frame = 0
                    
            #Land from Jump
            if self.action == 5:
                self.targetFrame = self.frames11
                self.velocity = 0
                self.state = "Land"
                if self.frame <= 1 and self.voiceFrame != 1:
                    self.voiceFrame = 1
                    self.Play("Audio/land.wav")
                if self.frame >= len(self.frames11) - 1:
                    self.action = 0
                    self.voiceFrame = 0
                    self.state = "Grounded"
                    self.superSkill = False
                    
            #Getting Hit A
            if self.action == 6:
                self.targetFrame = self.frames12
                if self.frame >= len(self.frames12) - 1:
                    self.action = 0
                    self.state = "Grounded"
                    
            #Getting Hit B
            if self.action == 6.3:
                self.targetFrame = self.frames13
                if self.frame >= len(self.frames13) - 1:
                    self.action = 0
                    self.state = "Grounded"
                    
            #Getting Hit C
            if self.action == 6.5:
                self.targetFrame = self.frames14
                if self.frame >= len(self.frames14) - 1:
                    self.action = 0
                    self.state = "Grounded"

            #Breaker
            if self.action == 6.7:
                self.targetFrame = self.frames29B
                if self.frame >= len(self.frames29B) - 1:
                    self.action = 0
                    self.state = "Grounded"
                    self.Play("Audio/Champs/Cammy/breaker.wav")
                    self.opponent.Get_Hit(attacker=self, damage=0, force=[12,5], typeHit="Ground")
                    self.frame = 0
                    self.superSkill = False
                    self.invincible = False
                    
            #Falling
            if self.action == 7:
                self.targetFrame = self.frames16
                if self.frame >= len(self.frames16) - 1:
                    self.frame = 0
                    
            #Back Spring
            if self.action == 7.5:
                self.targetFrame = self.frames17B
                self.velocity = 0
                self.state = "Lying"
                if self.frame >= len(self.frames17B) - 1:
                    self.frame = 0
                    self.action = 0
                    self.state = "Grounded"
                        
            #Lying
            if self.action == 7.9:
                self.targetFrame = self.frames17
                self.velocity = 0
                self.state = "Lying"
                self.vel = [0,0]
                if self.hitCombo > 0:
                    self.comboEnd = True
                    self.damageDealt = 0
                if self.frame >= len(self.frames17) - 1:
                    self.frame = 0
                    if self.health > 0:
                        self.action = 5
                        if self.backSpring:
                            self.action = 7.5
                            self.backSpring = False
                    else:
                        self.alive = False

            #Weak Kick
            if self.action == 10:
                self.targetFrame = self.frames20
                if self.frame >= len(self.frames20) - 1:
                    self.frame = 0
                    self.action = 0
                    
            #Weak Kick Crouch
            if self.action == 10.5:
                self.targetFrame = self.frames22
                if self.frame >= len(self.frames22) - 1:
                    self.frame = 0
                    self.action = 0
                    self.state = "Grounded"

            #Medium Kick
            if self.action == 11:
                self.targetFrame = self.frames21
                if self.frame >= len(self.frames21) - 1:
                    self.frame = 0
                    self.action = 0
                    
            #Medium Kick Crouch
            if self.action == 11.5:
                self.targetFrame = self.frames23
                if self.frame >= len(self.frames23) - 1:
                    self.frame = 0
                    self.velocity = 0
                    self.state = "Grounded"
                    self.action = 0
                    self.slideDirection = 0
                    self.force = [0,0]
                    
            #Spin Knuckle(Start)
            if self.action == 12:
                self.targetFrame = self.frames27
                if self.frame >= len(self.frames27) - 1:
                    self.Play("Audio/jump.wav")
                    self.action = 12.5
                    self.jumpHeight = 6
                    self._height()
                    self.frame = 0
                
            #Spin Knuckle(Mid)
            if self.action == 12.5:
                if self.frame < 1 and self.voiceFrame != -1:
                    self.invincible = True
                    choice = random.choice(["Audio/Champs/Cammy/spin_knuckle.wav", "Audio/Champs/Cammy/Grunt/51e.wav",
                                            "Audio/Champs/Cammy/Grunt/52e.wav"])
                    self.PlayVoice(choice)
                    self.voiceFrame = -1
                self.force = [7.2,5]
                self.damage = 30
                self.vel[0] = -3
                self.targetFrame = self.frames40
                if self.frame >= len(self.frames40) - 1:
                    self.voiceFrame = 0
                    self.frame = 0
                    
            #Spin Knuckle(End)
            if self.action == 12.8:
                self.targetFrame = self.frames41
                if self.frame < 1 and self.voiceFrame != -1:
                    self.Play("Audio/land.wav")
                    self.voiceFrame = -1
                if self.frame >= len(self.frames41) - 1:
                    self.velocity = 0
                    self.action = 0
                    self.voiceFrame = 0
                    self.force = [0,0]
                    self.state = "Grounded"
                    self.invincible = False
                    
            #Stand Block (Normal)
            if self.action == 13:
                self.targetFrame = self.frames29
                self.frame = 0
                self.blockWait += 1
                if self.blockWait >= 20:
                    self.action = 0
                    self.blockWait = 0
                    self.blockRight = False
                    self.blockLeft = False
                    if self.moveRight:
                        self.right = True
                    if self.moveLeft:
                        self.left = True
                        
            #Stand Block (Hit)
            if self.action == 13.5:
                self.targetFrame = self.frames29
                self.frame = 1
                self.blockWait += 1
                self.state = "BlockHit"
                if self.blockWait >= 10:
                    self.action = 13
                    self.blockWait = 0
                    self.state = "Grounded"
                    
            #Crouch Block (Normal)
            if self.action == 14:
                self.targetFrame = self.frames29
                self.frame = 2
                self.blockWait += 1
                self.state = "Crouch"
                if self.blockWait >= 10:
                    self.action = 4
                    self.blockWait = 0
                    self.blockRight = False
                    self.blockLeft = False
                    if self.moveRight:
                        self.right = True
                    if self.moveLeft:
                        self.left = True
                    
            #Crouch Block (Hit)
            if self.action == 14.5:
                self.targetFrame = self.frames29
                self.frame = 3
                self.blockWait += 1
                self.state = "CrouchBlockHit"
                if self.blockWait >= 20:
                    self.action = 14
                    self.blockWait = 0
                    
            #Cannon Drill(Start)
            if self.action == 17:
                self.targetFrame = self.frames24
                if self.frame >= len(self.frames24) - 1:
                    self.vel[0] = -5
                    self.frame = 0
                    self.jumpHeight = 4
                    self._height()  
                    choice = random.choice(["Audio/Champs/Cammy/cannon_drill_A.wav", "Audio/Champs/Cammy/cannon_drill_B.wav"])
                    self.PlayVoice(choice)
                    self.action = 17.3
                    self.superSkill = False
                    
            #Cannon Drill(Mid)
            if self.action == 17.3:
                self.force = [6.3,4.7]
                self.freezeInAir = True
                self.targetFrame = self.frames25A
                if self.targetFrame[int(self.frame)] == 82 and self.voiceFrame != 82:
                    self.Play("Audio/wiff.wav")
                    self.voiceFrame = 82
                    self.invincible = False
                if self.frame >= len(self.frames25) - 1:
                    if self.kickLoop > 0:
                        self.voiceFrame = 0
                        self.kickLoop -= 1
                        self.frame = 0
                    else:
                        self.kickLoop = 6
                        self.force = [0,0]
                        self.action = 17.5

                #End Cannon Drill if opponent is blocking
                blockStates = [13.5, 14.5]
                if self.opponent.action in blockStates:
                    self.freezeInAir = False
                    self.frame = 0
                    self.action = 17.8
                    self.targetFrame = self.frames25C
                    self.kickLoop = 6
                    self.vel[0] = 8
                    self.vel[1] = 9
                    
            #Cannon Drill(End)
            if self.action == 17.5:
                self.freezeInAir = False
                self.targetFrame = self.frames25B
                if self.frame >= len(self.frames25B) - 1:
                    self.frame = 0
                    self.action = -1


            #Cannon Drill Cancel
            if self.action == 17.8:
                self.freezeInAir = False
                self.targetFrame = self.frames25C
                if self.frame >= len(self.frames25C) - 1:
                    self.frame = 0
                    self.action = -1
                
                    
                    
            #Command Grab - Main (Start)
            if self.action == 19:
                self.targetFrame = self.frames42
                if self.voiceFrame != self.frame and self.frame >= len(self.frames42) - 2:
                    self.voiceFrame = self.frame
                    self.Play("Audio/wiff.wav")
                self.force = [5,0]
                if self.frame >= len(self.frames42) - 1:
                    self.frame = 0
                    self.action = -100
                    hits = [6, 6.3, 6.5]
                    if self.opponent.hitCD < 1:
                        #If the opponent is airborne
                        if self.opponent.pos[1] > self.ground:
                            self.opponent.pos[1] = self.ground
                            self.opponent.state = "Grounded"
                            self.opponent.action = random.choice(hits)
                            self.opponent.frame = 0
                            self.opponent.fall = False
                            self.opponent.jump == False
                            self.opponent.vel[1] = 0

                        #If it hits
                        if self.opponent.action in hits:
                            self.action = self.grabChain
                            self.targetGrabbed = self.opponent
                            self.grabChain = 19.2
                            self.targetGrabbed.frameSpeed = .05
                            self.targetGrabbed.toGrab = True
                    
            #Command Grab - A (Start)
            if self.action == 19.1:
                self.targetFrame = self.frames43
                if self.frame >= len(self.frames43) - 1:
                    if self.voiceFrame != -1:
                        self.voiceFrame = -1
                        self.Play("Audio/jump.wav")
                    self.jumpHeight = 3
                    self.gravity = .3
                    self.vel[0] = -4
                    self._height()
                    self.frame = len(self.frames43) - 1
                    hits = [6, 6.3, 6.5, 13.5, 14.5]
                    
            #Command Grab A (Caught)
            if self.action == 19.2:
                self.isGrabbing  = True
                self.targetFrame = self.frames44
                catchFrames = [23, 23, 23.3, 23.3, 23.3, 23.8, 23.8]
                self.opponent.action = catchFrames[int(self.frame)]
                self.force = [6 * self.direction,3]
                self.vel[0] = 2 * self.direction
                choice = random.choice(["Audio/Champs/Cammy/Grunt/50e.wav", "Audio/Champs/Cammy/Grunt/49e.wav", "Audio/Champs/Cammy/Grunt/48e.wav"])
                if self.targetFrame[int(self.frame)] == 120 and self.voiceFrame != self.targetFrame[int(self.frame)]:
                    self.voiceFrame = self.targetFrame[int(self.frame)]
                    self.PlayVoice(choice)
                if self.frame >= len(self.frames44) - 1:
                    self.targetGrabbed.frameSpeed = self.oldSpeed
                    self.targetGrabbed.isGrabbed = False
                    self.targetGrabbed.bounce = 1
                    self.targetGrabbed.toGrab = False
                    self.targetGrabbed.Get_Hit(attacker=self, damage=self.damage, force=self.force, typeHit="Ground")
                    self.targetGrabbed = None
                    self.isGrabbing = False
                    self.frame = len(self.frames44) - 1
                    self.action = 7.5
                    self.jump = True
                    self.gravity = .8
                    self.force = [0,0]

            #Shun' Po (Start)
            if self.action == 30:
                self.targetFrame = self.frames45
                self.force = [3, 16]
                self.invincible = True
                if self.targetFrame[int(self.frame)] == 64 and self.voiceFrame != 64:
                    self.voiceFrame = 64
                    self.Play("Audio/wiff.wav")
                    choice = random.choice(["Audio/Champs/Cammy/Grunt/42e.wav", "Audio/Champs/Cammy/Grunt/43e.wav"])
                    self.PlayVoice(choice)
                if self.frame >= len(self.frames45) - 1:
                    self.frame = 0
                    self.action = 0
                    self.voiceFrame = 0
                    self.invincible = False
                    self.state = "Grounded"
                    if self.opponent.fall:
                        self.state = "Skill"
                        self.action = 30.1
                        self.jumpHeight = 9
                        self._height()
                        self.Play("Audio/jump.wav")
                    
            ##Shun' Po -> Air Attack (Leap) -> Punch
            if self.action == 30.1:
                self.targetFrame = self.frames45B
                self.velocity = 2 * self.direction * -1
                if self.frame >= len(self.frames45B) - 1:
                    self.frame = 0
                    self.action = 30.2
                    self.vel[1] = self.jumpHeight
                    if self.hitKick == "MK":
                        self.action = 30.4
                        self.vel[1] += 3
                    
            ##Shun' Po -> Air Attack (First) -> Punch
            if self.action == 30.2:
                self.force = [3, 6]
                self.targetFrame = self.frames45C
                if self.targetFrame[int(self.frame)] == 69 and self.voiceFrame != 69:
                    self.voiceFrame = 69
                    self.Play("Audio/wiff.wav")
                    choice = random.choice(["Audio/Champs/Cammy/Grunt/42e.wav", "Audio/Champs/Cammy/Grunt/43e.wav"])
                if self.frame >= len(self.frames45C) - 1:
                    self.frame = 0
                    self.voiceFrame = 0
                    self.action = 30.3
                    self.vel[1] = 6
                    time.sleep(.05)
                    
            ##Shun' Po -> Air Attack (Second) -> Punch
            if self.action == 30.3:
                self.force = [8, 4]
                self.targetFrame = self.frames45D
                if self.targetFrame[int(self.frame)] == 72 and self.voiceFrame != 72:
                    self.voiceFrame = 72
                    self.Play("Audio/wiff.wav")
                    self.jumpHeight = 5
                    self.vel[1] = self.jumpHeight
                    choice = random.choice(["Audio/Champs/Cammy/Grunt/42e.wav", "Audio/Champs/Cammy/Grunt/43e.wav"])
                if self.frame >= len(self.frames45D) - 1:
                    self.frame = len(self.frames45D) - 1
                    self.voiceFrame = 0


            ##Shun' Po -> Air Attack (First) -> Kick
            if self.action == 30.4:
                self.inAfterImage = True
                self.force = [3, 3]
                self.damage = 30
                self.targetFrame = self.frames46
                if self.vel[1] <= 0:
                    self.jumpHeight = 0
                    self.vel[1] = self.jumpHeight
                if self.targetFrame[int(self.frame)] == 76 and self.voiceFrame != 76:
                    self.voiceFrame = 76
                    self.Play("Audio/wiff.wav")
                if self.frame >= len(self.frames46) - 1:
                    self.frame = 0
                    self.voiceFrame = 0
                    self.action = 30.5
                    time.sleep(.05)
                    
            ##Shun' Po -> Air Attack (Second) -> Kick
            if self.action == 30.5:
                self.force = [8, 7]
                self.targetFrame = self.frames46B
                if self.targetFrame[int(self.frame)] == 74 and self.voiceFrame != 74:
                    self.voiceFrame = 74
                    self.Play("Audio/wiff.wav")
                    self.jumpHeight = 0
                    self.vel[1] = self.jumpHeight
                    choice = random.choice(["Audio/Champs/Cammy/Grunt/45e.wav", "Audio/Champs/Cammy/Grunt/46e.wav", "Audio/Champs/Cammy/Grunt/48e.wav",
                                            "Audio/Champs/Cammy/Grunt/54_2e.wav"])
                    self.PlayVoice(choice)
                if self.frame >= len(self.frames46B) - 1:
                    self.frame = len(self.frames46B) - 1
                    self.voiceFrame = 0
                    self.inAfterImage = False
            
                    
            #Super Cannon Drill (Start)
            if self.action == 31:
                self.targetFrame = self.frames24
                if self.frame >= len(self.frames24) - 1:
                    self.frame = 0
                    self.action = 31.5
                
                    
                    
                    
            #Throwing(Catching)
            if self.action == 21:
                self.isGrabbing = True
                self.targetFrame = self.frames37
                if self.frame >= len(self.frames37) - 1:
                    self.isGrabbing = False
                    self.frame = 0
                    self.action = 0
                    
            #Throwing(Caught)
            if self.action == 22:
                self.backSpring = True
                self.isGrabbing = True
                self.targetFrame = self.frames38
                self.targetGrabbed.action = self.catchFrames[int(self.frame)]
                self.force = [6,1]
                if self.frame >= len(self.frames38) - 1:
                    self.targetGrabbed.isGrabbed = False
                    self.targetGrabbed.Get_Hit(attacker=self, damage=self.damage, force=self.force, typeHit="FireBall")
                    self.targetGrabbed = None
                    self.isGrabbing = False
                    self.action = 7.5
                    self.fallHeight = 3
                    self.fall = True
                    self.force = [0,0]
                    self.frame = len(self.frames38) - 1
                    

            #Dummy
            if self.action == -100:
                self.action = 0
                self.state = "Grounded"
                self.isGrabbing = False
                self.isControlled = True
                
            #Getting Caught A (Ground)
            if self.action == 23:
                self.targetFrame = self.frames39
                self.isGrabbed = True
                self.frame = 0
                    
            #Getting Caught B (Ground)
            if self.action == 23.3:
                self.targetFrame = self.frames39
                self.isGrabbed = True
                self.frame = 1
                    
            #Getting Caught C (Mid)
            if self.action == 23.6:
                self.targetFrame = self.frames39
                self.isGrabbed = True
                self.frame = 2
                    
            #Getting Caught D (High)
            if self.action == 23.8:
                self.targetFrame = self.frames39
                self.isGrabbed = True
                self.frame = 3



            ############ End Game ############
            #Win - To - Sub Animation Win
            if self.action == 20:
                self.targetFrame = self.frames30
                if self.frame >= len(self.frames30) - 1:
                    choice = [20.2, 20.5]
                    self.action = random.choice(choice)
                    self.frame = 0
                    if self.voiceCD <= 0:
                        if self.winCount == 1:
                            self.Play(self.wins[0][1][0])
                        if self.winCount >= 2:
                            choice = random.choice([0,1])
                            self.Play(self.wins[1][1][choice])
                    
            #Sub Animation Win (Shuffule Arms)
            if self.action == 20.2:
                self.targetFrame = self.frames31
                if self.frame >= len(self.frames31) - 1:
                    self.frame = len(self.frames31) - 1
                    
            #Sub Animation Win 2B (Turn Around)
            if self.action == 20.5:
                self.targetFrame = self.frames33
                if self.frame >= len(self.frames33) - 1:
                    self.frame = len(self.frames33) - 1
                    
                    
            #Idle - Taunt (Loop)
            if self.action == -4:
                self.targetFrame = self.frames36B
                if self.frame >= len(self.frames36B) - 1:
                    self.action = -5
                    self.frame = 0
                    
            #Taunt
            if self.action == -5:
                self.targetFrame = self.frames36
                if self.frame >= len(self.frames36) - 1:
                    self.action = 0
                    self.frame = 0
                    
                    
            #Idle - Response Taunt (Loop)
            if self.action == -4.5:
                self.targetFrame = self.frames35B
                if self.frame >= len(self.frames35B) - 1:
                    self.action = -6
                    self.frame = 0

                    
            #Respond Taunt
            if self.action == -6:
                self.targetFrame = self.frames35
                if self.frame >= len(self.frames35) - 1:
                    self.frame = 0
                    self.targetFrame = self.frames1
                    self.action = 0
                    
        self.Update_Grab()
        self.Update_Graphics()

























        



