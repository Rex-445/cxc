import sys, pickle, pyglet, random, time
from ball import *
from champion import *


def preload_image(image):
    img = pyglet.image.load("sprites/" + image + ".png")
    return img

class Ryu(Champion):
    def __init__(self, name):
        super().__init__(name)
        self.defualtSpeed = .2
        self.x = 0

        self.pos = [0,0,0]
        
        self.defualt2 = [name+"_mirror", name+"_2_mirror"]

        self.width, self.height = (79, 79)
        self.hitBox = [0,0, 30,30]
        self.body = [30,0,50,85]
        self.shadowOffset = [43,-5]
        

        #Vairations
        self.variation_images = [pyglet.sprite.Sprite(preload_image("Ryu/variation_A")), pyglet.sprite.Sprite(preload_image("Ryu/variation_B"))]
        self.variation_names = ["Dragon Born", "Possessed"]
        self.targetVariation = self.variation_names[0]
        self.variation_description = [self.variation_names[0] + ": Ryu gains access to multiple ranged abilities, his Super Dragon Ball restores 50 ragebar if it hits an enemy. Ryu also unlocks 'Dragon Stance', in this state he gains rapidly increasing ragebar and reduced cost for any special attack.",
                                      self.variation_names[1] + ": Ryu gives in to Tat'sui no' hado and becomes Anti-Ryu, gaining new abilities. Ryu also unlocks 'Rage Stance', in this tsate any successful projectile hit restores health to him depending on the damage dealt to opponents."]
        
        #Biography
        self.main_description = ["Ryu is the chosen warrior to protect the temple of Vaal, which was previously guarded by his Master, Eigen.",
                            " Eigen gave this responsibility to him. Invaders have tried to take over the temple but none have been ",
                            "able to withstand his Dragon Borne abilities. He remains vigilant, keeping it safe along side ",
                            "his closest companion, Ken."]
        self.description = ""

        for d in self.main_description:
            self.description += d

        #Variation_Skill
        self.auraTime = 0
        self.maxAuraTime = 100
        self.damageBuff = 20

        #Projectiles
        self.spawnFrame = 0
        self.balls = []
        self.vfx = []

        #Dialogues        
        self.talkTo = [["Ken", "D", "Audio/Champs/"+self.name+"/Dialogues/D.wav"], ["Ryu", "B", "Audio/Champs/"+self.name+"/Dialogues/B.wav"],
                       ["M.Bison", "G", "Audio/Champs/"+self.name+"/Dialogues/G.wav"], ["M.Bison", "F", "Audio/Champs/"+self.name+"/Dialogues/F.wav"],
                       ["Cammy", "B", "Audio/Champs/"+self.name+"/Dialogues/B.wav"], ["Cammy", "F", "Audio/Champs/"+self.name+"/Dialogues/F.wav"],
                       ["Cammy", "B", "Audio/Champs/"+self.name+"/Dialogues/F.wav"], ["Akuma", "E", "Audio/Champs/"+self.name+"/Dialogues/E.wav"],
                       ["Chun'Li", "D", "Audio/Champs/"+self.name+"/Dialogues/D.wav"], ["Chun'Li", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"],
                       ["Chun'Li", "F", "Audio/Champs/"+self.name+"/Dialogues/F.wav"]]
        
        self.respondTo = [["Ken", "D", "Audio/Champs/"+self.name+"/Dialogues/A.wav"], ["Ryu", "B", "Audio/Champs/"+self.name+"/Dialogues/C.wav"],
                          ["M.Bison", "B", "Audio/Champs/"+self.name+"/Dialogues/G.wav"], ["M.Bison", "A", "Audio/Champs/"+self.name+"/Dialogues/I.wav"],
                          ["M.Bison", "D", "Audio/Champs/"+self.name+"/Dialogues/H.wav"], ["M.Bison", "G", "Audio/Champs/"+self.name+"/Dialogues/G.wav"],
                          ["Cammy", "A", "Audio/Champs/"+self.name+"/Dialogues/A.wav"], ["Cammy", "A", "Audio/Champs/"+self.name+"/Dialogues/F.wav"],
                          ["Cammy", "B", "Audio/Champs/"+self.name+"/Dialogues/A.wav"], ["Cammy", "D", "Audio/Champs/"+self.name+"/Dialogues/A.wav"],
                          ["Akuma", "A", "Audio/Champs/"+self.name+"/Dialogues/I.wav"], ["Chun'Li", "A", "Audio/Champs/"+self.name+"/Dialogues/F.wav"],
                          ["Chun'Li", "D", "Audio/Champs/"+self.name+"/Dialogues/F.wav"], ["Anti-Ryu", "A", "Audio/Champs/"+self.name+"/Dialogues/I.wav"],
                          ["Anti-Ryu", "B", "Audio/Champs/"+self.name+"/Dialogues/F.wav"], ["Anti-Ryu", "C", "Audio/Champs/"+self.name+"/Dialogues/E.wav"],
                          ["Anti-Ryu", "D", "Audio/Champs/"+self.name+"/Dialogues/J.wav"], ["Anti-Ryu", "E", "Audio/Champs/"+self.name+"/Dialogues/K.wav"]]
        
        #Audio
        self.sound = pyglet.media.load("Audio/Champs/Ryu/dragon_ball.wav", streaming=False)
        self.voiceCD = 0
        self.voiceFrame = 0
        self.wins= [["First_Wins", ["Audio/Champs/Ryu/Wins/first_win.wav"]], ["End_Game", ["Audio/Champs/Ryu/Wins/end_gameA.wav",
                                                                                           "Audio/Champs/Ryu/Wins/end_gameB.wav"]],
                    ["Low_Health_Win", ["Audio/Champs/Ryu/Wins/low_health_win.wav"]]]

        #Combination
        self.skill = [["dfA", "Dragon Ball"], ["fdA", "Dragon Punch"], ["dbK", "Hurricane Kick"], ["dbSK", "Super Hurricane Kick"],
                      ["dfSA", "Super Dragon Ball"], ["bdfA", "Advanced Dragon Ball"], ["ddSS", "Dragon Born"]]

        ################ Animations ###############
        #Standing
        self.frames1 = [0, 1, 2, 3, 3]
        #Walking
        self.frames2 = [4, 5, 5, 6, 7, 7]
        #Weak Punch
        self.frames3 = [41, 42, 41]
        #Medium Punch
        self.frames4 = [43, 44, 43]
        #Close Weak Punch
        self.frames5 = [41, 45, 41]
        #Close Medium Punch
        self.frames6 = [46, 47, 46]
        #Left Uppercut
        self.frames6B = [49, 50, 51, 51, 50, 50, 50]
        #Right Uppercut
        self.frames6C = [46, 47, 46]
        #Crouch
        self.frames7 = [10]
        #Crouch Weak Punch
        self.frames8 = [52, 53, 52]
        #Crouch Medium Punch
        self.frames9 = [54, 55, 54]
        #Jump
        self.frames10 = [9]
        #Land
        self.frames11 = [10, 8, 8]
        #Getting Hit
        self.frames12 = [18, 18, 18, 18, 18]
        #Getting Hit
        self.frames13 = [19, 19, 19, 19, 19]
        #Getting Hit
        self.frames14 = [20, 20, 20, 20, 20]
        #Dragon Ball
        self.frames15 = [94, 95, 107, 108, 109, 109, 109, 109]
        self.frames15_ex = [110, 111, 112, 113, 114, 115, 114, 115, 116, 117, 118, 118, 118, 118, 118, 107, 95, 94]
        #Falling Bounce
        self.frames16 = [17, 17, 17, 22]
        #Lying
        self.frames17 = [24, 24, 24, 24, 24, 24, 24, 24, 24, 24]
        #Dragon Punch
        self.frames18 = [79, 101, 101, 102, 103]
        self.frames18_forcesX = [3, 0, 3, 0, 6]
        self.frames18_forcesY = [13, 0, 7, 0, 0]
        #Land From Dragon Punch
        self.frames19 = [104]
        #Weak Kick
        self.frames20 = [59, 60, 59]
        #Medium Kick
        self.frames21 = [61, 62, 63, 64, 65]
        #Crouch Weak Kick
        self.frames22 = [69, 70, 69]
        #Crouch Medium Kick
        self.frames23 = [69, 71, 69]
        #Hurricane Kick Start
        self.frames24 = [80, 81, 81]
        #Hurricane Kick Mid
        self.frames25 = [82, 83, 84, 85]
        self.freezeInAir = False
        self.kickLoop = 4
        #Hurricane Kick End
        self.frames26 = [86]
        #Super Hurricane Kick (Start)
        self.frames27 = [8, 8, 8, 8, 8, 8, 8, 80, 80, 80]
        #Super Dragon Ball
        self.frames28 = [94, 95, 95, 95, 95, 95, 95, 95, 95, 95, 95, 95, 107, 108, 109, 109, 109, 109,
                         109, 109, 109, 109]
        #Blocking Frames
        self.frames29 = [11, 12, 13, 14]
        self.frames29B = [50, 50, 50, 50, 50, 50, 50, 79, 100, 100, 100, 100]
        self.blockWait = 0


        
        #Win - To - Sub Animation Win
        self.frames30 = [87, 87, 87, 87]
        #Sub Animation Win
        self.frames31 = [105]
        #Sub Animation Win 2A
        self.frames32 = [88, 88, 89, 90, 90]
        #Sub Animation Win 2A (Loop)
        self.frames33 = [91, 92, 93, 92]
        self.frames34 = [79, 79, 79, 79, 79, 79, 79, 79]
        #Throw (Catching)
        self.frames37 = [29, 29, 29, 29, 29, 29]
        #Throw (Caught)
        self.frames38 = [29, 29, 30, 30, 30, 31, 31, 31, 32, 32]
        self.catchFrames = [23, 23.3, 23.3, 23.3, 23.6, 23.6, 23.6, 23.8, 23.8, 23.8, 23.8, 23.8]
        #Throw (Getting Caught)
        self.frames39 = [40, 39, 38, 22]
        
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
        #Dragon Born
        if self.state == "Grounded" or self.state == "Crouch":
            if skill == "Dragon Born" and self.stamina > 90 and self.auraTime <= 0:
                self.Play("Audio/Champs/Ryu/special.wav")
                self.frame = 0
                self.auraTime = self.maxAuraTime
                
        #Dragon Ball
        if self.state == "Grounded" or self.state == "Crouch":
            if skill == "Dragon Ball" and self.stamina > 20:
                self.stamina -= 20
                self.state = "Skill"
                self.Play("Audio/Champs/Ryu/dragon_ball.wav")
                self.frame = 0
                self.action = 8
                
        #Advanced Dragon Ball
        if self.state == "Grounded" or self.state == "Crouch":
            if skill == "Advanced Dragon Ball" and self.rageBar >= 200:
                self.state = "Skill"
                self.rageBar -= 200
                self.Play("Audio/Champs/Ryu/advanced_dragon_ball.wav")
                self.Play("Audio/Champs/Ryu/special.wav")
                self.frame = 0
                self.action = 8.5
                self.frameSpeed = .5

        #Super Dragon Ball
        if self.state == "Grounded" or self.state == "Crouch":
            if skill == "Super Dragon Ball" and self.rageBar >= 600 and self.auraTime > 0:
                self.rageBar -= 600
                self.faces.append(Face("sprites/Ryu/Ryu_Face.gif", self.direction))
                self.state = "Skill"
                self.superSkill = True 
                self.invincible = True                 
                self.vfx.append(Ball(pos=(self.pos[0] - 20, self.pos[1] - 20), name="VFX", loop=False, destroy=3, width=225, height=225,
                                      speed=.2, img="sprites/special.png", row=4, col=2))   
                self.PlayVoice(random.choice(["Audio/Champs/Ryu/dragon_ball_superA1.wav", "Audio/Champs/Ryu/dragon_ball_superA2.wav"]))
                self.Play("Audio/Champs/Ryu/special.wav")
                self.frame = 0
                self.action = 18
                #Variation Advantage
                if self.auraTime > 0:
                    self.rageBar += 200

        #Dragon Punch
        if self.state == "Grounded" or self.state == "Crouch":
            if skill == "Dragon Punch" and self.stamina > 40:
                self.stamina -= 40
                self.state = "Skill"
                self.PlayVoice("Audio/Champs/Ryu/dragon_punch.wav")
                self.frame = 0
                self.invincible = True
                self.action = 9
       
        #Hurricane Kick
        if skill == "Hurricane Kick":
            if self.state == "Airborne":
                self.state = "Skill"
                self.velocity = 0
                self.frame = 0
                self.action = 17.3
                
            if self.state == "Grounded" or self.state == "Crouch" and self.stamina > 40:
                self.stamina -= 40
                self.state = "Skill"
                self.Play("Audio/jump.wav")
                self.frame = 0
                self.invincible = True
                self.jumpHeight = 6
                self.action = 17
                self._height()
                
        #Super Hurricane Kick
        if skill == "Super Hurricane Kick" and self.rageBar >= 200:
##            if self.state == "Airborne":
##                self.state = "Skill"
##                self.vel[0] = -2
##                self.velocity = 0
##                self.frame = 0
##                self.action = 17.3
                
            if self.state == "Grounded" or self.state == "Crouch":
                self.rageBar -= 200
                self.state = "Skill"
                self.superSkill = True
                self.invincible = True
                self.vfx.append(Ball(pos=(self.pos[0] - 20, self.pos[1] - 20), name="VFX", loop=False, destroy=3, width=225, height=225,
                                      speed=.2, img="sprites/special.png", row=4, col=2))    
                choice = random.choice(["Audio/Champs/Ryu/spin_kick_superA1", "Audio/Champs/Ryu/spin_kick_superA2"])
                self.PlayVoice(choice + ".wav")
                self.Play("Audio/Champs/Ryu/special.wav")
                self.frame = 0
                self.action = 12
                #Variation Advantage
                if self.auraTime > 0:
                    self.rageBar += 100

    #Audio
    def Play(self, file):
        self.sound = pyglet.media.load(file, streaming=False)
        self.sound.play()

    def Update_Grab(self):
        if self.isGrabbing and self.targetGrabbed is not None:
            x = self.pos[0] + (self.hitBoxX[self.targetFrame[int(self.frame)]] * self.direction + (self.direction * -self.body[2])) 
            y = self.pos[1] + self.hitBoxY[self.targetFrame[int(self.frame)]] - 42
            if self.direction == -1:
                x += 0
            self.targetGrabbed.pos[0] = x
            self.targetGrabbed.pos[1] = y

    def Win(self):
        self.action = 20

    def Update_Alignment(self):
        #Update Alignment
        self.x = 0
        self.y = 0
        self.attacking_actions = [2, 2.5, 3, 3.5, 9, 10, 10.5, 11, 11.5, 12, 17.3, 12.5, 13, 13.5, 14, 14.5, 21, 22]        
        if self.direction == 1:
            self.x = self.pos[0] + self.alignX[self.targetFrame[int(self.frame)]]
            self.y = self.pos[1] + self.alignY[self.targetFrame[int(self.frame)]]
            
        if self.direction == -1:
            self.x = self.pos[0] - self.alignX[self.targetFrame[int(self.frame)]] + 120
            self.y = self.pos[1] + self.alignY[self.targetFrame[int(self.frame)]]
        if self.action not in self.attacking_actions:
            self.hitBox[0] = 10000
            self.hitBox[1] = 10000

    def Check_Combo(self):
        #Normal Combo
        check_combo = False
        key = None
        if len(self.key_combo) >= 3:
            check_combo = True
            key = self.key_combo

        if check_combo:
            for n in range(len(self.skill)):
                if key == self.skill[n][0]:
                    if self.state == "Airborne":
                        self.mixup = self.skill[n][0]
                        self.skill_combo_time = 0
                        self.key_combo = ""
                        break
                    self._skill(self.skill[n][1])
                    self.skill_combo_time = 0
                    self.key_combo = ""
                    break
                    
    def Update(self):
        if self.pause <= 0:
            self.frame += self.frameSpeed
            self.hitCD -= .09
            self.key_combo_time += .1
            if self.key_combo_time > 5:
                self.key_combo = ""

            self.auraTime -= .1
            if self.auraTime > 0:
                self.rageBar += .1
                
            self.UpdateActions()

            self.Check_Combo()

            #Updating Combos
            if self.voiceCD > 0:
                self.voiceCD -= .1
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
                    
            #Getting Hit A
            if self.action == 6:
                self.targetFrame = self.frames12
                if self.frame >= len(self.frames12) - 1:
                    self.action = 0
                    self.frame = 0
                    self.state = "Grounded"
                    
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
                if self.frame >= len(self.frames29B) - 1:
                    self.action = -100
                    self.state = "Grounded"
                    self.Play("Audio/Champs/Ryu/breaker.wav")
                    self.opponent.Get_Hit(attacker=self, damage=0, force=[10,8], typeHit="Ground")
                    self.frame = 0
                    self.superSkill = False
                    
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
                    
            #Dragon Ball
            if self.action == 8:
                self.targetFrame = self.frames15
                if self.targetFrame[int(self.frame)] == 109 and self.spawnFrame != 109:
                    self.spawnFrame = 109
                    #Positioning
                    x = self.pos[0] + 70
                    if self.direction == -1:
                        x = self.pos[0] + 10
                    y = self.pos[1] + 10
                    self.projectile_speed = 8
                    self.balls.append(Ball(pos=(x, y), velX=self.projectile_speed, width=82,  owner=self, speed=1, height=83, damage=40, direction=self.direction,
                                           img="sprites/Ryu/Balls/Medium_Energy_Ball.png", row=4, col=1))
                if self.frame >= len(self.frames15) - 1:
                    self.action = 0
                    self.state = "Grounded"
                    self.spawnFrame = 0
                    
            #Advanced Dragon Ball
            if self.action == 8.5:
                self.targetFrame = self.frames15_ex
                if self.targetFrame[int(self.frame)] == 117 and self.spawnFrame != 117:
                    self.spawnFrame = 117
                    #Positioning
                    x = self.pos[0] + 70
                    if self.direction == -1:
                        x = self.pos[0] + 10
                    y = self.pos[1] + 10
                    self.projectile_speed = 10
                    self.balls.append(Ball(pos=(x, y), velX=self.projectile_speed, width=82,  owner=self, height=80, speed=1, force=[9,5], damage=80, direction=self.direction,
                                           img="sprites/Ryu/Balls/Advanced_Energy_Ball.png", broken="sprites/Ryu/Balls/Advanced_Energy_Ball_broken.png",
                                           amber="sprites/Ryu/Balls/fire_particle3.png", row=4, col=1))
                if self.frame >= len(self.frames15_ex) - 1:
                    self.action = 0
                    self.state = "Grounded"
                    self.spawnFrame = 0
                    self.frameSpeed = .2
                    
            #Dragon Punch
            if self.action == 9:
                self.targetFrame = self.frames18
                self.force[0] = self.frames18_forcesX[int(self.frame)]
                self.force[1] = self.frames18_forcesY[int(self.frame)]
                if self.targetFrame[int(self.frame)] == 101:
                    self.jumpHeight = 15
                    self._height()
                    self.invincible = False
                    self.velocity = 3 * self.direction * -1
                if self.frame >= len(self.frames18) - 1:
                    self.frame = len(self.frames18) - 1
                    
            #Land From Dragon Punch
            if self.action == 9.5:
                self.targetFrame = self.frames19
                if self.frame >= len(self.frames19) - 1:
                    self.action = 5
                    self.force = [3,0]

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
                    self.action = 0
                    self.state = "Grounded"
                    
            #Super Hurricane Kick (Start)
            if self.action == 12:
                self.targetFrame = self.frames27
                if self.frame > len(self.frames27) - 3:
                    self.jumpHeight = 6
                    self._height()
                    self.vel[0] = -2
                if self.frame >= len(self.frames27) - 1:
                    self.Play("Audio/jump.wav")
                    self.PlayVoice("Audio/Champs/Ryu/spin_kick.wav")
                    self.kickLoop = 5
                    self.superSkill = False
                    self.action = 12.5
                    self.frame = 0
                
            #Super Hurricane Kick (Mid)
            if self.action == 12.5:
                self.force = [4.2,5]
                self.freezeInAir = True
                self.targetFrame = self.frames25
                if self.targetFrame[int(self.frame)] == 82 and self.voiceFrame != 82:
                    self.Play("Audio/big_wiff.wav")
                    self.voiceFrame = 82
                if self.frame >= len(self.frames25) - 1:
                    if self.kickLoop > 0:
                        self.voiceFrame = 0
                        self.kickLoop -= 1
                        self.frame = 0
                        if self.kickLoop > 2:
                            self.invincible = False
                    else:
                        self.kickLoop = 4
                        self.force = [3,0]
                        self.action = 17.5
                                        
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
     
            #Hurricane Kick (Start)
            if self.action == 17:
                self.targetFrame = self.frames24
                self.vel[0] = -2
                if self.frame >= len(self.frames24) - 1:
                    self.frame = 0
                    self.action = 17.3
                    self.PlayVoice("Audio/Champs/Ryu/superA1.wav", .5)
                    
            #Hurricane Kick (Mid)
            if self.action == 17.3:
                self.force = [4,0]
                self.freezeInAir = True
                self.targetFrame = self.frames25
                if self.targetFrame[int(self.frame)] == 82 and self.voiceFrame != 82:
                    self.Play("Audio/wiff.wav")
                    self.voiceFrame = 82
                if self.frame >= len(self.frames25) - 1:
                    if self.kickLoop > 0:
                        self.voiceFrame = 0
                        self.kickLoop -= 1
                        self.frame = 0
                        if self.kickLoop > 2:
                            self.invincible = False
                    else:
                        self.kickLoop = 6
                        self.force = [3,0]
                        self.action = 17.5
                    
            #Hurricane Kick (End)
            if self.action == 17.5:
                self.freezeInAir = False
                self.targetFrame = self.frames26
                if self.frame >= len(self.frames26) - 1:
                    self.frame = 0
                    self.action = -1

            #Shinku Dragon Ball
            if self.action == 18:
                self.targetFrame = self.frames28
                #Voice
                if self.targetFrame[int(self.frame)] == 107 and self.voiceFrame != 107:
                    self.voiceFrame = 107
                    self.superSkill = False
                    self.PlayVoice("Audio/Champs/Ryu/dragon_ball_superB.wav")
                #Spawn
                if self.targetFrame[int(self.frame)] == 109 and self.spawnFrame != 109:
                    self.spawnFrame = 109
                    #Positioning
                    x = self.pos[0] + 70
                    if self.direction == -1:
                        x = self.pos[0] + 30
                    y = self.pos[1] + 10
                    self.projectile_speed = 13
                    self.invincible = False
                    self.balls.append(Ball(pos=(x, y), velX=self.projectile_speed, width=82,  owner=self, height=80, speed=1, force=[9,5], damage=150, direction=self.direction,
                                           img="sprites/Ryu/Balls/Shinku_Ball2.png", broken="sprites/Ryu/Balls/Shinku_Broken.png",
                                           amber="sprites/Ryu/Balls/fire_particle.png", row=4, col=1))
                if self.frame >= len(self.frames28) - 1:
                    self.action = 0
                    self.state = "Grounded"
                    self.spawnFrame = 0
                    self.voiceFrame = 0
                    
                    
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
                self.isGrabbing = True
                self.targetFrame = self.frames38
                self.targetGrabbed.action = self.catchFrames[int(self.frame)]
                self.force = [8,5]
                if self.frame >= len(self.frames38) - 1:
                    self.targetGrabbed.isGrabbed = False
                    self.targetGrabbed.Get_Hit(attacker=self, damage=self.damage, force=self.force, typeHit="FireBall")
                    self.targetGrabbed = None
                    self.isGrabbing = False
                    self.action = 0
                    self.frame = len(self.frames38) - 1
                    
                    
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
                        percentage = (self.health / self.maxHealth) * 100
                        if percentage <= 20:
                            self.action = 20.9
                            self.Play(self.wins[2][1][0])
                            return
                        if self.winCount == 1:
                            self.Play(self.wins[0][1][0])
                        if self.winCount >= 2:
                            choice = random.choice([0,1])
                            self.Play(self.wins[1][1][choice])
                    
            #Sub Animation Win (Fist Up)
            if self.action == 20.2:
                self.targetFrame = self.frames31
                if self.frame >= len(self.frames31) - 1:
                    self.frame = 0
                    
            #Sub Animation Win 2A (Wind in my hair) - Start
            if self.action == 20.5:
                self.targetFrame = self.frames32
                if self.frame >= len(self.frames32) - 1:
                    self.action = 20.8
                    self.frame = 0
                    
            #Sub Animation Win 2B (Wind in my hair) - Loop
            if self.action == 20.8:
                self.targetFrame = self.frames33
                if self.frame >= len(self.frames33) - 1:
                    self.frame = 0
                    
            #Low Health Win
            if self.action == 20.9:
                self.targetFrame = self.frames30
                if self.frame >= len(self.frames30) - 1:
                    self.frame = 0

            #Taunt
            if self.action == -5:
                self.targetFrame = self.frames34
                if self.frame >= len(self.frames34) - 1:
                    self.frame = 0
                    self.action = 0
                    
            #Respond Taunt
            if self.action == -6:
                self.targetFrame = self.frames34
                if self.frame >= len(self.frames34) - 1:
                    self.frame = 0
                    self.action = 0
                    
        self.Update_Grab()
        self.Update_Graphics()

















        



