import sys, pickle, pyglet, random, time, math, os
from ball import *
from champion import Champion


def preload_image(image):
    img = pyglet.image.load("sprites/" + image + ".png")
    return img

class ChunLi(Champion):
    def __init__(self, name):
        super().__init__(name)
        self.defualtSpeed = .3
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
        self.variation_images = [pyglet.sprite.Sprite(preload_image("Chun'Li/variation_A"))]
        self.variation_names = ["Kung'Fu"]
        self.variation_description = [self.variation_names[0] + ": Chun'Li has strong kicks that deals bonus damage to an enemy depending on how much stamina she has she can also parry weak and medium attacks"]

        #Biography
        self.main_description = ["Chun'Li is a Chinese Warrior that aided the Dragon Temple during the world war. Her selfless ",
                                 "act granted her a place in the temple as one of the 'Guardians of Dragon'"]
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
        self.talkTo = [["Ken", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"], ["M.Bison", "E", "Audio/Champs/"+self.name+"/Dialogues/A.wav"],
                       ["Ryu", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"], ["Ryu", "D", "Audio/Champs/"+self.name+"/Dialogues/D.wav"],
                       ["Cammy", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"],
                       ["Akuma", "E", "Audio/Champs/"+self.name+"/Dialogues/A.wav"], ["Fei'Long", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"],
                       ["Chun'Li", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"], ["Chun'Li", "D", "Audio/Champs/"+self.name+"/Dialogues/D.wav"],
                       ["Ken", "D", "Audio/Champs/"+self.name+"/Dialogues/D.wav"]]
        
        self.respondTo = [["Ryu", "D", "Audio/Champs/"+self.name+"/Dialogues/B.wav"],["Fei'Long", "A", "Audio/Champs/"+self.name+"/Dialogues/E.wav"],
                          ["Chun'Li", "A", "Audio/Champs/"+self.name+"/Dialogues/B.wav"], ["Ken", "D", "Audio/Champs/"+self.name+"/Dialogues/C.wav"],
                          ["Ken", "I", "Audio/Champs/"+self.name+"/Dialogues/F.wav"], ["Ken", "I", "Audio/Champs/"+self.name+"/Dialogues/G.wav"],
                          ["Ken", "B", "Audio/Champs/"+self.name+"/Dialogues/F.wav"], ["Ken", "B", "Audio/Champs/"+self.name+"/Dialogues/G.wav"],
                          ["Ken", "C", "Audio/Champs/"+self.name+"/Dialogues/D.wav"], ["Ken", "F", "Audio/Champs/"+self.name+"/Dialogues/G.wav"],
                          ["Ryu", "F", "Audio/Champs/"+self.name+"/Dialogues/C.wav"], ["Akuma", "F", "Audio/Champs/"+self.name+"/Dialogues/F.wav"],
                          ["Chun'Li", "A", "Audio/Champs/"+self.name+"/Dialogues/I.wav"], ["Chun'Li", "D", "Audio/Champs/"+self.name+"/Dialogues/F.wav"]]

        #Combination
        self.skill = [["dfA", "Kikokun"], ["dfKK", "Thrust Kick"], ["bfKK", "Flurry Kicks"], ["fbKK", "Bird Kick"]]

        
        #Audio
        self.voiceFrame = 0
        self.sound = pyglet.media.load("Audio/Champs/Ryu/dragon_ball.wav", streaming=False)
        self.voiceCD = 0
        self.wins= [["First_Wins", ["Audio/Champs/"+self.name+"/Wins/first_win.wav"]], ["End_Game", ["Audio/Champs/"+self.name+"/Wins/end_gameA.wav",
                                                                                           "Audio/Champs/"+self.name+"/Wins/end_gameB.wav",
                                                                                           "Audio/Champs/"+self.name+"/Wins/end_gameC.wav",
                                                                                           "Audio/Champs/"+self.name+"/Wins/end_gameD.wav"]],
                    ["Low_Health_Win", ["Audio/Champs/Ryu/Wins/low_health_win.wav"]]]
        
        self.championTaunt = {"M.Bison": self.LoadAllFilesFromDirectory("Audio/Champs/"+self.name+"/Wins/M.Bison"),
                              "Ken": self.LoadAllFilesFromDirectory("Audio/Champs/"+self.name+"/Wins/Ken"),
                              "Fei'Long": self.LoadAllFilesFromDirectory("Audio/Champs/"+self.name+"/Wins/Fei'Long")}

        ################ Animations ###############
        #Standing
        self.frames1 = [0, 0, 1, 2, 2, 3, 3,]
        #Walking
        self.frames2 = [4, 5, 6, 7, 8, 9, 10, 11, 11]
        #Weak Punch
        self.frames3 = [17, 18, 19, 19]
        #Medium Punch
        self.frames4 = [23, 24, 24, 24, 24, 25, 25]
        #Strong Punch A
        self.frames15 = [27, 27, 28, 28]
        #Strong Punch B
        self.frames19 = [40, 40, 41]
        #Strong Punch C
        self.frames26 = [42, 43, 43, 44]
        #Crouch
        self.frames7 = [16]
        #Crouch Weak Punch
        self.frames8 = [44, 45, 45, 44]
        #Crouch Medium Punch
        self.frames9 = [44, 45, 45, 44]
        #Jump
        self.frames10 = [13, 13, 13, 13, 13, 14, 14, 14, 13]
        #Jump (Punch)
        self.frames10A = [53, 54, 54, 53]
        #Jump (Kick)
        self.frames10B = [55, 56, 56, 55]
        #Land
        self.frames11 = [12, 12, 12]
        #Getting Hit
        self.frames12 = [81, 81, 81, 80, 80, 80, 80]
        #Getting Hit
        self.frames13 = [82, 82, 82, 83, 83, 83, 83]
        #Getting Hit
        self.frames14 = [82, 82, 82, 83, 83, 83, 83]
        #Falling Bounce
        self.frames16 = [89, 89, 89]
        #Lying
        self.frames17 = [88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
        #Back Spring
        self.frames17B = [88, 88, 88, 89, 89, 89, 16, 16]
        #Weak Kick
        self.frames20 = [35, 35, 36, 35, 35]
        #Medium Kick
        self.frames21 = [38, 39, 39, 40, 41, 41]
        #Crouch Weak Kick
        self.frames22 = [46, 47, 47, 46]
        #Crouch Medium Kick 
        self.frames23 = [46, 48, 49, 49, 50, 50]

        
        #Kikokun
        self.frames24 = [59, 60, 60, 61, 61, 62, 62, 62, 62]
        self.freezeInAir = False
        self.kickLoop = 5


        #Flurry Kicks        
        #Flurry Kick(Start)
        self.frames40 = [35, 35]
        #Flurry Kick(Air)
        self.frames41 = [63, 64, 65, 66, 67, 68, 69]
        #Flurry Kick(End)
        self.frames42 = [35, 35]
        
        #Flurry Kick Follow Up (Start)
        self.frames25A = [70, 70, 71, 72, 73, 74, 74, 74]
        #Flurry Kick Follow Up (End)
        self.frames25B = [74, 75, 75]
        
        self.grabChain = 19.1
        #Command Grab A(Start)
        self.frames43 = [15, 15, 15, 118]
        #Command Grab A(Caught)
        self.frames44 = [118, 119, 119, 120, 120, 121, 121]


        
        #Blocking Frames
        self.frames29 = [29, 30, 31, 32]
        #Combo Breaker
        self.frames29B = [35, 35, 35, 35, 35, 35, 35, 70, 70, 71, 72, 73, 74, 74, 74]
        self.blockWait = 0

        
        #Win - To - Sub Animation Win
        self.frames30 = [107, 107, 107, 107]
        #Sub Animation Win
        self.frames31 = [107, 107, 108, 109, 110, 111, 112]
        #Sub Animation Win 2A
        self.frames32 = [75, 76, 77, 78]
        #Sub Animation Win 2A (Loop)
        self.frames33 = [104, 104, 105, 105, 106]
    
        #Bird kick (Start)
        self.frames45 = [93, 93, 93, 93, 93, 94, 94]
        #Bird Kick (Air)
        self.frames45B = [94]
        #Bird Kick (Loop)
        self.frames45C = [100, 99, 98, 97, 97]
        #Bird Kick (Land)
        self.frames45D = [101, 102, 103, 103]

        #Start Game (Dialogues)
        #Respond from taunt
        self.frames35 = [0]
        #Idle Response
        self.frames35B = [106, 106, 105, 105, 104, 104, 104, 104, 104, 104]
        #Taunt
        self.frames36 = [106, 106, 105, 105, 104, 104, 104, 104, 104, 104]
        #Taunt IDLE
        self.frames36B = [104, 104, 104, 104, 104, 104, 104, 104, 104, 104]
        
        #Throw (Catching)
        self.frames37 = [27, 27, 28, 28, 28]
        #Throw (Caught)
        self.frames38 = [76, 76, 77, 77, 78, 78]
        self.catchFrames = [23, 23.3, 23.8, 23.8, 23.8, 23.8]
        #Throw (Getting Caught)
        self.frames39 = [128, 127, 126, 132]

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
        #Bird Kick
        if skill == "Bird Kick":
            if self.state == "Grounded" or self.state == "Crouch":
                if self.rageBar >= 200:
                    self.invincible = True
                    self.rageBar -= 200
                    self.state = "Skill"
                    self.action = 30
                    self.frame = 0
                    self.kickLoop = 4     
                    self.vfx.append(Ball(pos=(self.pos[0] - 20, self.pos[1] - 20), name="VFX", loop=False, destroy=3, width=225, height=225,
                                          speed=.2, img="sprites/special.png", row=4, col=2))  
                    self.Play("Audio/Champs/Ryu/special.wav")
                    choice = ["Audio/Champs/Chun'Li/Skill/ultra_startA.wav", "Audio/Champs/Chun'Li/Skill/ultra_startB.wav", "Audio/Champs/Chun'Li/Skill/ultra_startC.wav"]
                    self.PlayVoice(random.choice(choice))
                    self.superSkill = True

        #Cannon Drill 
        if skill == "Kikokun":                
            if self.state == "Grounded" or self.state == "Crouch" or self.state == "BlockHit":
                if self.stamina > 30:
                    self.stamina -= 30
                    self.state = "Skill"
                    self.force = [4,0]
                    self.frame = 0
                    self.action = 17
                    self.PlayVoice("Audio/Champs/Chun'Li/Skill/kikokun.wav")
                
        #Flurry Kicks
        if skill == "Flurry Kicks":                
            if self.state == "Grounded" or self.state == "Crouch" and self.rageBar > 50:
                self.rageBar -= 50
                self.state = "Skill"      
                self.frame = 0
                self.action = 12
                self.kickLoop = 3
                choice = ["Audio/Champs/Chun'Li/Skill/skill_legsA.wav", "Audio/Champs/Chun'Li/Skill/skill_charge.wav"]
                self.PlayVoice(random.choice(choice))
                

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
        if self.direction == 1:
            self.x = self.pos[0] + self.alignX[self.targetFrame[int(self.frame)]] + -5
            self.y = self.pos[1] + self.alignY[self.targetFrame[int(self.frame)]]
            
        if self.direction == -1:
            self.x = self.pos[0] - self.alignX[self.targetFrame[int(self.frame)]] + 140
            self.y = self.pos[1] + self.alignY[self.targetFrame[int(self.frame)]]
        
         
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
                    
            #Jump (Punch)
            if self.action == -1.2:
                self.targetFrame = self.frames10A
                self.force = [0,0]
                if self.frame >= len(self.frames10A):
                    self.frame = 0
                    self.action = -1
                    
            #Jump (Kick)
            if self.action == -1.5:
                self.targetFrame = self.frames10B
                self.force = [0,0]
                if self.frame >= len(self.frames10B):
                    self.frame = 0
                    self.action = -1
                    
            #Land from Jump
            if self.action == 5:
                self.targetFrame = self.frames11
                self.velocity = 0
                self.state = "Land"
                if self.frame < 1 and self.voiceFrame != 1:
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
                    self.action = -100
                    self.state = "Grounded"
                    self.Play("Audio/Champs/Chun'Li/breaker.wav")
                    self.opponent.Get_Hit(attacker=self, damage=0, force=[12,5], typeHit="Ground")
                    self.frame = 0
                    self.superSkill = False
                    
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
                self.force = [7,5]
                self.targetFrame = self.frames23
                if self.frame >= len(self.frames23) - 1:
                    self.frame = 0
                    self.velocity = 0
                    self.state = "Grounded"
                    self.action = 0
                    
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
                    
            #Kikokun
            if self.action == 17:
                self.targetFrame = self.frames24
                if self.targetFrame[int(self.frame)] == 62 and self.voiceFrame != 62:
                    self.voiceFrame = 62        #Change Voice frame
                    #Spawn Projectile
                    x = self.pos[0] + 50
                    y = self.pos[1] + 15
                    self.Play("Audio/ball.wav")
                    self.balls.append(Ball(pos=(x, y), velX=self.projectile_speed, width=82,  force=self.force, owner=self, speed=1, height=83, damage=40, direction=self.direction,
                                           img="sprites/Ryu/Balls/Medium_Energy_Ball.png", row=4, col=1))
                if self.frame >= len(self.frames24) - 1:
                    self.frame = 0
                    self.action = -100
                    self.vel[0] = 0
                    self.voiceFrame = 0
                    
                    
            #Flurry Kicks
            if self.action == 12:
                self.targetFrame = self.frames40
                self.inAfterImage = True
                if self.frame >= len(self.frames40) - 1:
                    self.Play("Audio/jump.wav")
                    self.action = 19
                    self.jumpHeight = 7
                    self.frame = 0
                    
            #Flurry Kicks (loop)
            if self.action == 19:
                self.targetFrame = self.frames41
                self.force = [.5,0]
                FTPS = [63, 65, 67, 69]
                self.opponent.maxHitCD = .4
                for i in range(len(FTPS)):
                    if self.targetFrame[int(self.frame)] == FTPS[i] and self.voiceFrame != FTPS[i]:
                        self.voiceFrame = FTPS[i]
                        self.Play("Audio/wiff.wav")
                if self.frame >= len(self.frames41) - 1:
                    self.frame = 0
                    self.kickLoop -= 1
                    self.opponent.maxHitCD = 1
                    if self.kickLoop <= 0:
                        if self.hitKick == "MK" and self.rageBar > 30:
                            self.rageBar -= 30
                            self.action = 19.2
                            self.frame = 0
                            self.vel[0] = -1
                            self.PlayVoice("Audio/Champs/Chun'Li/Skill/hazanshu.wav")
                            self.opponent.frameSpeed = .1
                            return
                        elif self.hitPunch == "MP" and self.rageBar > 50:
                            self.rageBar -= 50
                            self.action = 17
                            self.frame = 3
                            self.force = [7,5]
                            self.PlayVoice("Audio/Champs/Chun'Li/Skill/Kikokun.wav")
                        else:
                            self.action = 19.1

            #Flurry Kicks (end)
            if self.action == 19.1:
                self.targetFrame = self.frames42
                self.inAfterImage = False
                if self.frame >= len(self.frames42) - 1:
                    self.action = -100
                    self.frame = 0

            #Flurry Kick Follow Up (Start)
            if self.action == 19.2:
                self.force = [6,13]
                self.targetFrame = self.frames25A
                if self.frame >= len(self.frames25A) - 1:
                    self.frame = 0
                    self.vel[0] = 0
                    self.action = 19.3

            #Flurry Kick Follow Up (End)
            if self.action == 19.3:
                self.targetFrame = self.frames25B
                if self.frame >= len(self.frames25B) - 1:
                    self.frame = 0
                    self.action = -100

            #Bird Kick (Start)
            if self.action == 30:
                self.inAfterImage = True
                self.targetFrame = self.frames45
                if self.frame >= len(self.frames45) - 1:
                    self.superSkill = False
                    self.frame = 0
                    self.action = 30.2
                    self.jumpHeight = 4.5
                    self._height()
                    self.force = [3, 5]
                    self.Play("Audio/jump.wav")
                    
            #Bird Kick (Air)
            if self.action == 30.1:
                self.targetFrame = self.frames45B
                if self.frame >= len(self.frames45B) - 1:
                    self.frame = 0
                    self.action = 30.2
                    self.freezeInAir = True
                    self.invincible = False
                    self.frameSpeed = .5
                    
            #Bird Kick (Loop)
            if self.action == 30.2:
                self.frameSpeed = .25
                self.opponent.maxHitCD = .4
                self.vel[0] = -2
                self.targetFrame = self.frames45C
                FTPS = [98, 100]
                self.damage = 10
                if self.frame > 0.2:
                    self.vel[1] += .63
                for i in range(len(FTPS)):
                    if self.targetFrame[int(self.frame)] == FTPS[i] and self.voiceFrame != FTPS[i]:
                        self.voiceFrame = FTPS[i]
                        self.Play("Audio/big_wiff.wav")
                if self.frame >= len(self.frames45C) - 1:
                    self.kickLoop -= 1
                    self.frame = 0
                    if self.kickLoop < 1:
                        self.force = [12, 4]
                        self.PlayVoice("Audio/Champs/Chun'Li/Grunt/43e.wav")
                        self.vel[1] += .4
                        self.opponent.maxHitCD = 1
                    if self.kickLoop <= 0:
                        self.frame = 0
                        self.voiceFrame = 0
                        self.action = 30.3
                        self.vel[1] = 6
                        self.opponent.maxHitCD = 1
                        self.freezeInAir = False
                        self.invincible = False
                    
            #Bird Kick (Land)
            if self.action == 30.3:
                self.inAfterImage = False
                self.targetFrame = self.frames45D
                if self.frame >= len(self.frames45D) - 1:
                    self.action = -1
                    self.frame = 0
                    self.force = [3, 0]
                    self.voiceFrame = 0
                    self.opponent.maxHitCD = 1
                    self.frameSpeed = self.defualtSpeed
                
                    
                    
                    
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
                self.force = [12,6]
                self.backSpring = True
                self.isGrabbing = True
                self.targetFrame = self.frames38
                if self.isGrabbing:
                    self.opponent.action = self.catchFrames[int(self.frame)]
                if self.frame >= len(self.frames38) - 1:
                    self.action = -100
                    self.force = [0,0]
                    self.frame = 0
                if self.targetFrame[int(self.frame)] == 79 and self.opponent.isGrabbed:
                    self.opponent.isGrabbed = False
                    self.opponent.Get_Hit(attacker=self, damage=self.damage, force=self.force, typeHit="None")
                    self.targetGrabbed = None
                    self.isGrabbing = False
                    
                
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
                    self.frame = 0
                    self.action = 0
                    
            #Taunt
            if self.action == -5:
                self.targetFrame = self.frames36
                if self.frame >= len(self.frames36) - 1:
                    self.action = 0
                    self.targetFrame = self.frames1
                    self.frame = 0
                    
                    
            #Idle - Response Taunt (Loop)
            if self.action == -4.5:
                self.targetFrame = self.frames35B
                if self.frame >= len(self.frames35B) - 1:
                    self.action = 0
                    self.frame = 0

                    
            #Respond Taunt
            if self.action == -6:
                self.action = -4
                    
        self.Update_Grab()
        self.Update_Graphics()

























        



