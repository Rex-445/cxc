import sys, pickle, pyglet, random, time, math
from ball import *
from champion import Champion


def preload_image(image):
    img = pyglet.image.load("sprites/" + image + ".png")
    return img

class Bison(Champion):
    def __init__(self, name):
        super().__init__(name)
        self.hitBoxOffset = -40
        self.aura = False
        self.action = -4
        self.frameSpeed = .3
        self.defualtSpeed = .3
        self.slideDirection = 0

        self.pos = [0,0,0]
        
        self.defualt2 = [name+"_mirror", name+"_2_mirror"]

        self.width, self.height = (79, 79)
        self.hitBox = [0,0, 30,30]
        self.body = [30,0,50,85]
        self.shadowOffset = [20,-5]
        

        #Vairations
        self.variation_images = [pyglet.sprite.Sprite(preload_image("M.Bison/variation_A"))]
        self.variation_names = ["Spell Vamp"]
        self.variation_description = [self.variation_names[0] + ": Bison's psycho powered spells heal him for a percentage of damage dealt, his damage is also greatly increased"]
        
        #Biography
        self.main_description = ["M.Bison is one of the masters of soul magic, he uses his soul to amplify his energy, which ",
                            "increases his strength and power. This power is known as 'Glory', stolen from an elder god ",
                            "he uses it to place authority among those weaker than him. And for others who try to stop him. ",
                            "Their FATE is sealed."]
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
                       ["M.Bison", "G", "Audio/Champs/"+self.name+"/Dialogues/G.wav"], ["M.Bison", "J", "Audio/Champs/"+self.name+"/Dialogues/J.wav"],
                       ["Ryu", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"], ["Ryu", "B", "Audio/Champs/"+self.name+"/Dialogues/B.wav"],
                       ["Ryu", "D", "Audio/Champs/"+self.name+"/Dialogues/D.wav"], ["Cammy", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"],
                       ["Cammy", "B", "Audio/Champs/"+self.name+"/Dialogues/B.wav"], ["Cammy", "G", "Audio/Champs/"+self.name+"/Dialogues/G.wav"],
                       ["Cammy", "J", "Audio/Champs/"+self.name+"/Dialogues/J.wav"], ["Cammy", "M", "Audio/Champs/"+self.name+"/Dialogues/M.wav"],
                       ["Cammy", "O", "Audio/Champs/"+self.name+"/Dialogues/O.wav"], ["Akuma", "A", "Audio/Champs/"+self.name+"/Dialogues/M.wav"],]
        
        self.respondTo = [["Ken", "F", "Audio/Champs/"+self.name+"/Dialogues/B.wav"], ["Ken", "B", "Audio/Champs/"+self.name+"/Dialogues/H.wav"],
                          ["Ken", "B", "Audio/Champs/"+self.name+"/Dialogues/C.wav"], ["Ken", "B", "Audio/Champs/"+self.name+"/Dialogues/K.wav"],
                          ["Ken", "D", "Audio/Champs/"+self.name+"/Dialogues/L.wav"], ["Ken", "D", "Audio/Champs/"+self.name+"/Dialogues/B.wav"],
                          ["Ken", "D", "Audio/Champs/"+self.name+"/Dialogues/N.wav"], ["Ken", "D", "Audio/Champs/"+self.name+"/Dialogues/P.wav"],
                          ["M.Bison", "A", "Audio/Champs/"+self.name+"/Dialogues/C.wav"],
                          ["M.Bison", "G", "Audio/Champs/"+self.name+"/Dialogues/H.wav"], ["M.Bison", "J", "Audio/Champs/"+self.name+"/Dialogues/I.wav"],
                          ["Ryu", "G", "Audio/Champs/"+self.name+"/Dialogues/C.wav"], ["Ryu", "F", "Audio/Champs/"+self.name+"/Dialogues/H.wav"],
                          ["Ryu", "G", "Audio/Champs/"+self.name+"/Dialogues/K.wav"], ["Ryu", "F", "Audio/Champs/"+self.name+"/Dialogues/C.wav"],
                          ["Ryu", "G", "Audio/Champs/"+self.name+"/Dialogues/B.wav"],["Cammy", "A", "Audio/Champs/"+self.name+"/Dialogues/B.wav"],
                          ["Cammy", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"], ["Cammy", "A", "Audio/Champs/"+self.name+"/Dialogues/Q.wav"],
                          ["Cammy", "A", "Audio/Champs/"+self.name+"/Dialogues/Q.wav"], ["Cammy", "A", "Audio/Champs/"+self.name+"/Dialogues/R.wav"],
                          ["Cammy", "B", "Audio/Champs/"+self.name+"/Dialogues/D.wav"], ["Cammy", "B", "Audio/Champs/"+self.name+"/Dialogues/Q.wav"],
                          ["Cammy", "G", "Audio/Champs/"+self.name+"/Dialogues/P.wav"], ["Cammy", "G", "Audio/Champs/"+self.name+"/Dialogues/H.wav"],
                          ["Cammy", "G", "Audio/Champs/"+self.name+"/Dialogues/M.wav"], ["Cammy", "H", "Audio/Champs/"+self.name+"/Dialogues/H.wav"],
                          ["Cammy", "I", "Audio/Champs/"+self.name+"/Dialogues/K.wav"], ["Cammy", "I", "Audio/Champs/"+self.name+"/Dialogues/N.wav"]]

        #Combination
        self.skill = [["bfA", "Psycho Crusher"], ["dbK", "Head Stomp"], ["fdSA", "Super Dragon Punch"], ["bfSA", "Advanced Psycho Crusher"], ["fbK", "Flip Kick"],
                      ["bfK", "Scissors Kick"], ["bSS", "Teleport Back"], ["fSS", "Teleport Forward"]]
        #Audio
        self.voiceFrame = 0
        self.sound = pyglet.media.load("Audio/Champs/Ryu/dragon_ball.wav", streaming=False)
        self.voiceCD = 0
        self.wins= [["First_Wins", ["Audio/Champs/M.Bison/Wins/first_win.wav"]], ["End_Game", ["Audio/Champs/M.Bison/Wins/end_gameA.wav",
                                                                                           "Audio/Champs/M.Bison/Wins/end_gameB.wav",
                                                                                           "Audio/Champs/M.Bison/Wins/end_gameC.wav",
                                                                                           "Audio/Champs/M.Bison/Wins/end_gameD.wav"]],
                    ["Low_Health_Win", ["Audio/Champs/Ryu/Wins/low_health_win.wav"]]]
        
        self.championTaunt = {"Cammy": self.LoadAllFilesFromDirectory("Audio/Champs/"+self.name+"/Wins/Cammy"),
                              "Ryu": self.LoadAllFilesFromDirectory("Audio/Champs/"+self.name+"/Wins/Ryu")}

        ################ Animations ###############
        #Standing
        self.frames1 = [0, 0, 1, 1, 2, 2, 1, 1]
        #Walking
        self.frames2 = [3, 3, 4, 4, 5, 5, 6, 6]
        #Weak Punch
        self.frames3 = [9, 10, 11, 12]
        #Medium Punch
        self.frames4 = [13, 14, 15, 16, 17, 18, 19, 20]
        #Crouch
        self.frames7 = [27]
        #Crouch Weak Punch
        self.frames8 = [31, 32, 31]
        #Crouch Medium Punch
        self.frames9 = [33, 34, 35, 36, 37, 38, 34, 33]
        #Jump
        self.frames10 = [8]
        #Jump (Punch)
        self.frames10A = [85, 86, 83, 84]
        #Jump (Kick)
        self.frames10B = [85, 86, 87, 88]
        #Land
        self.frames11 = [28, 7, 7]
        #Getting Hit
        self.frames12 = [61, 61, 61, 61, 61]
        #Getting Hit
        self.frames13 = [63, 63, 63, 63, 63]
        #Getting Hit
        self.frames14 = [64, 64, 64, 64, 64]
        #Dragon Ball
        self.frames15 = [94, 95, 107, 108, 109, 109, 109, 109]
        #Falling Bounce
        self.frames16 = [61, 61, 61, 66]
        #Lying
        self.frames17 = [68, 68, 68, 68, 68, 68, 68, 68, 68, 68]
        #Land From Dragon Punch
        self.frames19 = [104]
        #Weak Kick
        self.frames20 = [21, 24, 24]
        #Medium Kick
        self.frames21 = [21, 22, 23, 24, 24, 24, 24]
        #Crouch Weak Kick
        self.frames22 = [39, 40, 39]
        #Crouch Medium Kick (42 Frames are sliding Frames)
        self.frames23 = [41, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 43]
        #Psycho Crucher(Start)
        self.frames24 = [48, 49, 50]
        #Psycho Crucher(Mid)
        self.frames25 = [51, 52, 53, 54]
        self.frames25_ex = [110, 111, 112, 113]
        #Psycho Crucher(End)
        self.freezeInAir = False
        self.kickLoop = 5
        #Hurricane Kick End
        self.frames26 = [50]
        #Head Stomp(Start)
        self.frames27 = [100, 100, 101]
        #Breaker
        self.frames29B = [73, 73, 73, 73, 73, 74, 74, 74]
        #Head Stomp(Air)
        self.frames40 = [101, 101, 101, 101, 102, 102, 102]
        #Head Stomp(End)
        self.frames41 = [103, 103, 104, 104, 105]
        
        #Flip Kick(Start)
        self.frames42 = [106, 106, 106]
        #Flip Kick(Mid)
        self.frames42B = [107, 107, 108, 108, 108, 109, 109, 109, 109]
        
        #Scissors Kick(Start)
        self.frames43 = [43, 43, 43]
        #Scissors Kick(Mid)
        self.frames43B = [55, 55, 56, 56, 57, 57, 58, 59, 59, 59, 59]

        #Teleport
        self.frames44 = [110, 111, 110, 111, 110, 111, 110, 112, 111, 112, 111, 112]
        
        #Blocking Frames
        self.frames29 = [25, 26, 27, 28]
        self.blockWait = 0
        #Win - To - Sub Animation Win
        self.frames30 = [73, 73, 73, 73]
        #Sub Animation Win
        self.frames31 = [74]
        #Sub Animation Win 2A
        self.frames32 = [75, 76, 77, 78]
        #Sub Animation Win 2A (Loop)
        self.frames33 = [78]
        
        #Super Dragon Punch
        self.frames34 = [110, 110, 110, 110, 110, 110, 110, 110, 110, 111, 112, 112, 112, 113]
        self.frames34_forcesX = [0, 0, 0, 0, 0, 0, 5, 0, 0, 4, 0, 5, 5, 4]
        self.frames34_forcesY = [0, 0, 0, 0, 0, 0, 16, 16, 16, 8, 16, 0, 8, 0]

        #Start Game (Dialogues)
        self.frames35 = [81, 81, 81, 81, 81, 82, 82, 82, 82]
        self.frames36 = [79, 80, 79, 80, 79, 80, 79, 80, 79, 80, 79, 80, 79, 80, 79]
        
        #Throw (Catching)
        self.frames37 = [43, 44, 44]
        #Throw (Caught)
        self.frames38 = [43, 44, 44, 44, 45, 45, 45, 46, 46, 46, 47]
        self.catchFrames = [23, 23.3, 23.3, 23.3, 23.6, 23.6, 23.6, 23.8, 23.8, 23.8, 23.8]
        #Throw (Getting Caught)
        self.frames39 = [60, 61, 63, 65]

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
        #Dragon Ball
        if self.state == "Grounded" or self.state == "Crouch":
            if skill == "Teleport Back":
                self.state = "Skill"
                self.invincible = True
                self.Play("Audio/053.wav")
                self.breaker_input = ""
                self.frame = 0
                self.action = 25
                
            if skill == "Teleport Forward":
                self.state = "Skill"
                self.invincible = True
                self.Play("Audio/053.wav")
                self.frame = 0
                self.breaker_input = ""
                self.action = 25.5

        #Psycho Crusher
        if self.state == "Grounded" or self.state == "Crouch":
            if skill == "Psycho Crusher" and self.rageBar >= 50:
                self.rageBar -= 50
                self.state = "Skill"
                self.Play("Audio/jump.wav")
                self.frame = 0
                self.jumpHeight = 9
                self.action = 17
                self._height()
                self.kickLoop = 3


        #Advanced Psycho Crusher
        if self.state == "Grounded" or self.state == "Crouch":
            if skill == "Advanced Psycho Crusher" and self.rageBar >= 200:
                self.rageBar -= 200
                self.state = "Skill"
                self.Play("Audio/Champs/Ryu/special.wav")
                self.PlayVoice("Audio/Champs/M.Bison/advanced_psycho_crusher.wav")
                self.Play("Audio/jump.wav")
                self.frame = 0
                self.jumpHeight = 2
                self.vel[0] = -5
                self.pos[1] += 50
                self.action = 17.3
                self._height()
                self.kickLoop = 4
            
                
        #head Stomp
        if self.state == "Grounded" or self.state == "Crouch":
            if skill == "Head Stomp" and self.rageBar >= 20:
                self.rageBar -= 20
                self.state = "Skill"      
                self.frame = 0
                self.action = 12
            
                
        #Flip Kick
        if self.state == "Grounded" or self.state == "Crouch":
            if skill == "Flip Kick" and self.rageBar >= 20:
                self.rageBar -= 20
                self.state = "Skill"      
                self.frame = 0
                self.action = 18
            
                
        #Flip Kick
        if self.state == "Grounded" or self.state == "Crouch":
            if skill == "Scissors Kick" and self.rageBar >= 20:
                self.rageBar -= 20
                self.state = "Skill"      
                self.frame = 0
                self.action = 19

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
        self.attacking_actions = [2, 2.5, 3, 3.5, 9, 10, 10.5, 11, 11.5, 12, 17.3, 12.5, 13, 13.5, 14, 14.5, 19, 21, 22]        
        if self.direction == 1:
            try:
                self.x = self.pos[0] + self.alignX[self.targetFrame[int(self.frame)]] + 13
                self.y = self.pos[1] + self.alignY[self.targetFrame[int(self.frame)]]
            except:
                self.x = self.pos[0] + self.alignX[29] + 13
                self.y = self.pos[1] + self.alignY[29]
                
            
        if self.direction == -1:
            self.x = self.pos[0] - self.alignX[self.targetFrame[int(self.frame)]] + 113
            self.y = self.pos[1] + self.alignY[self.targetFrame[int(self.frame)]]
        if self.action not in self.attacking_actions:
            self.hitBox[0] = 10000
            self.hitBox[1] = 10000

            
    def Update(self):
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
                #Bonous Damage Increased
                self.AddDamage(5)
                self.targetFrame = self.frames3
                if self.frame >= len(self.frames3) - 1:
                    self.frame = 0
                    self.action = -100
                    
            #Weak Punch Crouch
            if self.action == 2.5:
                #Bonous Damage Increased
                self.AddDamage(5)
                self.targetFrame = self.frames8
                if self.frame >= len(self.frames8) - 1:
                    self.frame = 0
                    self.action = -100
                    self.state = "Grounded"

            #Medium Punch
            if self.action == 3:
                #Bonous Damage Increased
                self.AddDamage(5)
                self.targetFrame = self.frames4
                if self.frame >= len(self.frames4) - 1:
                    self.frame = 0
                    self.action = -100
                    
            #Medium Punch Crouch
            if self.action == 3.5:
                #Bonous Damage Increased
                self.AddDamage(5)
                self.targetFrame = self.frames9
                if self.frame >= len(self.frames9) - 1:
                    self.frame = 0
                    self.action = -100
                    self.state = "Grounded"
                    
            #Crouch
            if self.action == 4:
                self.targetFrame = self.frames7
                if self.frame >= len(self.frames7) - 1:
                    self.frame = 0
                    
            #Jump (Punch)
            if self.action == -1.2:
                self.targetFrame = self.frames10A
                if self.frame >= len(self.frames10A) - 1:
                    self.frame = 0
                    self.action = -1
                    
            #Jump (Kick)
            if self.action == -1.5:
                self.targetFrame = self.frames10B
                if self.frame >= len(self.frames10B) - 1:
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
                    self.frame = 0
                    self.state = "Grounded"
                    self.blockRight = False
                    self.blockLeft = False
                    if self.moveRight:
                        self.right = True
                    if self.moveLeft:
                        self.left = True
                    
            #Getting Hit B
            if self.action == 6.3:
                self.targetFrame = self.frames13
                if self.frame >= len(self.frames13) - 1:
                    self.action = 0
                    self.frame = 0
                    self.state = "Grounded"
                    
            #Getting Hit C
            if self.action == 6.5:
                self.targetFrame = self.frames14
                if self.frame >= len(self.frames14) - 1:
                    self.action = 0
                    self.frame = 0
                    self.state = "Grounded"
                    
            #Breaker
            if self.action == 6.7:
                self.targetFrame = self.frames29B
                if self.frame >= len(self.frames29B) - 4 and self.voiceFrame != -1:
                    self.voiceFrame = -1
                    self.PlayVoice("Audio/Champs/M.Bison/breaker.wav")
                    self.opponent.Get_Hit(attacker=self, damage=0, force=[8,5], typeHit="Ground")
                    self.superSkill = False
                if self.frame >= len(self.frames29B) - 1:
                    self.action = -100
                    self.state = "Grounded"
                    self.frame = 0
                    
            #Falling
            if self.action == 7:
                self.targetFrame = self.frames16
                if self.frame >= len(self.frames16) - 1:
                    self.frame = 0
                    
            #Lying
            if self.action == 7.9:
                self.targetFrame = self.frames17
                self.velocity = 0
                self.state = "Lying"
                self.EX = False
                self.vel = [0,0]
                if self.hitCombo > 0:
                    self.comboEnd = True
                    self.damageDealt = 0
                if self.frame >= len(self.frames17) - 1:
                    self.frame = 0
                    if self.health > 0:
                        self.action = 5
                    else:
                        self.alive = False
                    
                    
            #Land From Dragon Punch
            if self.action == 9.5:
                self.targetFrame = self.frames19
                if self.superSkill == True:
                    self.targetFrame = self.frames35
                if self.frame >= len(self.targetFrame) - 1:
                    self.action = 5

            #Weak Kick
            if self.action == 10:
                #Bonous Damage Increased
                self.AddDamage(5)
                self.targetFrame = self.frames20
                if self.frame >= len(self.frames20) - 1:
                    self.frame = 0
                    self.action = 0
                    
            #Weak Kick Crouch
            if self.action == 10.5:
                #Bonous Damage Increased
                self.AddDamage(5)
                self.targetFrame = self.frames22
                if self.frame >= len(self.frames22) - 1:
                    self.frame = 0
                    self.action = 0
                    self.state = "Grounded"

            #Medium Kick
            if self.action == 11:
                #Bonous Damage Increased
                self.AddDamage(5)
                self.targetFrame = self.frames21
                if self.frame >= len(self.frames21) - 1:
                    self.frame = 0
                    self.action = 0
                    
            #Medium Kick Crouch
            if self.action == 11.5:
                #Bonous Damage Increased
                self.AddDamage(5)
                self.force = [9,5]
                self.state = "Skill"
                if self.slideDirection == 0:
                    self.PlayVoice("Audio/Champs/M.Bison/Grunt/50e.wav")
                    self.slideDirection = self.direction
                self.velocity = -5 * self.slideDirection
                self.targetFrame = self.frames23
                if self.frame >= len(self.frames23) - 1:
                    self.frame = 0
                    self.velocity = 0
                    self.state = "Grounded"
                    self.action = 0
                    self.slideDirection = 0
                    
            #Head Stomp(Start)
            if self.action == 12:
                #Bonous Damage Increased
                self.AddDamage(10)
                self.targetFrame = self.frames27
                if self.frame >= len(self.frames27) - 1:
                    self.Play("Audio/jump.wav")
                    self.action = 12.5
                    self.jumpHeight = 10
                    self._height()
                    self.frame = 0
                
            #Head Stomp(Mid)
            if self.action == 12.5:
                self.force = [4.2,0]
                self.damage = 40
                self.gravity = .4
                if self.direction == 1 and self.opponent.pos[0] > self.pos[0] or self.direction == -1 and self.opponent.pos[0] < self.pos[0]: 
                    self.vel[0] = -math.sqrt(math.pow(self.pos[0] - self.opponent.pos[0], 2)) / 20
                self.targetFrame = self.frames40
                if self.frame >= len(self.frames40) - 1:
                    self.voiceFrame = 0
                    self.frame = len(self.frames40) - 1
                    if self.opponent.hitCD > 0:
                        self.action = 12.8
                        self.frame = 0
                        self.jumpHeight = 6
                        time.sleep(.1)
                        self.vel[1] = self.jumpHeight
                    
            #Head Stomp(End)
            if self.action == 12.8:
                self.targetFrame = self.frames41
                self.vel[0] = 3
                if self.frame >= len(self.frames41) - 1:
                    self.frame = len(self.frames41) - 1
                    self.gravity = .8
                    
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
                if self.blockWait >= 10:
                    self.action = 13
                    self.blockWait = 0
                    
            #Crouch Block (Normal)
            if self.action == 14:
                self.targetFrame = self.frames29
                self.frame = 3
                self.blockWait += 1
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
                self.frame = 4
                self.blockWait += 1
                if self.blockWait >= 20:
                    self.action = 14
                    self.blockWait = 0
                    
            #Psyco Crucher(Start)
            if self.action == 17:
                self.typeHit = "PsycoFire"
                #Bonous Damage Increased
                self.AddDamage(10)
                self.targetFrame = self.frames24
                self.velocity = 0
                self.vel[0] = -5
                if self.frame >= len(self.frames24) - 1:
                    self.frame = 0
                    self.PlayVoice("Audio/Champs/M.Bison/psycho_crusher.wav")
                    self.action = 17.3
                    
            #Psyco Crucher(Mid)
            if self.action == 17.3:
                self.force = [6.7,5]
                self.freezeInAir = True
                
                #Advanced Psyco Crusher
                if self.aura == True:
                    self.AddDamage(10)
                    self.targetFrame = self.frames25_ex
                    if self.targetFrame[int(self.frame)] == 111 and self.voiceFrame != 111:
                        self.Play("Audio/wiff.wav")
                        self.voiceFrame = 111
                    if self.frame >= len(self.frames25) - 1:
                        if self.kickLoop > 0:
                            self.voiceFrame = 0
                            self.kickLoop -= 1
                            self.frame = 0
                        else:
                            self.force = [3,0]
                            self.action = 17.5
                            self.aura = False

                #Normal Psyco Crusher
                else:
                    self.targetFrame = self.frames25
                    if self.targetFrame[int(self.frame)] == 82 and self.voiceFrame != 82:
                        self.Play("Audio/wiff.wav")
                        self.voiceFrame = 82
                    if self.frame >= len(self.frames25) - 1:
                        if self.kickLoop > 0:
                            self.voiceFrame = 0
                            self.kickLoop -= 1
                            self.frame = 0
                        else:
                            self.kickLoop = 6
                            self.force = [3,0]
                            self.action = 17.5
                    
            #Psyco Crucher(End)
            if self.action == 17.5:
                self.freezeInAir = False
                self.targetFrame = self.frames26
                if self.frame >= len(self.frames26) - 1:
                    self.frame = 0
                    self.action = -1
                    self.typeHit = "Damage"
                    self.EX = False

                    
                    
            #Flip kick(Start)
            if self.action == 18:
                self.targetFrame = self.frames42
                if self.frame >= len(self.frames42) - 1:
                    self.frame = 0
                    self.action = 18.5
                    self.jumpHeight = 6
                    self._height()
                    self.vel[0] = -5
                    self.force = [7, 14]

                    
                    
            #Flip kick(Mid)
            if self.action == 18.5:
                self.targetFrame = self.frames42B
                if self.targetFrame[int(self.frame)] == 108 and self.voiceFrame != 108:
                    self.Play("Audio/big_wiff.wav")
                    self.voiceFrame = 108
                if self.frame >= len(self.frames42B) - 1:
                    self.frame = 0
                    self.action = -1
                    self.targetFrame = self.frames10

                    
                    
            #Scissors kick(Start)
            if self.action == 19:
                self.targetFrame = self.frames43
                if self.frame >= len(self.frames43) - 1:
                    self.frame = 0
                    self.action = 19.5
                    self.vel[0] = -5
                    self.force = [10, 5]
                    self.jumpHeight = 5
                    self._height()
                    choice = ["Audio/Champs/M.Bison/Grunt/42e.wav", "Audio/Champs/M.Bison/Grunt/43e.wav",
                              "Audio/Champs/M.Bison/Grunt/45e.wav"]
                    self.PlayVoice(random.choice(choice))

                    
                    
            #Scissors kick(Mid)
            if self.action == 19.5:
                self.frameSpeed = .4
                self.targetFrame = self.frames43B
                if self.targetFrame[int(self.frame)] == 55 and self.voiceFrame != 55:
                    self.voiceFrame = 55
                    self.Play("Audio/big_wiff.wav")                    
                if self.frame >= len(self.frames43B) - 1:
                    self.frame = 0
                    self.frameSpeed = self.defualtSpeed
                    self.action = -100

            #Teleport Back    
            if self.action == 25:
                self.targetFrame = self.frames44
                #Teleport in that direction
                if int(self.frame) == 2 and self.voiceFrame != self.frame:
                    self.frame += 1
                    self.voiceFrame = int(self.frame)
                    self.PlayVoice("Audio/Champs/M.Bison/teleport_laugh.wav")
                    direction = -150 * self.direction
                    if self.pos[0] + direction > 0:
                        self.pos[0] += direction
                    else:
                        self.pos[0] = 0
                        
                if self.frame >= len(self.frames44) - 1:
                    self.invincible = False
                    self.frame = 0
                    self.action = -100
                    self.Mixup_Combo()

            #Teleport Forward
            if self.action == 25.5:
                self.targetFrame = self.frames44
                if int(self.frame) == 2 and self.voiceFrame != self.frame:
                    self.frame += 1
                    self.voiceFrame = int(self.frame)
                    TPAmount = -90 * self.direction
                    if self.opponent.pos[0] - TPAmount > 0:
                        self.pos[0] = self.opponent.body[0] + TPAmount
                    else:
                        self.pos[0] = 0
                    self.pos[0] = self.opponent.pos[0] - TPAmount
                    self.PlayVoice("Audio/Champs/M.Bison/teleport_laugh.wav")
                    
                if self.frame >= len(self.frames44) - 1:
                    self.invincible = False
                    self.frame = 0
                    self.action = -100
                    self.Mixup_Combo()
                

            
                    
                    
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
                self.frameSpeed = .3
                self.isGrabbing = True
                self.targetFrame = self.frames38
                self.targetGrabbed.bdy.x = self.hitBox[0] - self.targetGrabbed.body[0]
                self.targetGrabbed.bdy.y = self.hitBox[1] - self.targetGrabbed.body[1]
                self.targetGrabbed.action = self.catchFrames[int(self.frame)]
                self.force = [-8,10]
                if self.frame >= len(self.frames38) - 1:
                    self.targetGrabbed.isGrabbed = False
                    self.targetGrabbed.Get_Hit(attacker=self, damage=self.damage, force=self.force)
                    self.targetGrabbed = None
                    self.isGrabbing = False
                    self.frame = 0
                    self.action = 0
                    self.frameSpeed = .3
                    self.targetFrame = self.frames1
                    
                    
            #Getting Caught A
            if self.action == 23:
                self.targetFrame = self.frames39
                self.isGrabbed = True
                self.frame = 0
                    
            #Getting Caught B
            if self.action == 23.3:
                self.targetFrame = self.frames39
                self.isGrabbed = True
                self.frame = 1
                    
            #Getting Caught C
            if self.action == 23.6:
                self.targetFrame = self.frames39
                self.isGrabbed = True
                self.frame = 2
                    
            #Getting Caught D
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
                    
            #Sub Animation Win (Fold Arms)
            if self.action == 20.2:
                self.targetFrame = self.frames31
                if self.frame >= len(self.frames31) - 1:
                    self.frame = 0
                    
            #Sub Animation Win 2B (Slice Neck)
            if self.action == 20.5:
                self.targetFrame = self.frames33
                if self.frame >= len(self.frames33) - 1:
                    self.frame = 0
                    
            #Idle - To - Taunt (Loop)
            if self.action == -4:
                self.targetFrame = self.frames36
                if self.frame >= len(self.frames36) - 1:
                    self.frame = 0
                    
            #Taunt
            if self.action == -5:
                self.targetFrame = self.frames36
                if self.frame >= len(self.frames36) - 1:
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







                            
















        



