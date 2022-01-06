import sys, pickle, pyglet, random, time, math, os
from ball import *
from champion import Champion


def preload_image(image):
    img = pyglet.image.load("sprites/" + image + ".png")
    return img

class FeiLong(Champion):
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
        self.variation_images = [pyglet.sprite.Sprite(preload_image("Fei'Long/variation_A")), pyglet.sprite.Sprite(preload_image("Fei'Long/variation_B"))]
        self.variation_names = ["Kung'Fu", "Fei' Jit Su"]
        self.variation_description = [self.variation_names[0] + ": Fei'Long gains strong attacks but has reduced speed, he deals bonus damage depending on how much health he has",
                                      self.variation_names[1] + ": Fei'Long can parry opponents agaiinst basic attacks, he also gains attack speed that scales with his rage bar"]

        #Biography
        self.main_description = ["Fei'Long is a strong warrior that participated in the battle among daemons and humans. He joined Ryu ",
                            "and fought off the invaders with his unique skill and speed. Fei'Long hopes to train an army of ",
                            "young warriors to follow in his footsteps and become masters of Fei' Jit Su"]
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
        self.talkTo = [["Ken", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"], ["M.Bison", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"],
                       ["Ryu", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"],["Cammy", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"],
                       ["Akuma", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"], ["Fei'Long", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"],
                       ["Chun'Li", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"], ["Chun'Li", "I", "Audio/Champs/"+self.name+"/Dialogues/I.wav"]]
        
        self.respondTo = [["Ryu", "G", "Audio/Champs/"+self.name+"/Dialogues/B.wav"],["Fei'Long", "A", "Audio/Champs/"+self.name+"/Dialogues/E.wav"],
                          ["Fei'Long", "A", "Audio/Champs/"+self.name+"/Dialogues/I.wav"],["Fei'Long", "A", "Audio/Champs/"+self.name+"/Dialogues/F.wav"],
                          ["Chun'Li", "A", "Audio/Champs/"+self.name+"/Dialogues/E.wav"], ["Chun'Li", "A", "Audio/Champs/"+self.name+"/Dialogues/C.wav"],
                          ["Chun'Li", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"]]

        #Combination
        self.skill = [["dfA", "Rekkaken"], ["bfK", "Thrust Kick"], ["dbA", "Flurry Punch"], ["ddS", "Aura Flow"], ["ddA", "Parry"], ["bfSA", "Rekkaken Furry"]]

        
        #Audio
        self.soundFrame = 0
        self.voiceFrame = 0
        self.sound = pyglet.media.load("Audio/Champs/Ryu/dragon_ball.wav", streaming=False)
        self.voiceCD = 0
        self.wins= [["First_Wins", ["Audio/Champs/"+self.name+"/Wins/first_win.wav"]], ["End_Game", ["Audio/Champs/"+self.name+"/Wins/end_gameA.wav",
                                                                                           "Audio/Champs/"+self.name+"/Wins/end_gameB.wav",
                                                                                           "Audio/Champs/"+self.name+"/Wins/end_gameC.wav",
                                                                                           "Audio/Champs/"+self.name+"/Wins/end_gameD.wav"]],
                    ["Low_Health_Win", ["Audio/Champs/Ryu/Wins/low_health_win.wav"]]]

        self.championTaunt = {"M.Bison": self.LoadAllFilesFromDirectory("Audio/Champs/"+self.name+"/Wins/M.Bison"),
                              "Chun'Li": self.LoadAllFilesFromDirectory("Audio/Champs/"+self.name+"/Wins/Chun'Li")}

        ################ Animations ###############
        #Standing
        self.frames1 = [0, 0, 1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 8, 8, 9]
        #Walking
        self.frames2 = [10, 10, 11, 12, 12, 13, 14, 14]
        #Weak Punch
        self.frames3 = [23, 24, 24, 25]
        #Medium Punch
        self.frames4 = [26, 26, 27, 27, 28, 28, 29]
        #Strong Punch A
        self.frames15 = [51, 52, 52, 53, 53, 53]
        #Strong Punch B
        self.frames19 = [40, 40, 41]
        #Strong Punch C
        self.frames26 = [42, 43, 43, 44]
        #Crouch
        self.frames7 = [43]
        #Crouch Weak Punch
        self.frames8 = [47, 48, 48, 47]
        #Crouch Medium Punch
        self.frames9 = [49, 50, 50, 49]
        #Jump
        self.frames10 = [16, 16, 16, 16, 16, 17, 17, 17, 18]
        #Jump (Punch)
        self.frames10A = [75, 76, 77, 77, 76]
        #Jump (Kick)
        self.frames10B = [78, 79, 79, 78]
        #Land
        self.frames11 = [43, 43, 43]
        #Getting Hit
        self.frames12 = [80, 80, 80, 81, 81]
        #Getting Hit
        self.frames13 = [82, 82, 82, 83, 83]
        #Getting Hit
        self.frames14 = [84, 84, 84, 85, 85]
        #Falling Bounce
        self.frames16 = [89, 89, 89]
        #Lying
        self.frames17 = [88, 88, 88, 88, 88, 88, 88, 88, 88, 88]
        #Back Spring
        self.frames17B = [90, 90, 91, 91, 92, 92, 93, 93]
        #Weak Kick
        self.frames20 = [60, 60, 61, 61, 60]
        #Medium Kick
        self.frames21 = [60, 60, 61, 61, 60]
        #Crouch Weak Kick
        self.frames22 = [54, 55, 55, 54]
        #Crouch Medium Kick 
        self.frames23 = [56, 57, 57, 58]

        
        #Rekkaken(Start)
        self.frames24 = [100, 101, 102, 108, 108, 109]
        #Rekkaken(Second)
        self.frames25A = [100, 100, 103, 104, 108, 108, 109]
        #Rekkaken(Third)
        self.frames25B = [105, 105, 106, 107, 108, 108, 109, 108, 109, 108, 109, 109]
        self.freezeInAir = False
        self.kickLoop = 5

        
        #Thrust Kick(Start)
        self.frames27 = [110, 110]
        #Thrust Kick(Air)
        self.frames40 = [111, 111, 112, 112, 112, 112]
        #Thrust Kick(End)
        self.frames41 = [113, 114, 114, 113]
        
        #Flurry Punch(Start)
        self.grabChain = 19.1
        self.frames42 = [36, 37, 37, 36, 37, 37, 23, 24, 24, 24]
        #Parry (Start)
        self.frames43 = [104, 68, 68, 68, 68, 68]
        #Parry (Connect)
        self.frames44 = [109, 109, 109, 109, 109, 109]


        
        #Blocking Frames
        self.frames29 = [19, 20, 21, 22]
        self.frames29B = [61, 61, 61, 61, 61, 61, 61, 62, 64, 64, 64]
        self.blockWait = 0

        
        #Win - To - Sub Animation Win
        self.frames30 = [96, 96, 96, 96]
        #Sub Animation Win
        self.frames31 = [138, 138, 139, 139, 140, 140, 141, 141, 142, 142, 143, 143, 144, 144, 145, 145, 146, 146, 147, 147, 148, 148, 149]
        #Sub Animation Win 2A
        self.frames32 = [75, 76, 77, 78]
        #Sub Animation Win 2A (Loop)
        self.frames33 = [41]
        
        #Rekkaken Furry (Start)
        self.frames34 = [108, 108, 108, 108, 108, 108, 108, 108, 108]
        #Rekkaken Furry (Mid)
        self.frames34B = [100, 101, 102, 103, 104, 104, 27, 28, 104, 103, 100, 101, 102, 103, 104, 104]
        

        #Start Game (Dialogues)
        #Respond from taunt
        self.frames35 = [0]
        #Idle Response
        self.frames35B = [143, 143, 143, 144, 144, 144, 143, 143, 143, 144,144, 144, 143, 143, 143,
                          144, 144, 144, 143, 143, 143, 144, 144, 144, 143, 143, 143]
        #Taunt
        self.frames36 = [94, 94, 95, 95, 96, 97, 96, 97, 96, 96, 97, 97, 96, 95, 94, 94]
        #Taunt IDLE
        self.frames36B = [145, 145, 144, 144, 143, 143, 142, 142, 141, 141, 140, 140, 139, 139, 138, 138]
        
        #Throw (Catching)
        self.frames37 = [132, 132, 132, 132]
        #Throw (Caught)
        self.frames38 = [132, 133, 133, 133, 135, 135, 135, 136, 136, 136, 137, 137, 137]
        self.catchFrames = [23, 23.3, 23.3, 23.3, 23.3, 23.3, 23.3, 23.8, 23.8, 23.8, 23.8, 23.8, 23.8, 23.8]
        #Throw (Getting Caught)
        self.frames39 = [83, 84, 86, 87]

        #Aura Flow
        self.frames45 = [94, 94, 95, 95, 96, 97, 96, 97, 96, 96, 97, 97, 96, 95, 95]
        #Shun' Po -> Air Attack (Leap) -> Punch
        self.frames45B = [110, 110, 110, 122]
        #Shun' Po -> Air Attack (First) -> Punch
        self.frames45C = [67, 68, 68, 69, 69]
        #Shun' Po -> Air Attack (Second) -> Punch
        self.frames45D = [70, 71, 71, 72, 72, 72, 67]

        #Shun' Po
        #Shun' Po -> Air Attack (First) -> Kick
        self.frames46 = [70, 71, 72, 72]

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
        #Flurry Punch
        if skill == "Flurry Punch":
            if self.state == "Grounded" or self.state == "Crouch":
                self.state = "Skill"
                self.action = 19
                self.frame = 0

        #Rekkaken
        if skill == "Rekkaken":                
            if self.state == "Grounded" or self.state == "Crouch" or self.state == "BlockHit":
                self.state = "Skill"
                self.frame = 0
                self.action = 17      
                choice = "Audio/Champs/Fei'Long/Grunt/" + random.choice(os.listdir("Audio/Champs/Fei'Long/Grunt"))
                self.PlayVoice(choice)
                
        #Thrust Kick
        if skill == "Thrust Kick":                
            if self.state == "Grounded" or self.state == "Crouch":
                self.invincible = True
                self.state = "Skill"      
                self.frame = 0
                self.action = 12
                
        #Aura Flow
        if skill == "Aura Flow":                
            if self.state == "Grounded" or self.state == "Crouch":
                self.state = "Skill"      
                self.frame = 0
                self.PlayVoice("Audio/Champs/Fei'Long/Skill/skill_chargeB.wav")
                self.action = 30
                
        #Parry
        if skill == "Parry":                
            if self.state == "Grounded" or self.state == "Crouch":
                self.grabChain = 19
                self.parry = True
                self.state = "Skill"      
                self.frame = 0
                choice = "Audio/Champs/Fei'Long/Grunt/" + random.choice(os.listdir("Audio/Champs/Fei'Long/Grunt"))
                self.PlayVoice(choice)
                self.action = 19.1

        #Rekkaken Furry
        if skill == "Rekkaken Furry":
            if self.state == "Grounded" or self.state == "Crouch":
                if self.rageBar >= 400:
                    self.rageBar -= 400
                    self.action = 31
                    self.invincible = True
                    self.state = "Skill"  
                    self.voiceFrame = 0
                    self.superSkill = True
                    self.vfx.append(Ball(pos=(self.pos[0] - 20, self.pos[1] - 20), name="VFX", loop=False, destroy=3, width=225, height=225,
                                          speed=.2, img="sprites/special.png", row=4, col=2))  
                    self.Play("Audio/Champs/Ryu/special.wav")
                    choice = "Audio/Champs/Fei'Long/Skill/Rekkaken Furry/" + random.choice(os.listdir("Audio/Champs/Fei'Long/Skill/Rekkaken Furry"))
                    self.PlayVoice(choice)
                    

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
            if self.targetVariation == "Fei' Jit Su":
                self.frameSpeed = self.defualtSpeed + (self.rageBar / 4000)
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
                    self.action = -100
                    self.state = "Grounded"
                    self.Play("Audio/Champs/Fei'Long/breaker.wav")
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
                    self.slideDirection = 0
                    self.force = [0,0]
                    
            #Thrust Kick(Start)
            if self.action == 12:
                self.targetFrame = self.frames27
                if self.frame >= len(self.frames27) - 1:
                    self.Play("Audio/jump.wav")
                    self.action = 12.5
                    self.jumpHeight = 7
                    self._height()
                    self.frame = 0
                
            #Thrust Kick(Mid)
            if self.action == 12.5:
                self.invincible = False
                if self.frame < 1 and self.voiceFrame != -1:
                    self.invincible = True
                    choice = random.choice(["Audio/Champs/Fei'Long/Grunt/45e.wav", "Audio/Champs/Fei'Long/Grunt/43e.wav",
                                            "Audio/Champs/Fei'Long/Grunt/47e.wav"])
                    self.PlayVoice(choice)
                    self.voiceFrame = -1
                self.force = [7.2,5]
                self.damage = 30
                self.vel[0] = -4
                self.targetFrame = self.frames40
                if self.frame >= len(self.frames40) - 1:
                    self.voiceFrame = 0
                    self.frame = len(self.frames40) - 1
                    
            #Thrust Kick(End)
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
                    
            #Rekkaken(Start)
            if self.action == 17:
                self.force = [3,0]
                self.opponent.maxHitCD = .7
                self.targetFrame = self.frames24
                self.vel[0] = -2
                if self.frame >= len(self.frames24) - 1:
                    self.frame = 0
                    self.action = -100
                    self.vel[0] = 0
                    self.opponent.maxHitCD = 1
                    
                #Skip Some Frames 
                if self.frame >= len(self.frames24) - 3:
                    self.vel[0] = 0
                    if self.hitPunch:
                        self.vel[0] = -2
                        self.frame = 0
                        self.action = 17.3
                        self.hitPunch = ""
                        choice = "Audio/Champs/Fei'Long/Grunt/" + random.choice(os.listdir("Audio/Champs/Fei'Long/Grunt"))
                        self.PlayVoice(choice)
                    
            #Rekkaken(Second)
            if self.action == 17.3:
                self.targetFrame = self.frames25A
                if self.targetFrame[int(self.frame)] == 103 and self.voiceFrame != 103:
                    self.Play("Audio/wiff.wav")
                    self.voiceFrame = 103
                if self.frame >= len(self.frames25A) - 1:
                    self.frame = 0
                    self.vel[0] = 0
                    self.action = -100
                    self.opponent.maxHitCD = 1

                #Skip Some Frames 
                if self.frame >= len(self.frames25A) - 3:
                    self.vel[0] = 0
                    if self.hitPunch:
                        self.frame = 0
                        self.action = 17.5
                        self.hitPunch = ""
                        choice = random.choice(["Audio/Champs/Fei'Long/Skill/skill_endA.wav", "Audio/Champs/Fei'Long/Skill/skill_endB.wav"])
                        self.PlayVoice(choice)
                    
            #Rekkaken(Third)
            if self.action == 17.5:
                self.force = [8,7]
                self.targetFrame = self.frames25B
                if self.targetFrame[int(self.frame)] == 106 and self.voiceFrame != 106:
                    self.Play("Audio/wiff.wav")
                    self.voiceFrame = 106
                if self.frame >= len(self.frames25B) - 1:
                    self.vel[0] = 0
                    self.frame = 0
                    self.action = -100
                    self.hitPunch = ""
                    self.opponent.maxHitCD = 1
                    
                    
            #Flurry Punch
            if self.action == 19:
                self.targetFrame = self.frames42
                self.opponent.maxHitCD = .7
                self.force = [2,0]
                if self.targetFrame[int(self.frame)] == 36 and self.voiceFrame != 36:
                    self.voiceFrame = 36
                    self.Play("Audio/wiff.wav")
                    self.PlayVoice("Audio/Champs/Fei'Long/Skill/skill_start.wav")
                    self.vel[0] = -2
                elif self.targetFrame[int(self.frame)] == 24 and self.voiceFrame != 24:
                    self.vel[0] = -2
                    self.voiceFrame = 24
                else:
                    self.vel[0] = 0
                    self.voiceFrame = 0
                if self.frame >= len(self.frames42) - 1:
                    self.frame = 0
                    self.vel[0] = 0
                    self.opponent.maxHitCD = 1
                    self.action = 17.5
                    choice = random.choice(["Audio/Champs/Fei'Long/Skill/skill_endA.wav", "Audio/Champs/Fei'Long/Skill/skill_endB.wav"])
                    self.PlayVoice(choice)
                    
            #Parry (Start)
            if self.action == 19.1:
                self.targetFrame = self.frames43
                if self.frame >= len(self.frames43) - 1:
                    self.action = -100
                    self.frame = 0
                    self.parry = False
                    
            #Parry(Connect)
            if self.action == "Parry":
                self.invincible = True
                self.parry = False
                self.targetFrame = self.frames44
                self.opponent.frameSpeed = .05
                if int(self.frame) == 3 and self.voiceFrame != 3:
                    self.voiceFrame = 3
                    choice = "Audio/Champs/Fei'Long/Grunt/" + random.choice(os.listdir("Audio/Champs/Fei'Long/Grunt"))
                    self.PlayVoice(choice)
                if self.frame >= len(self.frames44) - 1:
                    self.state = "Skill"
                    self.action = 19
                    self.frame = 0
                    self.invincible = False
                    self.opponent.frameSpeed = self.opponent.defualtSpeed

            #Aura Flow
            if self.action == 30:
                self.targetFrame = self.frames45
                self.rageBar += .3
                if self.frame >= len(self.frames45) - 1:
                    self.frame = 0
                    self.action = -100
                    self.voiceFrame = 0
                    

            #Rekkaken Furry (Start)
            if self.action == 31:
                self.inAfterImage = True
                self.targetFrame = self.frames34
                if self.frame >= len(self.frames34) - 1:
                    self.frame = 0
                    self.action = 31.5
                    self.voiceFrame = -1
                    self.damage = 20
                    self.superSkill = False
                    

            #Rekkaken Furry (Mid)
            if self.action == 31.5:
                self.targetFrame = self.frames34B
                self.vel[0] = -2
                FTPS = [-1, 0, -1, -1, -1, -1, 1, -1, -1, -1, -1, 2, -1, 3, -1, -1]
                self.frameSpeed = .3
                choice = ["Audio/Champs/Fei'Long/Skill/rekkaken_furryA.wav", "Audio/Champs/Fei'Long/Skill/rekkaken_furryB.wav",
                          "Audio/Champs/Fei'Long/Skill/rekkaken_furryC.wav", "Audio/Champs/Fei'Long/Skill/rekkaken_furryD.wav"]                        
                if FTPS[int(self.frame)] > -1:
                    if self.voiceFrame != FTPS[int(self.frame)]:
                        self.PlayVoice(choice[self.voiceFrame])
                    self.voiceFrame = FTPS[int(self.frame)]

                
                #Wiff
                FTPS = [101, 103, 27]
                for i in range(len(FTPS)):
                    if self.targetFrame[int(self.frame)] == FTPS[i] and self.soundFrame != FTPS[i]:
                        self.soundFrame = FTPS[i]
                        self.Play("Audio/wiff.wav")
                        
                if self.frame >= len(self.frames34B) - 1:
                    self.frame = 0
                    self.action = 17.5
                    self.voiceFrame = 0
                    choice = random.choice(["Audio/Champs/Fei'Long/Skill/rekkaken_furryE.wav"])
                    self.PlayVoice(choice)
                    self.vel[0] = 0
                    self.inAfterImage = False
                    self.invincible = False
                
                    
                    
                    
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
                self.force = [-12,6]
                self.backSpring = True
                self.isGrabbing = True
                self.targetFrame = self.frames38
                if self.isGrabbing:
                    self.opponent.action = self.catchFrames[int(self.frame)]
                if self.frame >= len(self.frames38) - 1:
                    self.action = -100
                    self.force = [0,0]
                    self.frame = 0
                if self.targetFrame[int(self.frame)] == 137 and self.opponent.isGrabbed:
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
                    self.action = 0
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
                self.action = -4
                    
        self.Update_Grab()
        self.Update_Graphics()

























        



