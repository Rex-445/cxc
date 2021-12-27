import sys, pickle, pyglet, random, time
from ball import *
from champion import Champion


def preload_image(image):
    img = pyglet.image.load("sprites/" + image + ".png")
    return img

class Monk(Champion):
    def __init__(self, name):
        super().__init__(name)
        self.defualtSpeed = .15
        self.x = 0

        self.pos = [0,0,0]
        self.rageBar = 600
        
        self.defualt2 = [name+"_mirror", name+"_2_mirror"]

        self.hitBox = [0,0, 30,30]
        self.body = [30,0,50,85]
        self.shadowOffset = [20,-5]

        #Vairations
        self.variation_images = [pyglet.sprite.Sprite(preload_image("Ken/variation_A")), pyglet.sprite.Sprite(preload_image("Ken/variation_B"))]
        self.variation_names = ["Dragon Born", "Dragon Flame"]
        self.variation_description = ["Ken gains access to multiple mixup skills and throws projectiles",
                                      "Ken's attacks burns enemies dealing damage over time. Enemies ablaze take more damage from Ken's abilities"]
        
        #Audio
        self.sound = pyglet.media.load("Audio/Champs/Ryu/dragon_ball.wav", streaming=False)
        self.voiceCD = 0
        self.voiceFrame = 0
        self.wins= [["First_Wins", ["Audio/Champs/Ryu/Wins/first_win.wav"]], ["End_Game", ["Audio/Champs/Ryu/Wins/end_gameA.wav",
                                                                                           "Audio/Champs/Ryu/Wins/end_gameB.wav"]],
                    ["Low_Health_Win", ["Audio/Champs/Ryu/Wins/low_health_win.wav"]]]

        #Combination
        self.skill = [["dfA", "Shaolin Palm"]]

        ################ Animations ###############
        #Standing
        self.frames1 = [0, 1, 2, 3, 3]
        #Walking
        self.frames2 = [4, 5, 5, 6, 7, 7]
        #Weak Punch
        self.frames3 = [12, 13, 12]
        #Medium Punch
        self.frames4 = [10, 11, 10]
        #Close Weak Punch
        self.frames5 = [41, 45, 41]
        #Close Medium Punch
        self.frames6 = [46, 47, 46]
        #Crouch
        self.frames7 = [10]
        #Crouch Weak Punch
        self.frames8 = [52, 53, 52]
        #Crouch Medium Punch
        self.frames9 = [54, 55, 54]
        #Jump
        self.frames10 = [62]
        #Land
        self.frames11 = [61, 61]
        #Getting Hit
        self.frames12 = [120, 121, 121, 122, 122]
        #Getting Hit
        self.frames13 = [123, 124, 124, 122, 122]
        #Getting Hit
        self.frames14 = self.frames13
        #Falling Bounce
        self.frames16 = [35, 35, 35, 34]
        #Falling Bounce
        self.frames17 = [34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34]
        
        #Skills
        #Shaolin Palm
        self.frames28 = [8, 9, 16, 17, 18, 19, 29, 29, 29, 29]
        #Blocking Frames
        self.frames29 = [56, 57, 56, 57]
        self.frames29B = [50, 50, 50, 50, 50, 50, 50, 79, 100, 100, 100, 100]
        self.blockWait = 0


        
        #Win - To - Sub Animation Win
        self.frames30 = [8, 8, 8, 8]
        #Sub Animation Win
        self.frames31 = [9]
        #Sub Animation Win 2A
        self.frames32 = [8, 9, 16, 17, 18, 19]
        #Sub Animation Win 2A (Loop)
        self.frames33 = [29, 29]

        #Taunt
        self.frames34 = [79, 79, 79, 79, 79, 79, 79, 79]
        #Throw (Catching)
        self.frames37 = [12, 12, 13, 13, 13, 13]
        #Throw (Caught)
        self.frames38 = [29, 29, 30, 30, 30, 31, 31, 31, 32, 32]
        self.catchFrames = [23, 23.3, 23.3, 23.3, 23.6, 23.6, 23.6, 23.8, 23.8, 23.8, 23.8, 23.8]
        #Throw (Getting Caught)
        self.frames39 = [46, 55, 40, 41]

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


        #Align On Axes
        data = pickle.load(open("data/" + str(name) + ".txt", "rb"))
        self.alignX = data[0]
        self.alignY = data[1]
        self.hitBoxX = data[2]
        self.hitBoxY = data[3]
        self.velX = []
        self.velY = []
        for vel in range(180):
            self.velX.append(0)
            self.velY.append(0)
            self.alignX.append(0)
            self.alignY.append(0)
            self.hitBoxX.append(0)
            self.hitBoxY.append(0)
        
        
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
        #Shaolin Palm
        if self.state == "Grounded" or self.state == "Crouch":
            if skill == "Shaolin Palm":
                self.state = "Skill"
                self.frame = 0
                self.action = 8

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
            self.x = self.pos[0] - self.alignX[self.targetFrame[int(self.frame)]] + 80
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
                    self.action = 4

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
                    self.action = 4
                    
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
                    self.action = 0
                    self.state = "Grounded"
                    choice = random.choice(["Audio/Champs/Ryu/Grunt/45e.wav", "Audio/Champs/Ryu/Grunt/47e.wav"])
                    self.Play(choice)
                    self.opponent.Get_Hit(attacker=self, damage=0, force=[15,5], typeHit="Ground")
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
                    
            #Shaolin Palm
            if self.action == 8:
                self.targetFrame = self.frames28
                if self.targetFrame[int(self.frame)] == 19 and self.spawnFrame != 19:
                    self.spawnFrame = 19
                    self.PlayVoice("Audio/Champs/Monk/Grunt/A.wav")
                    self.Play("Audio/fire_ball.wav")
                    #Positioning
                    x = self.pos[0] + 70
                    if self.direction == -1:
                        x = self.pos[0] + 10
                    y = self.pos[1] + 10
                    self.balls.append(Ball(pos=(x, y), velX=60, width=82,  owner=self, height=82, speed=1, force=[9,5], damage=80, direction=self.direction,
                                           img="sprites/Monk/Ball/monk_wind_ball.png", broken="sprites/Monk/Ball/monk_wind_ball.png", row=4, col=1))
                    #VFX
                    self.vfx.append(Broken(pos=(x, 250), speed=.1, velX=0, row=4, col=1, direction=self.direction,
                                           img="sprites/Monk/Ball/monk_wind.png"))
                if self.frame >= len(self.frames28) - 1:
                    self.action = 0
                    self.state = "Grounded"
                    self.spawnFrame = 0
                    self.frameSpeed = .2

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
                    self.action = 4

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
                    self.action = 4
                                        
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
                self.action = 4
                    
            #Crouch Block (Hit)
            if self.action == 14.5:
                self.action = 4
                    
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
                            return
                    
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

















        



