import sys, pickle, pyglet, random, time, os
from ball import *


def preload_image(image):
    img = pyglet.image.load("sprites/" + image + ".png")
    return img


class AfterImage():
    def __init__(self, pos=(0,0), image="image", direction=1):
        self.pos = list(pos)
        self.sprite = image
        self.alpha = 255
        self.alive = True
        self.sprite.scale_x = direction

    def update(self):
        self.alpha -= 5
        self.sprite.x = self.pos[0]
        self.sprite.opacity = self.alpha
        self.alive = self.alpha > 0


class Face():
    def __init__(self, anim="Image", direction=1, time=40):
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load_animation(anim), y=150)
        self.time = time
        self.alive = True
        
    def update(self):
        self.time -= 1
        self.alive = self.time > 0
        if self.alive:
            self.sprite.draw()
        

        
class Champion(): 
    def __init__(self, name):
        self.sprite = pyglet.sprite.Sprite(preload_image(name+"/"+name))
        self.select_head = pyglet.sprite.Sprite(pyglet.image.load("sprites/Heads/"+name+"_head.png"))
        self.hit_sprite = pyglet.sprite.Sprite(preload_image("hitBox"))
        self.body_sprite = pyglet.sprite.Sprite(preload_image("body"))
        self.shadow = pyglet.sprite.Sprite(pyglet.image.load("bg/sp/s.png"))
        self.head = "sprites/"+name+"/small.png"
        self.name = name
        #UI Icon
        self.icon = pyglet.sprite.Sprite(pyglet.image.load("UI/p1.png"))
        self.faces = []
        self.defualt = ["sprites/"+name+"/"+name, "sprites/"+name+"/"+name+"_2"]
        self.x = 0

        self.pos = [0,0,0]
        self.opponent = None
        
        self.defualt2 = [name+"_mirror", name+"_2_mirror"]

        self.width, self.height = (79, 79)
        self.hitBox = [0,0, 30,30]
        self.body = [30,0,50,85]
        self.shadowOffset = [43,-5]
        self.alignmentOffset = [0,0]

        #Audio
        sounds = ["Audio/Sys/Game/Bar.wav", "Audio/Sys/Game/Bar2.wav"]

        #Projectiles
        self.spawnFrame = 0
        self.balls = []
        self.vfx = []

        #After Image
        self.maxImageTime = 3
        self.inAfterImage = False
        self.imageTime = self.maxImageTime
        self.afterImage = []

        #Audio
        self.voiceFrame = 0
        self.voice = pyglet.media.Player()        
        self.talkTo = []
        self.respondTo = []
        self.talking = False
        self.talkTime = 0
        self.maxTalkTime = 100
        self.talkChoice = ""
        self.sound = pyglet.media.load("Audio/Champs/Ryu/dragon_ball.wav", streaming=False)
        self.voiceCD = 0
        self.grunts = self.LoadAllFilesFromDirectory("Audio/Champs/"+name+"/Grunt")
        self.hurts = self.LoadAllFilesFromDirectory("Audio/Champs/"+name+"/Hurt")
        self.wins= [["First_Wins", ["Audio/Champs/Ryu/Wins/first_win.wav"]], ["End_Game", ["Audio/Champs/Ryu/Wins/end_gameA.wav",
                                                                                           "Audio/Champs/Ryu/Wins/end_gameB.wav"]],
                    ["Low_Health_Win", ["Audio/Champs/Ryu/Wins/low_health_win.wav"]]]
        
        self.loseImage = pyglet.sprite.Sprite(pyglet.image.load("sprites/" + self.name + "/lose.png"))
        self.winImage = pyglet.sprite.Sprite(pyglet.image.load("sprites/" + self.name + "/win.png"))
        self.finishImage = self.winImage
        
        self.combos = [self.LoadAllFilesFromDirectory("Audio/Champs/"+self.name+"/Wins/Combos/")]
        self.championTaunt = {}
        self.dir = "Audio/Champs/" + self.name
        
        #User Controller
        #Blocking
        self.blockRight = False
        self.blockLeft = False  
        self.isControlled = False
        self.canControl = True
        self.down = False
        self.up = False
        self.left = False
        self.right = False
        self.pause = False
        self.hitPunch = False
        self.hitKick = False
        #Directinal Blocks
        self.moveLeft = False
        self.moveRight = False

        #Combos
        self.vrest = 0
        self.maxVrest = 15
        self.hitCombo = 0
        self.comboEnd = False
        self.mixup = ""

        #Biography
        self.description = ""
        self.variation_images = []
        self.targetVariation = None
        
        #status of the character
        #Blinking
        self.blinkTime = 0
        self.canDraw = True
        self.blinking = True
        self.blinkDuration = 0

        #Ultra
        self.ultra = False
        self.ultraCount = 0

        #Burning
        self.burning = False
        self.burnTime = 0
        self.burnSheet = False

        
        self.action = 0
        self.healLength = 0
        self.parry = False
        self.EX = False
        self.EXOn = False
        self.invincible = False
        self.canJumpAttack = False
        self.speed = 1.6
        self.gruntHit = 0
        self.gruntCount = 6
        self.hurtHit = 0
        self.hurtCount = 6
        self.state = "Grounded"
        self.maxHealth = 500
        self.bloodLine = 500
        self.damageDealt = 0
        self.health = self.maxHealth
        self.maxRageBar = 600
        self.rageBar = 200
        self.stamina = 100
        self.staminaSpeed = 0
        self.damage = 15
        self.bonusDamage = 0
        self.addTime = 0
        self.hitCD = 0
        self.maxHitCD = 1
        #HitBox Type
        self.isGrabbed = False
        self.isGrabbing = False
        self.targetGrabbed = None
        self.unBreakable = False
        self.toGrab = False
        self.alive = True
        self.win = False
        self.superSkill = False
        self.backSpring = False
        self.winCount = 1
        self.victimAction = 0

        #Physics Variables
        self.cameraShake = 0
        self.typeHit = "Damage"
        self.vel = [0,0]
        self.jumpHeight = 9
        self.gravity = .7
        self.maxGravity = .7
        self.projectile_speed = 8
        self.ground = 100
        self.jump = False
        #Falling
        self.fall = False
        self.fallHeight = 6
        self.stamina = 100
        self.bounce = 5
        self.velocity = 0
        #Hitbox
        self.force = [3,0]

        #Combination
        self.skill = []
        
        self.key_combo = ""
        self.breaker_input = ""
        self.key_combo_time = 0

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
        #Crouch
        self.frames7 = [10]
        #Crouch Weak Punch
        self.frames8 = [52, 53, 52]
        #Crouch Medium Punch
        self.frames9 = [54, 55, 54]
        #BurnFrame
        self.burnFrames = [0,0]
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
        #Falling Bounce
        self.frames16 = [22]
        #Lying
        self.frames17 = [24, 24, 24, 24, 24, 24, 24, 24, 24, 24]
        #Dragon Punch
        self.frames18 = [79, 101, 101, 102, 103]
        self.frames18_forcesX = [5, 0, 4, 0, 6]
        self.frames18_forcesY = [16, 0, 7, 0, 0]
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
        self.kickLoop = 5
        self.maxKickLoop = 5
        #Hurricane Kick End
        self.frames26 = [86]
        #Super Hurricane Kick (Start)
        self.frames27 = [8, 8, 8, 8, 8, 8, 8, 80, 80, 80]
        #Super Dragon Ball
        self.frames28 = [94, 95, 95, 95, 95, 95, 95, 95, 95, 95, 95, 95, 107, 108, 109, 109, 109, 109,
                         109, 109, 109, 109]
        #Blocking Frames
        self.frames29 = [11, 12, 13, 14]
        self.blockWait = 0
        #Win - To - Sub Animation Win
        self.frames30 = [87, 87, 87, 87]
        #Sub Animation Win
        self.frames31 = [105]
        #Sub Animation Win 2A
        self.frames32 = [88, 88, 89, 90, 90]
        #Sub Animation Win 2A (Loop)
        self.frames33 = [91, 92, 93, 92]
        #Throw (Getting Caught)
        self.frames39 = [40, 39, 38, 22]

        #character frames
        self.cell = []
        self.flip = []
        self.targetCell = self.cell
        self.aura = []
        self.Ex_aura = []
        self.targetFrame = self.frames1
        self.frameSpeed = .2
        self.defualtSpeed = self.frameSpeed
        self.row = 0
        self.col = 0
        self.sounds = ["sounds/020.wav"]
        self.sndTimer = 1
        self.frame = 0
        self.direction = 1
        self.fallDirection = -1
        self.dvx = 0
        self.dvy = 0


        #Align On Axes
        data = pickle.load(open("data/Characters/" + str(name) + ".txt", "rb"))
        self.alignX = data[0]
        self.alignY = data[1]
        self.hitBoxX = data[2]
        self.hitBoxY = data[3]
        self.hitBoxOffsetX = -30
        self.hitBoxOffsetY = 0
        
    def LoadAllFilesFromDirectory(self, path):
        return os.listdir(path)

    #function was made to make GameObject's Initilization easier       
    def __init__self__(self, row, col, width, height, img):
        img = pyglet.image.load(img)
        sprite_sheet = pyglet.image.ImageGrid(img, col, row, item_width=width, item_height=height)

        cell = sprite_sheet
        counting = len(cell)
        for d in range(col):
            counting -= row
            for n in range(row):
                self.cell.append(cell[counting + n])
        self.targetCell = self.cell

        #Burning Frames 0 - Real Fire, 1 - Blue Fire, 2 - Pink Fire, 3 - Dark Blue Fire
        self.allBrunFrames = [[len(self.cell) - 8, len(self.cell) - 7], [len(self.cell) - 4, len(self.cell) - 3],
                              [len(self.cell) - 6, len(self.cell) - 5], [len(self.cell) - 2, len(self.cell) - 1]]
        self.burnFrames = self.allBrunFrames[2]
        
        #Dash
        self.frames10_B = self.frames10

    #function was made to make GameObject's Initilization easier       
    def __init__aura__(self, row, col, width, height, img):
        img = pyglet.image.load(img)
        sprite_sheet = pyglet.image.ImageGrid(img, col, row, item_width=width, item_height=height)

        cell = sprite_sheet
        counting = len(cell)
        for d in range(col):
            counting -= 10
            for n in range(row):
                self.aura.append(cell[counting + n])

    #function was made to make GameObject's Initilization easier       
    def __init__ex__aura__(self, row, col, width, height, img):
        img = pyglet.image.load(img)
        sprite_sheet = pyglet.image.ImageGrid(img, col, row, item_width=width, item_height=height)

        cell = sprite_sheet
        counting = len(cell)
        for d in range(col):
            counting -= 10
            for n in range(row):
                self.Ex_aura.append(cell[counting + n])
        
    def KeyDown(self, type):
        if self.isControlled:
            if self.key_combo_time > 5:
                self.key_combo_time = 0

            #Movement and animation
            if type == "Right":
                self.moveRight = True
                if self.action == 0 or self.action == 1 or self.action == 4:
                    self.right = True
                if self.direction == 1:
                    self.key_combo += "f"
                    #Add Mixup
                    if self.state == "Airborne":
                        self.mixup += "f"
                        
                if self.direction == -1:
                    self.key_combo += "b"
                    
                    #Add Mixup
                    if self.state == "Airborne":
                        self.mixup += "b"
                    
            if type == "Left":
                self.moveLeft = True
                if self.action == 0 or self.action == 1 or self.action == 4:
                    self.left = True
                if self.direction == 1:
                    self.key_combo += "b"
                    #Add Mixup
                    if self.state == "Airborne":
                        self.mixup += "b"
                        
                if self.direction == -1:
                    self.key_combo += "f"
                    #Add Mixup
                    if self.state == "Airborne":
                        self.mixup += "f"
                    
            if type == "Down":
                self.key_combo += "d"
                #Add Mixup
                if self.state == "Airborne":
                    self.mixup += "d"
                self._down()
                
            if type == "Up":
                self.up = True
        
    def KeyUp(self, type):
        if type == "Right":
            self.right = False
            self.moveRight = False
            self.blockRight = False
        if type == "Left":
            self.left = False
            self.moveLeft = False
            self.blockLeft = False
        if type == "Down":
            self.down = False
            if self.action == 4:
                self.action = 0
                self.state = "Grounded"
        if type == "Up":
            self.up = False

        keys = ["WP", "MP"]
        if type in keys:
            self.hitPunch = ""

        keys = ["WK", "MK"]
        if type in keys:
            self.hitKick = ""

    #Functions
    def _up(self):
        self.key_combo = ""
        actions = [0, 1]
        if self.state == "Grounded" and self.action in actions:
            if self.right:
                self.velocity = -5
            if self.left:
                self.velocity = 5
            self._jump()
            
    def _down(self):
        self.down = True
        
    def _left(self):
        self.pos[0] -= self.speed
    def _right(self):
        self.pos[0] += self.speed

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
        pass


    #Audio
    def Play(self, file):
        self.sound = pyglet.media.load(file, streaming=False, volume=.7)
        self.sound.play()

    def Win(self):
        self.action = 20
        self.frame = 0


    def Break(self):
        pass

    def Taunt(self):
        self.PlayVoice("Audio/Champs/Ken/Wins/combo4.wav")
                            
    def PlayVoice(self, file=None, volume=.7):
        self.voice = pyglet.media.Player()
        media = pyglet.media.load(file, streaming=False)
        self.voice.queue(media)
        self.voice.volume = volume
        self.voice.play()

    def Attack_Punch(self, type):
        dodge_states = [2, 2.5, 3, 3.5]
        if self.isControlled:            
            if type == "SP":
                self.breaker_input += "S"
                if self.key_combo != "":
                    self.key_combo += "S"
                    
                    #Add Mixup
                    if self.state == "Skill":
                        self.mixup += "S"
            if type == "WP" or type == "MP":
                if self.key_combo != "":
                    self.key_combo += "A"
                    
                    #Add Mixup
                    if self.state == "Airborne":
                        self.mixup += "A"
                
            if self.action not in dodge_states and self.isGrabbing == False:
                self.hitPunch = type   
                #Weak Punch
                if type == "WP":
                    self.breaker_input = ""
                    self.damage = 5
                    if self.state == "Grounded" and self.action != 2 and self.action != 13.5:                        
                        #Check For Stamina
                        if self.stamina > 15 and self.Break_Stamina() == False:
                            self.stamina -= 15
                            self.staminaSpeed = 0
                        else:
                            return
                        
                        self.Play("Audio/wiff.wav")
                        self.action = 2
                        self.typeHit = "Damage"
                        self.frame = 0
                        self.force = [3,0]
                    if self.state == "Crouch" and self.action != 2.5 and self.action != 14.5:                    
                        #Check For Stamina
                        if self.stamina > 15 and self.Break_Stamina() == False:
                            self.stamina -= 10
                            self.staminaSpeed = 0
                        else:
                            return
                        
                        self.frame = 0
                        self.action = 2.5
                        self.typeHit = "Damage"   
                        self.force = [3,0]    
                
                #Medium Punch
                if type == "MP":
                    self.damage = 15
                    self.breaker_input = ""
                    if self.state == "Grounded" and self.action != 3 and self.action != 13.5:                    
                        #Check For Stamina
                        if self.stamina > 15 and self.Break_Stamina() == False:
                            self.stamina -= 10
                            self.staminaSpeed = 0
                        else:
                            return
                        
                        self.Play("Audio/wiff.wav")
                        self.action = 3
                        self.frame = 0
                        self.typeHit = "Damage"  
                        self.force = [3,0]
                        
                    if self.state == "Crouch" and self.action != 3.5 and self.action != 14.5:                    
                        #Check For Stamina
                        if self.stamina > 15 and self.Break_Stamina() == False:
                            self.stamina -= 15
                            self.staminaSpeed = 0
                        else:
                            return
                        
                        self.Play("Audio/wiff.wav")
                        self.action = 3.5
                        self.frame = 0
                        self.typeHit = "Damage"  
                        self.force = [3,0] 
                #Grabbing
                if type == "IP":
                    grabs = [21, 22]
                    if self.state == "Grounded" and self.action not in grabs:
                        self.action = 21
                        self.frame = 0
            
    def Attack_Kick(self, type):
        dodge_states = [10, 10.5, 11, 11.5]
        self.force = [3,0]
        if self.isControlled:            
            if type == "SK":
                self.breaker_input += "S"
                if self.key_combo != "":
                    self.key_combo += "S"
                    
                    #Add Mixup
                    if self.state == "Skill":
                        self.mixup += "S"
                        
            if type == "WK" or type == "MK":
                if self.key_combo != "":
                    self.key_combo += "K"
                    
                    #Add Mixup
                    if self.state == "Airborne":
                        self.mixup += "K"
                        
            if self.action not in dodge_states and self.isGrabbing == False:
                self.hitKick = type
                #Weak Kick
                if type == "WK":
                    self.damage = 5
                    self.breaker_input = ""
                    if self.state == "Grounded" and self.action != 10 and self.action != 13.5:                    
                        #Check For Stamina
                        if self.stamina > 15 and self.Break_Stamina() == False:
                            self.stamina -= 10
                            self.staminaSpeed = 0
                        else:
                            return
                        
                        self.action = 10
                        self.typeHit = "Damage"
                        self.frame = 0       
                        self.force = [3,0]
                        
                    if self.state == "Crouch" and self.action != 10.5 and self.action != 14.5:                    
                        #Check For Stamina
                        if self.stamina > 15 and self.Break_Stamina() == False:
                            self.stamina -= 10
                            self.staminaSpeed = 0
                        else:
                            return
                        
                        self.frame = 0
                        self.action = 10.5
                        self.typeHit = "Damage"
                        self.force = [3,0]
                
                #Medium Kick
                if type == "MK":
                    self.damage = 15
                    self.breaker_input = ""
                    if self.state == "Grounded" and self.action != 11 and self.action != 13.5:                    
                        #Check For Stamina
                        if self.stamina > 15 and self.Break_Stamina() == False:
                            self.stamina -= 15
                            self.staminaSpeed = 0
                        else:
                            return
                        
                        self.action = 11
                        self.typeHit = "Damage"
                        self.frame = 0
                        self.force = [3,0]
                        
                    if self.state == "Crouch" and self.action != 11.5 and self.action != 14.5:                    
                        #Check For Stamina
                        if self.stamina > 15 and self.Break_Stamina() == False:
                            self.stamina -= 15
                            self.staminaSpeed = 0
                        else:
                            return
                        
                        self.action = 11.5
                        self.frame = 0
                        self.typeHit = "Damage"
                        self.force = [3,0]
                        
    
    def Update_Alignment(self):
        pass

    def UpdateActions(self):
        dodge_states = [-1, 2, 2.5, 3, 3.5, 9, 10, 10.5, 11, 11.5, 12, 12.8, 12.5, 13, 13.5, 14, 14.5, 17.3, 19, 19.1, 19.2, 21, 22]  
        if self.action not in dodge_states:
            if self.right == True:
                if self.state == "Grounded":
                    self.action = 1
                    self._right()
                
            if self.left == True:
                if self.state == "Grounded":
                    self.action = 1
                    self._left()

        #Reset action in case both axes are not pressed anymore
        if self.right == False and self.left == False and self.action == 1:
            self.action = 0

        if self.up == True:
            if self.state != "Crouch":
                self._up()

        if self.down == True:
            actions = [2, 2.5, 3, 3.5, 10, 10.5, 11, 11.5, 7.9]
            condition = self.action not in actions and self.state != "Skill" and self.isGrabbing == False and self.state != "Airborne" and self.state != "Hit"
            if condition:
                self.action = 4
                self.state = "Crouch"

    #Damage
    def Hit_Connect(self, victim):
        victim.Get_Hit(attacker=self, damage=self.damage, force=self.force, typeHit=self.typeHit)

    def Get_Hit(self, attacker=None, typeHit="Damage", damage=0, force=[0,0]): 
        if typeHit == "Block":
            self.Play("Audio/block.wav")
            self.opponent.rageBar += 5
            self.rageBar += 5
            self.health -= damage/2
            self.blockWait = -5
            self.hitCD = self.maxHitCD
            self.vel[0] = force[0]
            self.vrest += 5
            self.action = 13.5
            self.frame = 1
            if self.state == "Crouch":
                self.action = 14.5
                self.frame = 3
            if self.alive == False:
                if self.canControl:
                    self.isControlled = False
                    self.Play("Audio/Combat/K.O.mp3")
                    self.canControl = False
                if force[1] == 0:
                    force[1] = 5
                    force[0] += 7
                if force[1] > 0:
                    self.vel[1] = force[1]
                    self.fall = True
            alive = self.health > 0
            if not alive and self.opponent.win == False:
                self.Get_Hit(self, "none", 5)
            return

        self.voice._set_playing(False)
        self.frameSpeed = self.defualtSpeed
        self.vel[1] = 0
        self.vel[0] = force[0]
        self.combo = 0
        self.cameraShake = 0
        self.opponent.maxHitCD = 1
        self.isGrabbing = False
        self.parry = False
        self.invincible = False
        if self.opponent.isGrabbed:
            self.opponent.isGrabbed = False
            self.opponent.action = -1
            self.fallHeight = 3
            self.opponent.fall = True
            self.opponent.isControlled = True
            self.frame = len(self.frames38) - 1


        #Breaker 
        if "SS" in self.breaker_input and self.rageBar > 200:
            if self.state == "Grounded":
                self.rageBar -= 200
                self.breaker_input = ""
                self.invincible = True
                self.action = 6.7
                self.stamina = 0
                self.staminaSpeed = -1
                self.opponent.stamina = 0
                self.opponent.staminaSpeed = -1
                self.superSkill = True              
                self.vfx.append(Ball(pos=(self.pos[0] - 20, self.pos[1] - 20), name="VFX", loop=False, destroy=3, width=225, height=225,
                                      speed=.2, img="sprites/special.png", row=4, col=2))
                self.Play("Audio/Champs/Ryu/special.wav")
                self.state = "Hit"
                self.vel[0] = 0
                self.opponent.action = 6
        #Taking Damage
        else:
            if self.blinkDuration <= 0:
                self.blinkDuration = 5
            if self.action != 6.7:
                #Add Rage Points
                if self.hitCombo > 1:
                    self.stamina += 3
                    self.opponent.rageBar += 5
                    
                if self.hitCombo > 5:
                    self.hurtHit -= 1
                    if self.hurtHit < 0:
                        self.hurtHit = self.hurtCount
                        self.PlayVoice("Audio/Champs/"+self.name+"/Hurt/"+random.choice(self.hurts))

                self.rageBar += 5
                force = force
                self.hitCombo += 1
                self.velocity = 0
                self.damageDealt += damage
                self.vrest = 10
                if attacker.bonusDamage > 0:
                    self.health -= damage + attacker.bonusDamage
                else:
                    self.health -= damage
                #Check for bonus Damage
                self.alive = self.health > 0 
                if self.jump and self.alive == True:
                    if force[1] == 0:
                        force[1] += 3
                    else:
                        force[1] = 5
                    self.jump = False

                #Check For Death
                if self.alive == False:
                    if self.canControl:
                        self.Play("Audio/Combat/K.O.mp3")
                        self.canControl = False
                    if force[1] == 0:
                        force[1] = 5
                        force[0] += 7
                    
                #Physics
                self.vel[0] = force[0]
                if force[1] > 0:
                    self.vel[1] = force[1]
                    self.fall = True
                if force[1] < 0:
                    self.vel[1] = force[1]
                    self.fall = True

                #Combos
                self.hitCD = self.maxHitCD
                action = [6, 6.3, 6.5]
                self.action = random.choice(action)
                self.frame = 0
                self.state = "Hit" 
                self.blinkDuration = 0

                #Sounds
                #Basic Hit
                if typeHit == "Damage":
                    self.Play("Audio/hit.wav")
                #Fireball Projectile
                if "FireBall" in typeHit:
                    self.Play("Audio/fire_ball.wav")
                    self.Play("Audio/flame.wav")
                    if typeHit == "FireBall2":
                        self.burnSheet = True
                        self.invincible = True
                    if self.opponent.name == "Ken":
                        self.burnTime = 20
                #Fire Sound
                if typeHit == "Fire":
                    self.Play("Audio/hit.wav")
                    self.Play("Audio/flame.wav")
                    self.burnTime = 20
                    self.burnSheet = True
                    self.invincible = True
                    self.burnFrames = self.allBrunFrames[0]
                #Psyco Fire
                if typeHit == "PsycoFire":
                    self.Play("Audio/hit.wav")
                    self.Play("Audio/flame.wav")
                    self.burnSheet = True
                    self.invincible = True
                    self.burnFrames = self.allBrunFrames[2]
                #Throw Sound
                if typeHit == "Throw":
                    self.Play("Audio/wiff.wav") 
                #Ground Hit Sound
                if typeHit == "Ground":
                    self.Play("Audio/ground.wav")

                #Damage Over time
                if typeHit == "Burn":
                    self.Play("Audio/hit.wav")
                    self.Play("Audio/flame.wav")
                    self.burnTime = 20

    def Mixup_Combo(self): 
        #Big Mixup
        if len(self.mixup) > 0:
            for n in range(len(self.skill)):
                if self.mixup == self.skill[n][0]:
                    self._skill(self.skill[n][1])
                    self.mixup = ""
                    self.skill_combo_time = 0
                    self.key_combo = ""
                    self.hitKick = ""
                    break      

    def Check_Combo(self):
        #Normal Combo
        check_combo = False
        key = None
        if len(self.key_combo) >= 1:
            check_combo = True
            key = self.key_combo

        if check_combo:
            for n in range(len(self.skill)):
                if key == self.skill[n][0]:
##                    self.opponent.hitCD = -1
                    self.hitPunch =  ""
                    self.hitKick = ""
                    self.staminaSpeed = 0
                    self.opponent.hitCD = self.opponent.maxHitCD
                    if self.state == "Airborne" or self.state == "Skill":
                        self.mixup = self.skill[n][0]
                        self.skill_combo_time = 0
                        self.key_combo = ""
                        break
                    self._skill(self.skill[n][1])
                    self.skill_combo_time = 0
                    self.key_combo = ""
                    break
                
    def Break_Stamina(self):
        key = self.key_combo            
        for n in range(len(self.skill)):
            if key == self.skill[n][0]:
                return True
        return False

    def Update_Grab(self):
        if self.isGrabbing and self.targetGrabbed is not None:
            self.targetGrabbed.isGrabbed = True
            x = self.pos[0] + (self.hitBoxX[self.targetFrame[int(self.frame)]] * self.direction + (self.direction * -self.body[2])) 
            y = self.pos[1] + self.hitBoxY[self.targetFrame[int(self.frame)]] - 42
            if self.direction == -1:
                x += 20
            self.targetGrabbed.pos[0] = x
            self.targetGrabbed.pos[1] = y

    def Update_Hitbox(self):
        if self.direction == 1:
                self.hitBox[0] = self.bdy.x + self.hitBoxX[self.targetFrame[int(self.frame)]] 
                self.hitBox[1] = self.bdy.y + self.hitBoxY[self.targetFrame[int(self.frame)]]
                
        if self.direction == -1:
                self.hitBox[0] = self.bdy.x - self.hitBoxX[self.targetFrame[int(self.frame)]] + self.hitBoxOffsetX
                self.hitBox[1] = self.bdy.y + self.hitBoxY[self.targetFrame[int(self.frame)]] - self.hitBoxOffsetY

            
    def Update_Graphics(self):
        self.Update_Alignment()
        
        if self.burnSheet:
            self.frameSpeed = .2
            self.targetFrame = self.burnFrames
            self.action = -5
            
        #Draw
        if self.frame > len(self.targetFrame) - 1:
            self.frame = len(self.targetFrame) - 1
            if self.burnSheet:
                self.frame = 0
            
        self.bdy = pyglet.sprite.Sprite(self.cell[self.targetFrame[int(self.frame)]], self.x, self.y)
        if self.inAfterImage:
            self.imageTime -= .1

        if self.imageTime <= 0:
            self.imageTime = self.maxImageTime
            spr = self.bdy
            self.afterImage.append(AfterImage(pos=(self.x, self.y), image=spr, direction=self.direction))
            
        if self.EX > 0:
            self.bdy.color = (255,255,255)
        if self.EX < 0:
            self.bdy.color = (255,255,0)
            
        self.hit_sprite.x = self.hitBox[0]
        self.hit_sprite.y = self.hitBox[1]
        self.bdy.scale_x = self.direction
        
        self.Update_Hitbox()

        #Check For Ex
        self.EX = 1
        if self.EX <= -.5:
            self.EX = .5

        #Body
        #States
        blockStates = [13, 13.5, 14, 14.5]
        #Increase the hitBox size for blocking frames
        if self.action in blockStates:
            self.hitBox[2] = 100
        else:
            self.hitBox[2] = 50
            
        self.body = [self.pos[0] + 40, self.pos[1], 50,85]
        if self.invincible:
            self.body = [self.pos[0] + 40, self.pos[1], 0,0]
        
        if self.state == "Crouch":
            self.body[3] = 40
        if self.action == 7.9:
            self.body[3] = 0
            self.body[2] = 0
        self.body_sprite.x = self.body[0]
        self.body_sprite.y = self.body[1]
        self.body_sprite.scale_x = self.body[2]/50
        self.body_sprite.scale_y = self.body[3]/85
        #Hit Sprite
        self.hit_sprite.scale_x = self.body[2]/50
        self.hit_sprite.scale_y = self.body[3]/100

        #Getting Hit Effect
        self.blinkDuration -= .1
        self.blinking = self.blinkDuration >= 0
        if self.blinking:
            self.blinkTime -= .1
            self.canDraw = self.blinkTime <= .5
            if self.blinkTime <= 0:
                self.blinkTime = 1
        else:
            self.canDraw = True

        
    def AddDamage(self, amount=0, fixed=False):
        if self.addTime < 0:
            self.addTime = 2
            self.bonusDamage += amount
            if fixed == True:
                self.bonusDamage = amount

            
    def UpdatePhysics(self):  
        #Left and Right Directional Presses
        if self.moveRight:
            self.right = True
        if self.moveLeft:
            self.left = True          
        if self.rageBar > self.maxRageBar:
            self.rageBar = self.maxRageBar


        #Undefined
        self.burnTime -= .1
        self.rageBar += .1
        self.burning = self.burnTime > 0                    
        self.bonusDamage -= .08
        self.addTime -= .1

        #Stamina
        if self.stamina < 100:
            self.staminaSpeed += .01
            self.stamina += self.staminaSpeed
        #Limit
        if self.stamina > 100:
            self.stamina = 100
        if self.stamina < 0 :
            self.stamina = 0

        if self.alive and self.health < self.maxHealth:
            self.health += .02
        if self.health > self.maxHealth:
            self.health = self.maxHealth

        #Damage over time
        if self.burning:
            self.health -= .1
            if self.health < 1:
                self.burning = False

        #Attack Rest
        if self.vrest > 0:
            self.vrest -= .2
            if self.vrest <= 0:
                self.vrest = 0
                self.damageDealt = 0
                self.hitCombo = 0
                self.breaker_input = ""

        #Hit Combo
        if self.hitCombo < 2:
            self.bloodLine -= (self.bloodLine - self.health) / 10
            if self.bloodLine < 0:
                self.bloodLine = 0
                
        #Healing
        if self.healLength > 0 and self.alive:
            self.health += self.healLength / 20
            self.healLength -= 1 

        self.pos[0] -= self.velocity
            
        #Jumping
        if self.jump:
            self.pos[0] -= self.vel[0] * self.direction
        else:
            if self.opponent.body[0] > self.body[0] + 10:
                self.fallDirection = -1
            if self.opponent.body[0] + self.opponent.body[2] < self.body[0] - 10:
                self.fallDirection = 1
            self.pos[0] -= self.vel[0] * self.fallDirection * -1
        if self.freezeInAir == False:
            #Generally falling
            self.pos[1] += self.vel[1]
            if self.vel[0] > 0:
                self.vel[0] -= .3
                if self.vel[0] < 0:
                    self.vel[0] = 0
            if self.jump:
                self.canJumpAttack = self.action == -1
                if self.canJumpAttack:
                    #Jump Attack
                    if self.hitPunch == "MP" or self.hitPunch == "WP":
                        self.action = -1.2
                        self.frame = 0
                        self.state = "Skill"
                    #Jump Attack
                    if self.hitKick == "MK" or self.hitKick == "WK":
                        self.action = -1.5
                        self.state = "Skill"
                        self.frame = 0
                        
                self.vel[1] -= self.gravity
                self.gravity += .01
                self.state = "Airborne"
                if self.action == -1:
                    if self.frame > len(self.frames10) - 1: 
                        self.frame = len(self.frames10) - 1
                if self.pos[1] < self.ground:
                    self.jump = False
                    self.Play("Audio/land.wav")
                    self.frame = 0
                    self.pos[1] = self.ground
                    self.velocity = 0
                    self.vel[1] = 0
                    self.vel[0] = 0
                    self.jumpHeight = 15
                    
                    #Actions Unique to champions
                    #Chun'Li
                    if self.name == "Chun'Li":
                        self.action = -100
                        print("YES")
                    #Cammy and Fei'Long
                    if self.action == 12.5:
                        if self.name == "Cammy" or self.name == "Fei'Long":
                            self.action = 12.8
                        if self.name == "M.Bison":
                            self.action = 5
                            self.gravity = self.maxGravity
                            
                    else:
                        self.action = 5
                        self.gravity = self.maxGravity
                        if self.mixup != "fdA":
                            self.state = "Grounded"
                            self.key_combo = self.mixup
                            self.Check_Combo()

                    #Reset the KeyCombo espically if there has been a mixup
                    self.skill_combo_time = 0
                    self.key_combo = ""
                    if self.action == 9:
                        self.action = 9.5

        #If Falling
        if self.fall:
            #Stop Jumping 
            self.velocity = 0
            self.freezeInAir = False
            self.jump = False
            self.gravity += .01
            self.vel[1] -= self.gravity
            self.state = "Airborne"
            self.targetFrame = self.frames16
            self.action = -1
            self.gravity = self.maxGravity
            if self.frame > len(self.frames16) - 1: 
                self.frame = len(self.frames16) - 1
            if self.pos[1] < self.ground:
                if self.bounce > 0:
                    self.targetFrame = self.frames17
                    self.Play("Audio/fall.wav")
                    self.bounce = 0
                    self.fallHeight = 5
                    self.burnSheet = False
                    self.frame = 0
                    self.vel[1] = self.fallHeight
                else:
                    self.Play("Audio/fall.wav")
                    self.fall = False
                    self.pos[1] = self.ground
                    self.frame = 0
                    self.bounce = 1
                    self.invincible = False
                    self.gravity = self.maxGravity    
                    if self.alive:
                        self.isControlled = True
                    self.action = 7.9

        #Dummy
        if self.action == -100:
            self.action = 0
            self.vel[0] = 0
            self.state = "Grounded"
            self.isGrabbing = False
            self.isControlled = True
            self.invincible = False
            self.inAfterImage = False
            self.voiceFrame = 0
            self.opponent.maxHitCD = 1
            self.opponent.frameSpeed = self.defualtSpeed
                    
    def Update(self):
        if self.pause == False:
            self.frame += .2
            self.hitCD -= .1
            self.key_combo_time += .1
            if self.key_combo_time > 5:
                self.key_combo = ""
                
            self.UpdateActions()

            self.Check_Combo()

            #Updating Combos
            if self.voiceCD > 0:
                self.voiceCD -= .1

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
                if self.frame >= len(self.frames17) - 1:
                    self.frame = 0
                    if self.health > 0:
                        self.action = 5
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
                if self.blockWait >= 10:
                    self.action = 13
                    self.blockWait = 0
                    self.blockRight = False
                    self.blockLeft = False
                    if self.moveRight:
                        self.right = True
                    if self.moveLeft:
                        self.left = True
                    
            #Crouch Block (Normal)
            if self.action == 14:
                self.targetFrame = self.frames29
                self.frame = 3
                self.blockWait += 1
                if self.blockWait >= 10:
                    self.action = 4
                    self.blockWait = 0
                    if self.blockRight:
                        self.blockRight = False
                    if self.blockLeft:
                        self.blockLeft = False
                    
            #Crouch Block (Hit)
            if self.action == 14.5:
                self.targetFrame = self.frames29
                self.frame = 4
                self.blockWait += 1
                if self.blockWait >= 20:
                    self.action = 14
                    self.blockWait = 0
                    if self.blockRight:
                        self.blockRight = False
                        self.right = True
                    if self.blockLeft:
                        self.blockLeft = False
                        self.left = True



























        



