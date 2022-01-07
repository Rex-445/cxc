#! python3
#Dragon Fighters Main Script

import pyglet, random, math, pickle, pygame
from pyglet import *
from pyglet.input import base as pgt
from pyglet.window import key, FPSDisplay, mouse
from pyglet.gl import *
from menu_manager import *
from story_manager import *
##from sounds import *
from button import Button
from prop import *
from char_AI import *
from data_manager import *
from network import Network

#Characters
from Characters import *


pygame.init()
fullScreen = False
big_screen = [150, 150]
if fullScreen:
    big_screen = [520, 300]
    
class Camera():
    def __init__(self, pos=(0,0), target=None):
        self.pos = list(pos)
        self.target = target
        self.use_occlusion_culling = True

        self.offset = [500,500]
        self.stageWidth = 0

        #Camera Shake
        self.shakeTime = 0
        self.isShaking = False

        self.anchor = [0,350]

        #Encapsulate
        self.center = [0,0]       


    def set_offset(self, x,y):
        self.offset = [x,y]
        
    def AnchorTarget(self, target):
        #Restrict on the X
        self.pos[0] -= ((self.pos[0]) - (target - 430)) / 20
        if self.pos[0] > self.stageWidth - 1000:
            self.pos[0] = self.stageWidth - 1000
        if self.pos[0] < 0:
            self.pos[0] = 0

    def Encapsulate(self, p1, p2):
        self.center = [0,0]
        if p1.pos[0] > p2.pos[0]:
            dist = p1.pos[0] - p2.pos[0]
            dist = dist/2
            self.center[0] = p2.pos[0] + dist
        if p2.pos[0] > p1.pos[0]:
            dist = p2.pos[0] - p1.pos[0]
            dist = dist/2
            self.center[0] = p1.pos[0] + dist

        if self.center[0] > 5:
            self.AnchorTarget(self.center[0])
        

    def update(self, objs, user):
        for obj in objs:
            obj.update()
            obj.sprite.x -= self.pos[0] * obj.cameraType
            obj.sprite.y -= self.pos[1]
            obj.sprite.draw()
            
    def Raw_Draw(self, objs):
        for obj in objs:
            obj.bdy.draw()
            
    def Update_UI(self, objs):
        for menu in  objs:
            menu.sprite.draw()
            if menu.type == "InputField":
                menu.text.draw()
            
    def update_back_ground_objects(self, objs):
        if self.isShaking:
            self.pos[0] += math.sin(self.pos[0]) * .2
            self.pos[1] += math.cos(self.pos[1]) * .2
            self.shakeTime -= .1
            if self.shakeTime <= 0:
                self.shakeTime = 0
                self.isShaking = False
            
        for obj in objs:                
            obj.update()
            obj.sprite.y +=  big_screen[1]
            if obj.cameraType == 1:
                obj.sprite.x -= self.pos[0]
                obj.sprite.y -= self.pos[1] 
            if obj.cameraType == 2:
                obj.sprite.x -= self.pos[0] * obj.zpos
                obj.sprite.y -= self.pos[1]                
            obj.sprite.draw()

            
        if not self.isShaking:
            self.pos[1] = 0

        self.isShaking = self.shakeTime > 0
            
    def update_fore_ground_objects(self, objs):
        for obj in objs:
            obj.update()
            obj.sprite.y +=  big_screen[1]
            if obj.cameraType == 1:
                obj.sprite.x -= self.pos[0]
                obj.sprite.y -= self.pos[1]
            if obj.cameraType == 2:
                obj.sprite.x -= self.pos[0] * obj.zpos
                obj.sprite.y -= self.pos[1]
            obj.sprite.draw()

    def update_vfx(self, vfx_list):
        for vfx in vfx_list:
            if vfx.alive == False:
                vfx_list.remove(vfx)
                return
            vfx.update(big_screen)
            if vfx.alive:
                vfx.sprite.x -= self.pos[0]
                vfx.sprite.y -= self.pos[1]
                vfx.sprite.draw()

    def Distance(self, champion, opponent):
        dist = (((champion.pos[0] + champion.body[0]) - (opponent.pos[0] + opponent.body[0]) - 20) + (champion.pos[1] + champion.body[3]) - (opponent.pos[1] + opponent.body[3]))
        if dist < 0:
            dist = dist * -1
        return dist


    def UpdateAfterImage(self, imgs, owner):
        for img in imgs:
            if img.alive:
                img.update()
                img.sprite.x -= self.pos[0]
                img.sprite.y -= self.pos[1]
                img.sprite.draw()
            else:
                del img

    def Draw_Story_Characters(self, objs):       
            
        #Shadows
        for shad in objs:
            if shad.pause == False:
                #Shadow
                shad.shadow.x = shad.pos[0] - self.pos[0] + shad.shadowOffset[0]
                shad.shadow.y = shad.ground - 3
                shad.shadow.y += big_screen[1]
            shad.shadow.draw()
            
            
        #Champions
        for obj in objs:
            obj.Update()
            obj.bdy.y += big_screen[1]
            obj.bdy.x -= self.pos[0]
            obj.bdy.y -= self.pos[1]
            obj.bdy.draw()


        
    def update_player_objects(self, objs):
            
        #Shadows
        for shad in objs:
            if shad.pause == False:
                #Shadow
                shad.shadow.x = shad.pos[0] - self.pos[0] + shad.shadowOffset[0]
                shad.shadow.y = shad.ground - 3
                shad.shadow.y += big_screen[1]
                #UI Icon
                shad.icon.x = shad.pos[0] + 40 - self.pos[0]
                shad.icon.y = shad.pos[1] + 80
                shad.icon.y += big_screen[1]
            shad.shadow.draw()
            shad.icon.draw()
            
            
        #Champions
        for obj in objs:
            for face in obj.faces:
                if face.alive == False:
                    obj.faces.remove(face)
                    return
                face.update()
                
            self.UpdateAfterImage(obj.afterImage, owner=obj)
            #Shake the camera
            if obj.cameraShake > 0 and self.shakeTime == 0:
                self.shakeTime = obj.cameraShake
            conditions = [not obj.opponent.isGrabbed, not obj.action == 7.9, obj.state != "Airborne", obj.opponent.state != "Airborne"]
            goOn = False
            for c in conditions:
                goOn = c
                if goOn == False:
                    break
            if goOn:
                #Collision of both players
                if self.Distance(obj, obj.opponent) < 40:
                    if obj.opponent.toGrab == False:
                        if obj.body[0] + obj.body[2] + 5 >= obj.opponent.body[0] and obj.body[0] < obj.opponent.body[0]:
                            obj.pos[0] -= 2
                        if obj.body[0] - 5 <= obj.opponent.body[0] + obj.opponent.body[2] and obj.body[0] + obj.body[2] >= obj.opponent.body[0] + obj.opponent.body[2]:
                            obj.pos[0] += 2
                
            if obj.isGrabbed:
                obj.isControlled = False
            
            #Re-position player 1 at Right boundary
            maxBoundry = 100
            
            #Boundries
            if obj.pos[0] + 30 < 0:
                obj.pos[0] = -30
                obj.KeyUp("Left")
            if obj.pos[0] > self.stageWidth  - maxBoundry:
                obj.pos[0] = self.stageWidth - maxBoundry
                obj.KeyUp("Right")

            maxCenter = 400
            #Left Side
            if obj.pos[0] < self.center[0] - maxCenter:
                if abs(obj.velocity) > 0 or abs(obj.vel[0]) > 0:
                    obj.pos[0] = self.center[0] - maxCenter
                if obj.left:
                    obj.KeyUp("Left")
                    
            #Right Side
            if obj.pos[0] > self.center[0] + maxCenter:
                if abs(obj.velocity) > 0 or abs(obj.vel[0]) > 0:
                    obj.pos[0] = self.center[0] + maxCenter
                if obj.right:
                    obj.KeyUp("Right")
                
            if obj.pause == False:
                obj.Update()
                obj.bdy.y += big_screen[1]
                obj.bdy.x -= self.pos[0]
                obj.bdy.y -= self.pos[1]
            if obj.canDraw:
                obj.bdy.draw()

        #Projectiles
        for obj in objs:
            #Special Effects
            for b in obj.balls:
                #Boundries
                if b.pos[0] + b.sprite.width < 0:
                    b.alive = False
                if b.pos[0] + b.sprite.width > self.stageWidth + b.sprite.width:
                    b.alive = False

                #Updates
                if b.alive:
                    if objs[0].superSkill == False and objs[1].superSkill == False:
                        b.update()
                        b.sprite.y += big_screen[1]
                        b.sprite.x -= self.pos[0]
                        b.sprite.y -= self.pos[1]
                        b.hit_sprite.x -= self.pos[0]
                        b.hit_sprite.y -= self.pos[1]
##                        b.hit_sprite.draw()
                    b.sprite.draw()
                else:
                    if b.direction == -1:
                        vfx_list.append(Broken(pos=(b.pos[0] - 70, b.sprite.y + 5), speed=.3, direction=b.direction, img=b.broken_sheet, row=4, col=1))
                    else:
                        vfx_list.append(Broken(pos=(b.pos[0] + 20, b.sprite.y + 5), speed=.3, direction=b.direction, img=b.broken_sheet, row=4, col=1))
                    obj.balls.remove(b)
            
        #Body and Hitbox Visuals
        for obj in objs:
            obj.hit_sprite.x -= self.pos[0]
            obj.hit_sprite.y -= self.pos[1] - big_screen[1]
            obj.body_sprite.x -= self.pos[0]
            obj.body_sprite.y -= self.pos[1] - big_screen[1]
            obj.hit_sprite.draw()
            obj.body_sprite.draw()
            self.update_vfx(obj.vfx)
            

class OnlineChampion():
    def __init__(self, pos=(0,0)):
        self.pos = list(pos)
        self.sprite = None
        self.frame = 0
        self.targetFrame = None
        self.health = 100
        self.rageBar = 100
        self.stamina = 100
   
#Camera
cam = Camera(pos=(0,0))
n = Network()
p = n.getP()
p2 = n.send(p)

class Background():
    def __init__(self, pos=(0,0), size=1, img="bg/sp/ship.png", zpos=1, cameraType=1):
        self.pos = list(pos)
        self.size = size
        self.zpos = zpos
        self.cameraType = cameraType
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load(img), x=self.pos[0], y=self.pos[1])
        self.shadow = pyglet.sprite.Sprite(pyglet.image.load("bg/sp/s.png"))
    def update(self):
        self.sprite.x = self.pos[0]
        self.sprite.y = self.pos[1]
        self.sprite.scale_x = self.size
        self.sprite.scale_y = self.size

class SplashImage():
    def __init__(self, pos=(0,0), img="", length=0):
        self.pos = list(pos)
        self.frame = 0
        self.loop = length > 1
        self.cells = []

        if length > 0:
            self.__init__self__(length, img)
            
        else:
            self.sprite = pyglet.sprite.Sprite(pyglet.image.load(img), x=self.pos[0], y=self.pos[1])

    def __init__self__(self, length, img):
        for i in range(length):
            self.cells.append(pyglet.sprite.Sprite(pyglet.image.load(img + str(i)+".png")))
        
    def update(self):
        self.frame += .3

        #If an Animatable Splash Image
        if len(self.cells) > 0:
            if self.frame < len(self.cells):
                self.sprite = self.cells[int(self.frame)]
                self.sprite.x = self.pos[0]
                self.sprite.y = self.pos[1]
                self.sprite.draw()

        #If not Animatable
        else:
            if self.frame < 20:
                self.sprite.draw()
                self.sprite.x = self.pos[0]
                self.sprite.y = self.pos[1]
            
        
        
class GameWindow(pyglet.window.Window):
    #Initilize the Game Window
    def __init__(self, *args, **kwargs):
        global icon
        
        super().__init__(*args, **kwargs)
##        glClearColor(0, 0, 0, 1)
        self.set_location(400,100)
        self.frame_rate = 1/70
        self.set_icon(pyglet.image.load("sprites/icon.png"), pyglet.image.load("UI/ryu_small.png"))
        self.fps_display = FPSDisplay(self)
        self.fps_display.label.font_size = 10

        self.main_batch = pyglet.graphics.Batch()
        self.menu_batch = pyglet.graphics.Batch()
        self.story_batch = pyglet.graphics.Batch()

        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        self.joystickKeys = pickle.load(open("data/JoystickKeys.txt", "rb"))
        self.isSettingKeys = False

        #StoryMode
        self.storyMode = False
        self.storyCharacters = []
        self.loadingBar = pyglet.sprite.Sprite(pyglet.image.load("sprites/healthBar.png"), x=200, y=50)
        self.chatText = pyglet.text.Label("Name: ", x=150, y=360 + big_screen[1], multiline=True, width=400)
        self.chatBox = pyglet.sprite.Sprite(pyglet.image.load("UI/ChatBox.png"), x=10, y=420)
        self.chatImage = pyglet.sprite.Sprite(pyglet.image.load("UI/Story_Headshots/Ryu_head.png"), x=15, y=424)

        #Menu_UI
        self.targetInput = None
        self.caps = False
        self.canClick = True

        #Joystick
        self.joyStickLeft = False
        self.joyStickRight = False
        self.joyStickDown = False
        self.joyStickUp = False

        #Stall for a defualtt game
        self.maxStallTime = 10
        self.stallTime = self.maxStallTime
        self.face = pyglet.sprite.Sprite(pyglet.image.load("UI/Ryu_Head.png"), x=0, y=0, batch=self.menu_batch)
        self.face.scale_x = 4
        self.face.scale_y = 4
        self.face.opacity = 100
        self.face.color = (255,0,0)

        #Knock Out Slpash Image
        self.ko = SplashImage(pos=(270,200), img="UI/Splash/", length=42)
        self.ko.frame = 100

        #Sound
        self.player = pyglet.media.Player()
        self.music = False
        self.musicVolume = .1
        self.main = pyglet.media.load("BGM/BGM.mp3")

        self.player.queue(self.main)
        self.player.volume = self.musicVolume
        self.player.loop = True
        self.player.play()
##        self.player.seek(-1)

        #Start Game
        self.startGame = False
        
        #End Game
        self.deathTimer = 50
        self.endTimer = 100
        self.timer = 0
        self.winner = "None"
        self.wins = [0,0]
        self.bgTransition = pyglet.sprite.Sprite(pyglet.image.load("sprites/black.png"))
        self.targetOpacity = 0
        self.transitionSpeed = 20


        #Hit Combo Visuals
        #Damage Dealt
        #Player 1
        self.dmgDealt1 = pyglet.text.Label("Damage: ", x=80, y=220 + big_screen[1], multiline=True, width=100)
        self.dmgDealt1.bold = True
        self.dmgDealt1.color = (255,255,0,255)
        #Player 2
        self.dmgDealt2 = pyglet.text.Label("Damage: ", x=self.width - 80, y=220 + big_screen[1], multiline=True, width=100)
        self.dmgDealt2.bold = True
        self.dmgDealt2.color = (255,255,0,255)
        
        self.hit1 = pyglet.text.Label("Hits: ", x=80, y=250 + big_screen[1], multiline=True, width=100)
        self.hit1.bold = True
        self.hit1.color = (255,255,0,255)
        self.hit2 = pyglet.text.Label("Hits: ", x=self.width - 80, y=250 + big_screen[1], multiline=True, width=100)
        self.hit2.bold = True
        self.hit2.color = (255,255,0,255)

        #Create
        menuManager.charSelect = [Char_Ken(pos=[0,0]), Char_Ryu(pos=[0,0]), Char_ChunLi(pos=[0,0]), Char_Bison(pos=[0,0]), Char_Cammy(pos=[0,0]), Char_Akuma(pos=[0,0]), Char_FeiLong(pos=[0,0])]
        menuManager.update_all_menu_objects()
        menuManager.full_screen(big_screen)
        
        #Start Game
        self.startTime = 30
        self.startTimer = 0
        self.round = 1
        self.roundCall = pyglet.text.Label("Round " + str(self.round), x=320 + big_screen[0], y=280 + big_screen[1], multiline=True, width=100)
        self.roundCall.bold = True
        self.roundCall.color = (255,255,0,255)
        self.shake_time = 0
        self.mag = 0

        self.resetPos = [[200 + big_screen[0],100], [500+big_screen[0],100]]


        #Keys
        self.checking = False
        self.keys = pickle.load(open("data/Keys.txt", "rb"))
        self.newKeys = []
##        pickle.dump(self.keys, open("data/Keys.txt", "wb"))


        self.back_ground = []
        self.AIs = 1

        #Check for PlayerData
        self.MakePlayerData()
        if player_name == "Defualt":
            menuManager.stage = "PlayerDetails"
            menuManager.update_menu_objects()
        self.UpdateJoystickVisuals()


    def MakePlayerData(self):
        #Player Data
        #Player Name
        #Player Boarder
##        media = pyglet.media.load("Gameplay.mp4")
##        player = pyglet.media.Player()
##        player.queue(media)
##        player._create_texture()
##        player.play()
        
        self.playerBoarder = pyglet.sprite.Sprite(pyglet.image.load("UI/PlayerData/Boarder/" + boarder + ".png"), x=10, y=415 + big_screen[1])
        self.playerNameText = pyglet.text.Label(player_name, x=150, y=480 + big_screen[1], multiline=True, width=400, batch=self.menu_batch)
        #Player Icon
        self.playerIcon = pyglet.sprite.Sprite(pyglet.image.load("UI/PlayerData/Icons/"+icon+".png"), x=70, y=460 + big_screen[1], batch=self.menu_batch)
        self.playerIcon.scale_x = .5
        self.playerIcon.scale_y = .5

        #Joystick
        self.joystickText = pyglet.text.Label("Set The Joystick Key", x=420, y=420 + big_screen[1], multiline=True, width=400)
        self.joystickText.color = (255,0,0,255)
        self.joystickText.font_size = 20

    #Play Sounds
    def PlaySound(self, file):
        self.sound = pyglet.media.Player()
        media = pyglet.media.load(file)

        self.sound.queue(media)
        self.sound.volume = .5
        self.sound.play()

    #Play BG Music
    def PlayMusic(self, file):
        self.player.delete()
        media = pyglet.media.load(file)

        self.player.queue(media)
        self.player.next_source()
        self.player.volume = .1
        self.player.loop = True
        self.player.play()

        
    def Make_Players(self, player1, player2, AI):
        global vfx_list

        self.bgTransition.opacity = 255
        self.targetOpacity = 0
        self.startGame = False
        self.startTimer = 0
        
        cam.pos[0] = 0
        #Refresh
        self.winner = "None"
        vfx_list = []
        
        self.player1 = None
        self.player2 = None
        
        #Player1
        self.champs = Craft_Champions(player1, player2)

        #Update Variations
        randChoice = 0
        if self.round == 1:
            randChoice = random.randint(0, len(Craft_Champions(player1, player2)[1].variation_names)-1)
            self.AssignVariations(self.champs[0], menuManager.variationSelectID)
            self.AssignVariations(self.champs[1], randChoice)
        
        self.player1 = self.champs[0]
        self.player1.finishImage.scale_x = 1
        self.player1.pos = self.resetPos[0]

        #Player2
        self.player2 = self.champs[1]
        self.player2.icon = pyglet.sprite.Sprite(pyglet.image.load("UI/p2.png"))
        self.player2.finishImage.scale_x = -1
        self.player2.pos = self.resetPos[1]
        
        self.champions = []
        self.champions.append(self.player1)
        self.champions.append(self.player2)
        self.player2.opponent = self.player1
        self.player1.opponent = self.player2
        self.player1.talking = True
        
        #AI
        self.AIs = AI
        if AI > 0:
            self.AI = Human_AI(champion=self.player2, opponent=self.player1)
        if AI > 1:
            self.AI2 = Human_AI(champion=self.player1, opponent=self.player2)

        self.Make_Player_UI(randChoice)

    def AssignVariations(self, p, choice):
        p.targetVariation = p.variation_names[choice]
        #Ryu
        if p.name == "Ryu":
            if choice == 1:
                if p.name == self.champs[0].name:
                    self.champs = Craft_Champions("Anti-Ryu", self.champs[1].name)
                    menuManager.player = Char_AntiRyu()
                    return
                if p.name == self.champs[1].name:
                    self.champs = Craft_Champions(self.champs[0], "Anti-Ryu")
                    menuManager.enemy = Char_AntiRyu()
        menuManager.update_all_menu_objects()

    def Make_Player_UI(self, variation):
        self.normalHealthbar = pyglet.sprite.Sprite(pyglet.image.load("sprites/healthBar.png"))
        self.healHealhBar = pyglet.sprite.Sprite(pyglet.image.load_animation("sprites/healthBar_heal.gif"))
        self.glowHealthBar = pyglet.sprite.Sprite(pyglet.image.load_animation("sprites/healthBar_glow.gif"))
        #UI Player1
        self.playerStats1 = pyglet.sprite.Sprite(pyglet.image.load(self.player1.head), x=30, y=330 + big_screen[1])
        self.playerStats1.scale_x = 1.7
        self.playerStats1.scale_y = 1.7
        self.healthBar1 = pyglet.sprite.Sprite(pyglet.image.load("sprites/healthBar.png"), x=68.5, y=332 + big_screen[1])
        self.healthBar1.scale_x = 1.7
        self.healthBar1.scale_y = 1.7
        #Variation Icon
        self.icon1 = pyglet.sprite.Sprite(pyglet.image.load("sprites/healthBar.png"), x=250, y=355 + big_screen[1])
        self.icon1.image = self.player1.variation_images[menuManager.variationSelectID].image
        self.icon1.scale_x = .6
        self.icon1.scale_y = .6
        #BloodLine
        self.bloodLine1 = pyglet.sprite.Sprite(pyglet.image.load("sprites/bloodLine.png"), x=68, y=332 + big_screen[1])
        self.bloodLine1.scale_x = 1.7
        self.bloodLine1.scale_y = 1.7
        #Stamina
        self.staminaBar1 = pyglet.sprite.Sprite(pyglet.image.load("sprites/staminaBar.png"), x=73, y=300 + big_screen[1])
        self.staminaBoarder1 = pyglet.sprite.Sprite(pyglet.image.load("sprites/staminaBoarder.png"), x=73, y=300 + big_screen[1])
        #RageBar
        self.rageBarOutline1 = pyglet.sprite.Sprite(pyglet.image.load("sprites/rage_bar_outline.png"), x=70, y=313 + big_screen[1])
        self.rageBarOutline1.scale_x = 1.3
        self.rageBarOutline1.scale_y = 1.3
        #Rulers
        self.rageBarOutlineRulers1 = pyglet.sprite.Sprite(pyglet.image.load("sprites/rage_bar_outline_rulers.png"), x=70, y=312 + big_screen[1])
        self.rageBarOutlineRulers1.scale_x = 1.3
        self.rageBarOutlineRulers1.scale_y = 1.3
        #Fill
        self.rageBarFill1 = pyglet.sprite.Sprite(pyglet.image.load("sprites/rage_bar_fill.png"), batch=self.main_batch, x=70, y=314 + big_screen[1])
        self.rageBarFill1.scale_x = 1.1
        self.rageBarFill1.scale_y = 1.1
        #Glow
        self.glows = []
        for i in range(3):
            self.glows.append(pyglet.sprite.Sprite(pyglet.image.load_animation("sprites/glow_rage_bar.gif"), x=73 + (i * 52),  y=313 + big_screen[1]))
            self.glows[-1].scale_x = 1.3
            self.glows[-1].scale_y = 1.3
            self.glows[-1].visible = False

        

        #UI Player2
        self.playerStats2 = pyglet.sprite.Sprite(pyglet.image.load(self.player2.head), x=self.width - 30, y=330 + big_screen[1])
        self.healthBar2 = pyglet.sprite.Sprite(pyglet.image.load("sprites/healthBar.png"), x=self.width-280, y=331 + big_screen[1])
        self.healthBar2.scale_x = 1.7
        self.healthBar2.scale_y = 1.7
        self.playerStats2.scale_x = -1.7
        self.playerStats2.scale_y = 1.7
        #BloodLine
        self.bloodLine2 = pyglet.sprite.Sprite(pyglet.image.load("sprites/bloodLine.png"), x=self.width-280, y=332 + big_screen[1])
        self.bloodLine2.scale_x = 1.7
        self.bloodLine2.scale_y = 1.7
        #Variation Icon
        self.icon2 = pyglet.sprite.Sprite(pyglet.image.load("sprites/healthBar.png"), x=self.width-280, y=355 + big_screen[1])
        self.icon2.image = self.player2.variation_images[variation].image
        self.icon2.scale_x = .6
        self.icon2.scale_y = .6
        #Stamina
        self.staminaBar2 = pyglet.sprite.Sprite(pyglet.image.load("sprites/staminaBar.png"), x=self.width - 280, y=300 + big_screen[1])
        self.staminaBoarder2 = pyglet.sprite.Sprite(pyglet.image.load("sprites/staminaBoarder.png"), x=self.width - 280, y=300 + big_screen[1])
        #RageBar
        self.rageBarOutline2 = pyglet.sprite.Sprite(pyglet.image.load("sprites/rage_bar_outline.png"), x=self.width - 235, y=313 + big_screen[1])
        self.rageBarOutline2.scale_x = 1.3
        self.rageBarOutline2.scale_y = 1.3
        #Fill
        self.rageBarFill2 = pyglet.sprite.Sprite(pyglet.image.load("sprites/rage_bar_fill.png"), batch=self.main_batch, x=self.width - 72, y=314 + big_screen[1])
        self.rageBarFill2.scale_x = 1.1
        self.rageBarFill2.scale_y = 1.1
        #Rulers
        self.rageBarOutlineRulers2 = pyglet.sprite.Sprite(pyglet.image.load("sprites/rage_bar_outline_rulers.png"), x=self.width - 235, y=312 + big_screen[1])
        self.rageBarOutlineRulers2.scale_x = 1.3
        self.rageBarOutlineRulers2.scale_y = 1.3
        #Glow]
        for i in range(3):
            self.glows.append(pyglet.sprite.Sprite(pyglet.image.load_animation("sprites/glow_rage_bar.gif"), x=self.width - 232 + (i * 52),  y=313 + big_screen[1]))
            self.glows[-1].scale_x = 1.3
            self.glows[-1].scale_y = 1.3
            self.glows[-1].visible = False

        #Advanced Visuals
        self.glow2 = pyglet.sprite.Sprite(pyglet.image.load_animation("sprites/healthBar_glow.gif"), x=self.width-280, y=332 + big_screen[1])

    def UpdateHealthBars(self):
        #Player1
        self.bloodLine1.scale_x = self.player1.bloodLine / self.player1.maxHealth * 1.7
        self.rageBarFill1.scale_x = self.player1.rageBar / self.player1.maxRageBar * 1.3
        self.healthBar1.scale_x = self.player1.health / self.player1.maxHealth * 1.7
        self.staminaBar1.scale_x = self.player1.stamina * .015
        self.staminaBoarder1.scale_x = 1.5
        
        if self.player1.health <= 0:
            self.healthBar1.scale_x = 0          
            
            
        #Player 2
        self.bloodLine2.scale_x = self.player2.bloodLine / self.player2.maxHealth * 1.7
        self.rageBarFill2.scale_x = -self.player2.rageBar / self.player2.maxRageBar * 1.3
        self.healthBar2.scale_x = self.player2.health / self.player2.maxHealth * 1.7
        self.staminaBar2.scale_x = self.player2.stamina * .015
        self.staminaBoarder2.scale_x = self.player2.stamina * .015
        self.staminaBoarder2.scale_x = 1.5
        if self.player2.health <= 0:
            self.healthBar2.scale_x = 0
            
        #Player Stats
        self.playerStats2.draw()
        self.playerStats1.draw()
        #Player Ragebar
        self.rageBarOutline1.draw()
        self.rageBarOutline2.draw()
        #Player Stamina Bar
        self.staminaBar1.draw()
        self.staminaBoarder1.draw()
        self.staminaBar2.draw()
        self.staminaBoarder2.draw()
        #RageBar Detail
        self.rageBarOutlineRulers1.draw()
        self.rageBarOutlineRulers2.draw()
        #Player Bloodline
        self.bloodLine1.draw()
        self.bloodLine2.draw()
        #Player HealthBar
        self.healthBar1.draw()
        self.healthBar2.draw()
        #Player Variation Icon
        self.icon2.draw()
        self.icon1.draw()

    def Load_Audio_Length(self, audio):
        playerIntro = pyglet.media.Player()
        playerIntro.queue(pyglet.media.load(audio))
        return playerIntro.get_duration()
    
    def Player_Talks(self):
        if self.player1.talking:
            self.player1.pos = [200 + big_screen[0],100]
            self.player2.pos = [500 + big_screen[0],100]
            #Player 1 Talks
            if self.player1.talkTime == 50:
                self.player1.action = -5
                self.player1.talkTime += 1
                choiceList = []
                choices = []
                rand = 0
                for ch in self.player1.talkTo:
                    if ch[0] == self.player2.name:
                        choiceList.append(ch[2]) 
                        choices.append(ch[1])
                if len(choiceList) == 0:
                    self.startGame = True
                    self.player1.talking = False
                    return
                
                rand = random.randint(0, len(choiceList)-1)
                self.player1.PlayVoice(choiceList[rand])
                self.player1.talkChoice = choices[rand]
                
            #Player 2 Responds
            if self.player1.talkTime == self.player1.maxTalkTime:
                choiceList = []
                choices = []
                rand = 0
                for choice in range(len(self.player2.respondTo)):
                    if self.player2.respondTo[choice][0] == self.player1.name and self.player1.talkChoice == self.player2.respondTo[choice][1]:
                        choiceList.append(self.player2.respondTo[choice][2])
                        choices.append(self.player2.respondTo[choice][1])
                if len(choiceList) == 0:
                    self.player1.talking = False
                    self.startGame = True
                    return
                rand = random.randint(0, len(choiceList)-1)
                self.player2.Play(choiceList[rand])
                self.player2.action = -6
                self.player2.frame = 0
                
                #Start Game
                self.player1.talking = False
                self.startGame = True
            if self.player1.voice.playing == False:
                self.player1.talkTime += 1

    def MakeCombos(self, p1, p2):
        if p2.comboEnd == True:
            p2.comboEnd = False
            highest = p2.hitCombo
            voice = []
            targetVoiceCD = 70
            #Get the highest one
            if p2.name in p1.championTaunt:
                if highest >= 5:
                    nameTaunt = p1.championTaunt
                    voice = p1.championTaunt[p2.name]
                    choice = random.randint(0, len(voice)-1)
                    voice  = p1.dir + "/Wins/" + p2.name + "/" + voice[choice]
                    targetVoiceCD = 40
            else:
                if highest >= 5:
                    for combo in p1.combos:
                        voice = p1.dir + "/Wins/Combos/" + random.choice(combo)
                    
            #Taunt Opponent
            if p1.voiceCD <= 0 and len(voice) > 0:
                p1.voiceCD = targetVoiceCD
                p1.PlayVoice(voice)
            p2.hitCombo = 0
                
    def Update_Hit_Combos(self):
        #Player1
        if self.player2.hitCombo > 1:
            self.hit1.text = "Hits: " + str(self.player2.hitCombo)
            self.dmgDealt1.text = str(int(self.player2.damageDealt / self.player2.maxHealth * 100)) + "%"
            self.dmgDealt1.draw()
            self.hit1.draw()

        #Player2
        if self.player1.hitCombo > 1:
            self.hit2.text = "Hits: " + str(self.player1.hitCombo)
            self.dmgDealt2.text = str(int(self.player1.damageDealt / self.player1.maxHealth * 100)) + "%"
            self.dmgDealt2.draw()
            self.hit2.draw()

    def UpdatePlayerDirections(self, player):
        if player.isGrabbing or player.opponent.isGrabbing:
            return
        #Player1 Direction
        if player.body[0] < player.opponent.body[0]:
            if player.state == "Grounded" or player.state == "Crouch":
                player.direction = 1
        if player.body[0] > player.opponent.body[0]:
            if player.state == "Grounded" or player.state == "Crouch":
                player.direction = -1


    def Transition(self):
        self.bgTransition.opacity -= (self.bgTransition.opacity - self.targetOpacity) / self.transitionSpeed
            
    def UpdateGlows(self):
        for glow in self.glows:
            glow.draw()
        #Player1 Glows
        #First
        if self.player1.rageBar >= 200:
            if self.glows[0].visible == False:
                self.PlaySound("Audio/Sys/Game/Bar2.wav")
            self.glows[0].visible = True
        else:
            self.glows[0].visible = False
            
        #Second
        if self.player1.rageBar >= 400:
            if self.glows[1].visible == False:
                self.PlaySound("Audio/Sys/Game/Bar2.wav")
            self.glows[1].visible = True
        else:
            self.glows[1].visible = False
            
        #Third
        if self.player1.rageBar >= 600:
            if self.glows[2].visible == False:
                self.PlaySound("Audio/Sys/Game/Bar.wav")
            self.glows[2].visible = True
        else:
            self.glows[2].visible = False
            
        #Player2 Glows
        #First
        if self.player2.rageBar >= 200:
            if self.glows[5].visible == False:
                self.PlaySound("Audio/Sys/Game/Bar2.wav")
            self.glows[5].visible = True
        else:
            self.glows[5].visible = False
            
        #Second
        if self.player2.rageBar >= 400:
            if self.glows[4].visible == False:
                self.PlaySound("Audio/Sys/Game/Bar2.wav")
            self.glows[4].visible = True
        else:
            self.glows[4].visible = False
            
        #Third
        if self.player2.rageBar >= 600:
            if self.glows[3].visible == False:
                self.PlaySound("Audio/Sys/Game/Bar.wav")
            self.glows[3].visible = True
        else:
            self.glows[3].visible = False
            
    #Reset Game
    def Check_Win(self):
        #Check if either players looses        
        if self.player1.alive == False or self.player2.alive == False:
            self.player1.isControlled = False
            self.player2.isControlled = False
            if self.winner == "None":
                choices = ["Ken", "M.Bison", "Ryu", "Cammy", "Fei'Long", "Chun'Li"]
                choice = random.choice(choices)
                choice2 = random.choice(choices)
            
        #Player 2 Looses
        if self.player2.alive == False and self.player1.alive == True:
            self.timer += .2
            self.winner = self.player1.name
            self.player2.finishImage = self.player2.loseImage
            if self.timer > self.deathTimer:
                self.roundCall.text = self.player1.name + " WINS!!"
                #Check For Perfect
                if self.timer > self.deathTimer + 20:
                    if self.player1.health == self.player1.maxHealth:
                        self.roundCall.text = self.player1.name + " WINS!!\nPERFECT"
                if self.player1.win == False:
                    if self.player1.state == "Grounded":
                        self.roundCall.draw()
                        self.wins[0] += 1
                        self.player1.win = True
                        self.player1.winCount = self.wins[0]
                        self.player1.frame = 0
                        self.player1.Win()
                    else:
                        self.timer = self.deathTimer - 5
                        return
                self.roundCall.draw()
            if self.timer > self.endTimer:
                #Champion To Select
                choice = self.player2.name
                name = self.player1.name
                #Remake the game if in Game mode
                if storyManager.mode == "Game":
                    if self.wins[0] > 1:
                        self.round = 0
                        self.wins = [0,0]
                        self.player1.finishImage = self.player1.winImage
                        self.player2.finishImage = self.player2.loseImage
                        self.MenuGraphics()
                        return
                    del self.player1
                    del self.player2
                    self.Make_Players(name, choice, AI=self.AIs)

                #Return to story if in Story mode
                if storyManager.mode == "Story":
                    if self.wins[0] > 1:
                        self.round = 0
                        self.wins = [0,0]
                        menuManager.mode = "Story"
                    if menuManager.mode == "Game":
                        self.Make_Players(self.player1.name, choice, AI=self.AIs)
                self.timer = 0
                self.round += 1

        #Player 1 Looses
        if self.player1.alive == False and self.player2.alive == True:
            self.timer += .2
            self.winner = self.player2.name
            if self.timer > self.deathTimer:
                self.roundCall.text = self.player2.name + " WINS!!"
                #Check For Perfect
                if self.timer > self.deathTimer + 20:
                    if self.player2.health == self.player2.maxHealth:
                        self.roundCall.text = self.player2.name + " WINS!!\n  PERFECT"
                if self.player2.win == False:
                    if self.player2.state == "Grounded":
                        self.wins[1] += 1
                        self.player2.win = True
                        self.player2.winCount = self.wins[1]
                        self.player2.frame = 0
                        self.player2.Win()
                    else:
                        self.timer = self.deathTimer - 5
                        return
                self.roundCall.draw()
            if self.timer > self.endTimer:
                choice = self.player2.name
                name = self.player1.name
                if storyManager.mode == "Game":
                    if self.wins[1] > 1:
                        self.round = 0
                        self.wins = [0,0]
                        self.player1.finishImage = self.player1.loseImage
                        self.player2.finishImage = self.player2.winImage
                        self.MenuGraphics()
                        return
                    del self.player1
                    del self.player2
                    self.Make_Players(name, choice, AI=self.AIs)

                #Return to story if in Story mode
                if storyManager.mode == "Story":
                    if self.wins[0] > 1:
                        self.round = 0
                        self.wins = [0,0]
                    self.Make_Players(self.player1.name, choice, AI=self.AIs)
                self.timer = 0
                self.round += 1

        #Double K.O
        elif self.player1.alive == False and self.player2.alive == False:
            self.player1.isControlled = False
            self.player2.isControlled = False
            self.timer += .2
            self.winner = "Double"
            if self.timer > self.deathTimer:
                self.roundCall.text = "DOUBLE \n     K.O"
                self.roundCall.draw()
            if self.timer > self.endTimer:
                name = self.player1.name
                choice = self.player1.name   
                if self.wins[1] > 1  and self.wins[0] > 1:
                    self.round = 0
                    self.wins = [0,0]
                del self.player1
                del self.player2
                self.Make_Players(name, choice2, AI=self.AIs)
                self.timer = 0
                self.round += 1
                self.wins[0] += 1
                self.wins[1] += 1

        #Pause
        if self.timer > self.endTimer - 40:
            self.winner = "None"
            self.targetOpacity = 255

##        if self.timer >= self.endTimer:
##            self.Build_BG()
            
        if self.timer > 0:
            self.player1.pause = True
            self.player2.pause = True
            
        if self.timer > 27:
            self.player1.pause = False
            self.player2.pause = False


    def MenuGraphics(self):
        menuManager.stage = "Finish"
        menuManager.mode = "Menu"
        menuManager.player = self.player1
        menuManager.enemy = self.player2
        menuManager.enemy.finishImage.scale_x = -1
        menuManager.update_menu_objects()
        menuManager.update_all_menu_objects()

    #This method is about a champion going into the blocking state
    def UpdateBlocking(self, p1, p2):
        attacking_actions = [2, 2.5, 3, 3.5, 8, 9, 10, 10.5, 11, 11.5, 12, 17.3, 12.5, 12.8, 18, 19, 30, 30.1, 30.2]
        #Players First
        if p1.action != 13.5 and p1.action != 14.5:
            if p2.action in attacking_actions:
                if p1.state == "Grounded" or p1.state == "Crouch":
                    p1.blockWait = 0
                    if p1.left and p2.pos[0] + p2.body[0] > p1.pos[0] + p1.body[0]:
                        p1.action = 13
                        if p1.state == "Crouch":
                            p1.action = 14
                        p1.left = False
                        p1.blockLeft = True
                    if p1.right and p1.pos[0] + p1.body[0] + p1.body[2] > p2.pos[0] + p2.body[0] + p2.body[2]:
                        p1.action = 13
                        if p1.state == "Crouch":
                            p1.action = 14
                            p1.blockWait = 10
                        p1.right = False
                        p1.blockRight = True
                    
        #Blocking Projectiles
        if len(p2.balls) > 0:
            if p1.state == "Grounded" or p1.state == "Crouch":
                p1.blockWait = 0
                if p1.left and p2.pos[0] + p2.body[0] > p1.pos[0] + p1.body[0]:
                    p1.action = 13
                    if p1.state == "Crouch":
                        p1.action = 14
                    p1.left = False
                    p1.blockLeft = True
                if p1.right and p1.pos[0] + p1.body[0] + p1.body[2] > p2.pos[0] + p2.body[0] + p2.body[2]:
                    p1.action = 13
                    if p1.state == "Crouch":
                        p1.action = 14
                    p1.right = False
                    p1.blockRight = True


    def Distance(self, p1, p2):
        dist = math.sqrt(math.pow(p1.hitBox[0] - p2.hitBox[0],2) + math.pow(p1.hitBox[1] - p2.hitBox[1],2))
        return dist
    
    #This method is to check if "victim" is in the blocking state, if not it takes damage and goes into the hit state
    def hit_collide(self, victim, attacker):
        blocks = [13, 13.5, 14, 14.5]
        if attacker.name != "Fireball": 
            if attacker.superSkill or victim.superSkill:
                return
            if attacker.action in blocks or attacker.parry:
                return

            
        #Check for projectile collisions
        if attacker.name == "Fireball" and victim.name == "Fireball":
            if self.Distance(attacker, victim) < 40:
                if attacker.damage > victim.damage:
                    victim.Hit_Connect(attacker)
                    attacker.damage -= victim.damage
                else:
                    attacker.Hit_Connect(victim)
                self.player1.Play("Audio/fire_ball.wav")
            return
        #Hit
        if attacker.hitBox[0] + attacker.hitBox[2] > victim.body[0] and attacker.hitBox[0] + attacker.hitBox[2] < victim.body[0] + victim.body[2] \
           or attacker.hitBox[0] > victim.body[0] and attacker.hitBox[0] < victim.body[0] + victim.body[2]:
            if attacker.hitBox[1] > victim.body[1] and attacker.hitBox[1] < victim.body[1] + victim.body[3] \
               or attacker.hitBox[1] + attacker.hitBox[3] > victim.body[1] and attacker.hitBox[1] + attacker.hitBox[3] < victim.body[1] + victim.body[3]:


                #Check if attacker is catching
                if victim.toGrab:
                    attacker.action = attacker.grabChain
                    attacker.frame = 0
                    attacker.jump = False
                    attacker.vel[1] = 0
                    attacker.vel[0] = 0
                    victim.toGrab = False
                    attacker.pos[1] = attacker.ground
                    return

                #Check if attacker is not a fireball
                if attacker.name != "Fireball":
                    if attacker.isGrabbing:
                        if attacker.targetGrabbed == None:
                            attacker.targetGrabbed = victim
                            attacker.Play("Audio/catching.wav")
                            attacker.frame = 0
                            attacker.action = 22
                            victim.action = 23
                            victim.isGrabbed = True
                        return                        

                        
                #Check first if the victim is blocking
                if self.Block(attacker, victim):
                    if victim.hitCD < 0:
                        cam.shakeTime = .5
                        vfx_list.append(Ball(pos=(attacker.hitBox[0] - 15, attacker.hitBox[1] - 10), loop=False, destroy=3, width=100, height=70, speed=2, img="sprites/hitVfx.png", row=5, col=1))
                        victim.Get_Hit(attacker=attacker, typeHit="Block", damage=attacker.damage, force=attacker.force)
                    return
                    
                #If not deal damage
                if victim.hitCD < 0:
                    if attacker.name != "Fireball":
                        if victim.parry and attacker.jump == False and victim.rageBar >= 200:
                            attacker.frameSpeed = 0
                            victim.vfx.append(Ball(pos=(victim.pos[0] - 20, victim.pos[1] - 20), name="VFX", loop=False, destroy=3, width=225, height=225,
                                                  speed=.2, img="sprites/special.png", row=4, col=2))  
                            victim.Play("Audio/Champs/Ryu/special.wav")
                            attacker.PlayVoice("Audio/Champs/"+attacker.name+"/Hurt/"+random.choice(attacker.hurts))
                            attacker.Get_Hit(attacker=attacker, typeHit="Damage", damage=0, force=[0,0])
                            victim.action = "Parry"
                            victim.rageBar -= 200
                            victim.frame = 0
                            return
                    cam.shakeTime = .5
                    victim.fallDirection = attacker.direction
                    vfx_list.append(Ball(pos=(attacker.hitBox[0] - 15, attacker.hitBox[1] - 10), loop=False, destroy=3, width=100, height=70, speed=2, img="sprites/hitVfx.png", row=5, col=1))
                    attacker.Hit_Connect(victim)
                    if victim.health <= 0 and self.ko.frame > int(len(self.ko.cells)):
                        self.ko.frame = 0


                    #This is variation sensitive
                    if attacker.name == "Fireball":
                        if attacker.owner is not None:
                            if attacker.owner.name == "Ryu" and victim.action != 6.7:
                                if attacker.owner.targetVariation == "Dragon Born":
                                    attacker.owner.rageBar += 50
                                if attacker.owner.targetVariation == "Dragon Born":
                                    attacker.owner.rageBar += 50

    #This method is to check if both hitBoxes collide          
    def Block(self, p1, p2):
        blocks = [13, 13.5, 14, 14.5]
        if p1.name == "Fireball":
            return
        if p1.action in blocks:
            return
        
        if p2.action in blocks:
            if p1.hitBox[0] + p1.hitBox[2] > p2.hitBox[0] and p1.hitBox[0] + p1.hitBox[2] < p2.hitBox[0] + p2.hitBox[2] \
               or p1.hitBox[0] > p2.hitBox[0] and p1.hitBox[0] < p2.hitBox[0] + p2.hitBox[2]:
                if p1.hitBox[1] > p2.hitBox[1] and p1.hitBox[1] < p2.hitBox[1] + p2.hitBox[3] \
                   or p1.hitBox[1] + p1.hitBox[3] > p2.hitBox[1] and p1.hitBox[1] + p1.hitBox[3] < p2.hitBox[1] + p2.hitBox[3]:
                    return True
        if len(p1.balls) > 0:
            return True
        

    def Build_BG(self):
        cam.stageWidth = 0
        self.back_ground = []
        self.fore_ground = []
        f = open(menuManager.bgs[menuManager.stageSelectID],'r')
        data = f.read()
        f.close()
        data = data.split('\n')
        world = []
        for row in data:
            if row.startswith('//') == False:
                world.append(row)
            

        #Base
        #Back Ground
        e = 3
        for w in range(int((len(world) - 2)/2)):
            #General
            image = world[w+e-1].split(';')[1]
            spawnType = world[w+e-1].split(';')[2]
            loop = world[w+e].split(';')[0].split(':')[1]
            offset = [int(world[w+e].split(';')[1].split(':')[1].split(',')[0]), int(world[w+e].split(';')[1].split(':')[1].split(',')[1])]
            cameraType = float(world[w+e-1].split(';')[3].split(':')[1])
            zpos = 0

                       
            #Data 
            if spawnType:
                startPoint = 0
                anim = False
                length = 0
                speed = 0
                vel_x = 0
                vel_y = 0
                soundTime = 0
                zpos = 0
                soundPath = ""   
                volume = 0
                size = 1
                value = world[w+e].split(';')
                for v in range(len(value)):
                    if value[v].split(':')[0] == ' startpoint':
                        startPoint = float(value[v].split(':')[1]) 
                    if value[v].split(':')[0] == ' anim':                   
                        anim = value[v].split(':')[1]
                    if value[v].split(':')[0] == ' length':                         
                        length = int(value[v].split(':')[1])
                    if value[v].split(':')[0] == ' speed': 
                        speed = float(value[v].split(':')[1])
                    if value[v].split(':')[0] == ' vel_x': 
                        vel_x = float(value[v].split(':')[1])
                    if value[v].split(':')[0] == ' vel_y': 
                        vel_y = float(value[v].split(':')[1])
                    if value[v].split(':')[0] == ' sound': 
                        soundTime = float(value[v].split(':')[1])
                    if value[v].split(':')[0] == ' soundPath': 
                        soundPath = value[v].split(':')[1]
                    if value[v].split(':')[0] == ' volume': 
                        volume = float(value[v].split(':')[1])
                    if value[v].split(':')[0] == ' zpos': 
                        zpos = float(value[v].split(':')[1])
                    if value[v].split(':')[0] == ' size': 
                        zpos = float(value[v].split(':')[1])

            #If The SpawnType is a Background Object
            if spawnType == ' BG' or spawnType == ' BG2':
                for d in range(int(loop)):
                    self.back_ground.append(Background(pos=(startPoint + (d * offset[0]), offset[1]), img=image, zpos=zpos, size=size, cameraType=cameraType))
                    if spawnType == ' BG':
                        cam.stageWidth += self.back_ground[-1].sprite.width
                    
            if spawnType == ' FG':
                for d in range(int(loop)):
                    self.fore_ground.append(Background(pos=(d * offset[0], offset[1]), img=image, zpos=zpos, size=size, cameraType=cameraType))

            #If The SpawnType is a Prop Object
            if spawnType == ' Prop':
                for d in range(int(loop)):
                    self.back_ground.append(Prop(pos=(startPoint + (d * offset[0]), offset[1]), zpos=zpos, img=image, anim=anim, length=length, speed=speed,
                                                 velX=vel_x, velY=vel_y, soundTime=soundTime,cameraType=cameraType, soundPath=soundPath, volume=volume))
            e += 1

        if menuManager.mode == "Story_Mode":
            return
            self.PlayMusic(storyManager.music)
        else:
            if menuManager.mode == "Game":
                self.PlayMusic(menuManager.music[menuManager.stageSelectID])
  
    def Click(self, button):
            canChange = True
            resetButton = True
            
            #Login Screen
            if menuManager.stage == "PlayerDetails":
                if self.targetInput != None:
                    if self.targetInput.user_text != "":
                        player_name = self.targetInput.user_text
                        self.playerNameText.text = player_name
                        SavePlayerData(name=player_name)
                        self.targetInput = None
                        menuManager.update_menu_objects()
                    else:
                        canChange = False
                else:
                    canChange = False

            if button.name.startswith("Controls"):
                canChange = False
                self.isSettingKeys = button.next.split('_')[-1]
                resetButton = False
                return
                    
            #Selecting an Icon
            if menuManager.stage == "PlayerIcon":
                SavePlayerData(name=self.playerNameText.text, icon=button.name)
                self.playerIcon = pyglet.sprite.Sprite(pyglet.image.load("UI/PlayerData/Icons/"+button.name+".png"), x=20, y=460 + big_screen[1], batch=self.menu_batch)
                self.playerIcon.scale_x = .5
                self.playerIcon.scale_y = .5
                
            #If targetInput is not null reset it
            if self.targetInput != None:
                self.targetInput.active = False
                self.targetInput = None

            if canChange:
                menuManager.Change(button)
                menuManager.starter = True
                
            if button.name == "story_mode":
                self.Make_Story_Characters()

            if button.name == "exit_game":
                self.PlayMusic("BGM/BGM.mp3")

            if button.name == "Save":
                self.SaveJoystickKeys()
                print("Saved Data")
                
            if button.name == "Exit":
                self.close()
                pyglet.app.exit()
                
            if button.name == "Begin":
                self.stallTime = self.maxStallTime
                menuManager.stage = "Battle"
                menuManager.enemy = random.choice(menuManager.charSelect)
            if button.name == "next" or button.name == "prev":
                resetButton = False

            menuManager.player = menuManager.charSelect[menuManager.charSelectID]
            menuManager.update_menu_objects(resetButton)
            menuManager.update_all_menu_objects()
        
    #Inputs_Begin
    def on_mouse_press(self, x, y, button, modifiers):   
        if menuManager.mode == "Menu":
            self.stallTime = self.maxStallTime
            if button == mouse.LEFT:
                hasClicked = False
                for mb in menuManager.draw_list:
                    if mb.on_click(x,y) and hasClicked == False:
                        if mb.type == "InputField":
                            self.targetInput = mb.get_click()
                            hasClicked = True

                        #In Case of Buttons
                        if mb.type == "Button":
                            canChange = True

                            #Login Screen
                            if menuManager.stage == "PlayerDetails":
                                if self.targetInput != None:
                                    if self.targetInput.user_text != "":
                                        player_name = self.targetInput.user_text
                                        self.playerNameText.text = player_name
                                        SavePlayerData(name=player_name)
                                        self.targetInput = None
                                        menuManager.update_menu_objects()
                                    else:
                                        canChange = False
                                else:
                                    canChange = False
                                    
                            #Selecting an Icon
                            if menuManager.stage == "PlayerIcon":
                                SavePlayerData(name=self.playerNameText.text, icon=mb.name)
                                self.playerIcon = pyglet.sprite.Sprite(pyglet.image.load("UI/PlayerData/Icons/"+mb.name+".png"), x=20, y=460 + big_screen[1], batch=self.menu_batch)
                                self.playerIcon.scale_x = .5
                                self.playerIcon.scale_y = .5
                                
                            #If targetInput is not null reset it
                            if self.targetInput != None:
                                self.targetInput.active = False
                                self.targetInput = None

                            if canChange:
                                menuManager.Change(mb)
                            if mb.name == "story_mode":
                                self.Make_Story_Characters()

                            if mb.name == "exit_game":
                                self.PlayMusic("BGM/BGM.mp3")
                                
                            if mb.name == "Begin":
                                self.stallTime = self.maxStallTime
                                menuManager.stage = "Battle"
                                menuManager.enemy = random.choice(menuManager.charSelect)
                                
                            self.PlaySound("Audio/Sys/20H.wav")
                            hasClicked = True
                    menuManager.player = menuManager.charSelect[menuManager.charSelectID]
                menuManager.update_all_menu_objects()
                        
                        

        #Exit
        if menuManager.stage == "Exit":
            self.on_close()

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
##        for mb in menuManager.draw_list:
##            mb.IsHover(x,y)
        pass

    def IsDecimal(self, number):
        return len(str(number).split('.')) > 1
    
    def SaveJoystickKeys(self):
        pickle.dump(self.joystickKeys, open("data/JoystickKeys.txt", "wb"))

    def UpdateJoystickVisuals(self):
        for b in menuManager.menu_objects:
            if b.type == "Text":
                if b.name == "key_WP":
                    b.sprite.text = str(self.joystickKeys[0])
                if b.name == "key_MP":
                    b.sprite.text = str(self.joystickKeys[1])
                if b.name == "key_WK":
                    b.sprite.text = str(self.joystickKeys[2])
                if b.name == "key_MK":
                    b.sprite.text = str(self.joystickKeys[3])
                if b.name == "key_Super":
                    b.sprite.text = str(self.joystickKeys[4])
                if b.name == "key_Grab":
                    b.sprite.text = str(self.joystickKeys[5])
        
    def JoystickMovement(self):            
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                print(event)
                if menuManager.mode == "Game":
                    #Weak Kick
                    if event.button == self.joystickKeys[2]:
                        self.player2.Attack_Kick("WK")
                    #Medium Kick
                    if event.button == self.joystickKeys[3]:
                        self.player2.Attack_Kick("MK")
                    #Medium Punch
                    if event.button == self.joystickKeys[0]:
                        self.player2.Attack_Punch("WP")
                    #Weak Punch
                    if event.button == self.joystickKeys[1]:
                        self.player2.Attack_Punch("MP")
                    #Grab
                    if event.button == self.joystickKeys[5]:
                        self.player2.Attack_Punch("IP")
                    #Super
                    if event.button == self.joystickKeys[4]:
                        self.player2.Attack_Punch("SP")

                if menuManager.mode == "Menu":
                    goOn = True
                    if event.button != 3:
                        #Setting Player Keys
                        if self.isSettingKeys == "WP":
                            self.isSettingKeys = False
                            self.joystickKeys[0] = event.button
                            self.UpdateJoystickVisuals()
                            goOn = False
                        if self.isSettingKeys == "MP":
                            self.isSettingKeys = False
                            self.joystickKeys[1] = event.button
                            self.UpdateJoystickVisuals()
                            goOn = False
                        if self.isSettingKeys == "WK":
                            self.isSettingKeys = False
                            self.joystickKeys[2] = event.button
                            self.UpdateJoystickVisuals()
                            goOn = False
                        if self.isSettingKeys == "MK":
                            self.isSettingKeys = False
                            self.joystickKeys[3] = event.button
                            self.UpdateJoystickVisuals()
                            goOn = False
                        if self.isSettingKeys == "Super":
                            self.isSettingKeys = False
                            self.joystickKeys[4] = event.button
                            self.UpdateJoystickVisuals()
                            goOn = False
                        if self.isSettingKeys == "Grab":
                            self.isSettingKeys = False
                            self.joystickKeys[5] = event.button
                            self.UpdateJoystickVisuals()
                            goOn = False

                    
                    if self.isSettingKeys == False:
                        #Moving the Menu Buttons
                        if event.button == 4:
                            menuManager.Move_Cursor("Up")
                        if event.button == 6:
                            menuManager.Move_Cursor("Down")
                        if event.button == 7:
                            menuManager.Move_Cursor("Left")
                        if event.button == 5:
                            menuManager.Move_Cursor("Right")
                        #Select A Button
                        if event.button == 14 and goOn == True:
                            self.PlaySound("Audio/Sys/20H.wav")
                            self.Click(menuManager.selectedItem)


                #Escape
                if event.button == 3:
                    if menuManager.mode == "Game":
                        menuManager.mode = "Menu"
                        window.set_exclusive_mouse(False)
                        menuManager.stage = "Paused"
                        menuManager.starter = True
                        menuManager.update_menu_objects()
                        return
                    
                    #Return to game
                    if menuManager.mode == "Menu":
                        if menuManager.stage == "Paused":
                            menuManager.mode = "Game"
                            window.set_exclusive_mouse(True)
                            menuManager.update_menu_objects()
                            return
                        
                        if menuManager.stage == "Battle":
                            return
                        self.close()
                        pyglet.app.exit()

                    if menuManager.mode == "WatchGame":
                        self.Reset()
                        
                    
            if event.type == pygame.JOYBUTTONUP:
                pass
            
            if event.type == pygame.JOYAXISMOTION:                              
                if menuManager.mode == "Game":
                    value = .3
                    #Left And Right
                    if event.axis == 0:
                        #Axis Left
                        if event.value < -value:
                            if self.joyStickLeft == False:
                                self.player2.KeyDown("Left")
                                self.joyStickLeft = True
                            self.player2.KeyUp("Right")
                        #Axis Right
                        if event.value > value:
                            if self.joyStickLeft == False:
                                self.player2.KeyDown("Right")
                                self.joyStickLeft = True
                            self.player2.KeyUp("Left")
                        #Reset
                        if event.value < value and event.value > -value:
                            self.player2.KeyUp("Left")
                            self.player2.KeyUp("Right")
                            self.joyStickLeft = False
                            self.joyStickRight = False
                        
                    #Up And Down
                    if event.axis == 1:
                        if event.value < -value:
                            if self.joyStickUp == False:
                                self.player2.KeyDown("Up")
                                self.joyStickUp = True
                            self.player2.KeyUp("Down")
                        if event.value > value:
                            if self.joyStickDown == False:
                                self.player2.KeyDown("Down")
                                self.joyStickDown = True
                            self.player2.KeyUp("Up")
                        if event.value < value and event.value > -value:
                            self.player2.KeyUp("Up")
                            self.player2.KeyUp("Down")
                            self.joyStickUp = False
                            self.joyStickDown = False
                        
                    
            if event.type == pygame.JOYHATMOTION:
                print(event)

            
    #Check For Key Presses
    def on_key_press(self, symbol, modifiers):
        if menuManager.stage != "Battle":
            self.stallTime = self.maxStallTime
            
        keys = {'113': "Q", '119': 'W', '101': 'E', '114': 'R', '116': 'T', '121': 'Y', '117': 'U', '105': 'I', '111': 'O', '112': 'P', '97': 'A', '115': 'S', '100': 'D',
                '102': 'F', '103': 'G', '104': 'H', '106': 'J', '107': 'K', '108': 'L', '122': 'Z', '120': 'X', '99': 'C', '118': 'V', '98': 'B', '110': 'N', '109': 'M',
                '32': ' ', '304': '^'}
##        print(symbol)
        if self.targetInput != None:
            #Caps Lock
            if symbol == 65509:
                self.caps = not self.caps
            #Backspace
            if symbol == 65288:
                text = self.targetInput.user_text[:-1]
                self.targetInput.user_text = text
                self.targetInput.text.text = self.targetInput.user_text
            try:
                if self.targetInput.user_text == "" or self.targetInput.user_text[-1:] == " ":
                    self.targetInput.user_text += keys[str(symbol)]
                else:
                    if self.caps == False:
                        self.targetInput.user_text += keys[str(symbol)].lower()
                    else:
                        self.targetInput.user_text += keys[str(symbol)]
                self.targetInput.text.text = self.targetInput.user_text
            except:
                print("Can't use that value")

        #Config.
        if self.checking:
            self.newKeys.append(symbol)
            
        if symbol == key.Q:
            self.newKeys = []
            self.checking = not self.checking

        if menuManager.mode == "Game":
            if self.targetInput == None:
                if symbol == key.RIGHT:
                    self.player1.KeyDown("Right")
                        

                if symbol == key.LEFT:
                    self.player1.KeyDown("Left")
                        
                if symbol == key.DOWN:
                    self.player1.KeyDown("Down")
                        
                if symbol == key.UP:
                    self.player1.KeyDown("Up")

                #Attacks
                #Punches
                if symbol == key.Q:
                    self.player1.Attack_Punch("WP")
                        
                if symbol == key.W:
                    self.player1.Attack_Punch("MP")
                        
                if symbol == key.E:
                    self.player1.Attack_Punch("SP")

                #Kicks
                if symbol == key.A:
                    self.player1.Attack_Kick("WK")
                        
                if symbol == key.S:
                    self.player1.Attack_Kick("MK")
                        
                if symbol == key.D:
                    self.player1.Attack_Kick("SK")

                #Interactables_Punch
                if symbol == key.R:
                    self.player1.Attack_Punch("IP")
                #Interactables_Kick
                if symbol == key.F:
                    self.player1.Attack_Punch("IK")
                        

        if symbol == key.ESCAPE:
            if menuManager.mode == "Game":
                menuManager.mode = "Menu"
                window.set_exclusive_mouse(False)
                menuManager.stage = "Paused"
                menuManager.update_menu_objects()
                return
            
            #Return to game
            if menuManager.mode == "Menu":
                if menuManager.stage == "Paused":
                    menuManager.mode = "Game"
                    window.set_exclusive_mouse(True)
                    menuManager.update_menu_objects()

            if menuManager.mode == "WatchGame":
                self.Reset()

            else:
                if menuManager.stage == "Battle":
                    return
                self.close()
                pyglet.app.exit()

    def Reset(self):
        menuManager.mode = "Menu"
        menuManager.stage = "Main"
        self.champs = []
        self.player1 = None
        self.player2 = None
        window.set_exclusive_mouse(False)
        menuManager.update_menu_objects()
        self.AI = None
        self.AI2 = None
        
    #Release
    def on_key_release(self, symbol, modifiers):


        if menuManager.mode == "Game":
            if symbol == key.Q:
                self.player1.KeyUp("WP")
                    
            if symbol == key.W:
                self.player1.KeyUp("MP")

            #Kicks
            if symbol == key.A:
                self.player1.KeyUp("WK")
                    
            if symbol == key.S:
                self.player1.KeyUp("MK")

                
                
            if symbol == key.RIGHT:
                self.player1.KeyUp("Right")

            if symbol == key.LEFT:
                self.player1.KeyUp("Left")
                    
            if symbol == key.DOWN:
                self.player1.KeyUp("Down")
                    
            if symbol == key.UP:
                self.player1.KeyUp("Up")

    def Make_Story_Characters(self):
        #Make Story Characters
        for champ in menuManager.charSelect:
            self.Make_Players(champ.name, "Ken", AI=self.AIs)
            menuManager.stageSelectID = storyManager.bg
            storyManager.champions.append(self.player1)
        self.Build_BG()
        storyManager.SetPositions()
        storyManager.mode = "Story"

                
    #Update all images on the Game Screen
    def on_draw(self):
        self.clear()
                
        #Visuals
        if self.isSettingKeys != False:
            self.joystickText.draw()
            
        if menuManager.mode == "Menu":
            self.playerBoarder.draw()
            self.menu_batch.draw()
            cam.Update_UI(menuManager.draw_list)
            
            if menuManager.stage == "Battle":
                self.loadingBar.scale_x = (self.stallTime / 125) * 50
                self.loadingBar.draw()

            
        ############################## Story #################################
        if menuManager.mode == "Story":
            cam.Draw_Story_Characters(storyManager.champions)

            #Draw Fore-Ground Objects
            if self.targetOpacity >= 0:
                cam.update_fore_ground_objects(self.fore_ground)
                
            cam.AnchorTarget(storyManager.camFocus.pos[0])
            
            #Player Directions
            for champ in storyManager.champions:
                self.UpdatePlayerDirections(champ)
                champ.opponent = storyManager.targetDirection

            #Checking for Super Skill
            for c in storyManager.champions:
                for ch in storyManager.champions:
                    if c is not ch:
                        self.hit_collide(c, ch)
                        self.UpdateBlocking(c, ch)
                        for b in c.balls:
                            b.hit_collide(ch)
                if c.superSkill:
                    self.targetOpacity = 100
                    self.transitionSpeed = 10
                    self.bgTransition.draw()
                    cam.Raw_Draw(storyManager.champions)

            self.story_batch.draw()


            #Updating Visuals
            if storyManager.canDraw:
                self.chatText.text = storyManager.chat
                self.chatImage = storyManager.head
                self.chatBox.draw()
                self.chatImage.draw()
                self.chatText.italic = storyManager.italic
                self.chatText.draw()

            if storyManager.speechBubble:
                storyManager.speechBubble.x = storyManager.camFocus.pos[0] - cam.pos[0]
                storyManager.speechBubble.y = storyManager.camFocus.pos[1] + 240
                storyManager.speechBubble.draw()

            #Update Players particles
            for v in self.champions:
                for vx in v.balls:
                    cam.update_vfx(vx.vfx)
                for vfx in v.vfx:
                    cam.update_vfx(vfx.vfx)
            cam.update_vfx(vfx_list)
            ### UI_end###
            
        ##############################################################
        
        if menuManager.mode == "Game" or menuManager.mode == "WatchGame":
            if self.targetOpacity <= 200:
                cam.update_back_ground_objects(self.back_ground)

            #Draw Players
            cam.update_player_objects(self.champions)

            #Draw Fore-Ground Objects
            if self.targetOpacity <= 200:
                cam.update_fore_ground_objects(self.fore_ground)            

            #UI
            self.UpdateHealthBars()

            #Start Game
            if self.startGame:
                self.roundCall.draw()
                
            self.main_batch.draw()
            self.UpdateGlows()
            
            self.bgTransition.draw()

            #Check to see if either players have won
            if self.player1.alive == False or self.player2.alive == False:
                self.Check_Win()


            #Checking for Super Skill
            for c in self.champions:
                if c.alive:
                    if c.superSkill:
                        self.targetOpacity = 100
                        self.transitionSpeed = 10
##                        self.bgTransition.draw()
                        cam.Raw_Draw(self.champions)
                        break
                    else:
                        self.targetOpacity = 0
                else:
                    break
                

            #Update Players particles
            for v in self.champions:
                for vx in v.balls:
                    if self.player1.pause == False and self.player2.pause == False:
                        cam.update_vfx(vx.vfx)
            cam.update_vfx(vfx_list)
            self.Update_Hit_Combos()
            
            ### UI_end###

            #Dominant UI
            pyglet.gl.glFlush()
            self.fps_display.draw()
            self.ko.update()


            
    #The general update function
    def update(self, dt):
        self.Transition()
        #Joystick Controller
        self.JoystickMovement()
            
        ############################## Story #################################
        if menuManager.stage == "Story_Mode":    
            storyManager.update()            
            menuManager.mode = "Story"
            
        if storyManager.canPlayMusic == True:
            self.PlayMusic(storyManager.music)
            storyManager.canPlayMusic = False

        if menuManager.mode ==  "Story":
            if storyManager.currentMode == "Game":
                storyManager.currentMode = "None"
                self.Make_Players(storyManager.champs[0].name, storyManager.champs[1].name, AI=self.AIs)
                self.Build_BG()
                menuManager.mode = "Game"
                menuManager.stage = "Game"

        try:
            if float(self.fps_display.label.text) >= 30:
                self.fps_display.label.color = (200,100,0,255)
            if float(self.fps_display.label.text) >= 40:
                self.fps_display.label.color = (100,200,0,255)
            if float(self.fps_display.label.text) >= 50:
                self.fps_display.label.color = (0,255,0,255)
            if float(self.fps_display.label.text) < 30:
                self.fps_display.label.color = (255,0,0,255)
        except:
            pass

        if menuManager.mode == "Menu":
            if menuManager.stage == "Battle":
                self.stallTime -= 5 * dt
            else:
                self.stallTime -= .01 * dt
                
            if self.stallTime <= 0:
                if menuManager.stage == "Finish":
                    self.close()
                    pyglet.app.exit()
                    return
                
                choices = ["Ken", "M.Bison", "Ryu", "Cammy", "Fei'Long", "Chun'Li"]
                choice = random.choice(choices)
                if menuManager.stage == "Finish":
                    self.Reset()
                    return
                
                #Check if waiting for a match
                if menuManager.stage != "Battle":
                    self.PlaySound("Audio/Sys/22H.wav")
                    self.Make_Players(random.choice(choices), choice, AI=2)
                    self.AIs = 2
                    window.set_exclusive_mouse(True)
                    menuManager.mode = "WatchGame"

                #Check if waiting for a match after char select
                else:
                    self.stallTime = self.maxStallTime
                    choice = menuManager.enemy.name
                    self.AIs = 1
                    menuManager.player = menuManager.charSelect[menuManager.charSelectID]
                    self.Make_Players(menuManager.player.name, choice, AI=0)
                    window.set_exclusive_mouse(True)
                    menuManager.mode = "Game"
                self.Build_BG()

                
            
        ############################## Game #################################        
        if menuManager.mode == "Game" or menuManager.mode == "WatchGame":
            
            self.Player_Talks()
            if self.AIs > 1:
                if self.AI2.champion.isControlled:
                    self.AI2.Control()
            if self.AIs > 0:
                if self.AI.champion.isControlled:
                    self.AI.Control()

            if self.player1.pause == False and self.player2.pause == False:
                cam.Encapsulate(self.player2, self.player1)

            #Stop frames for players when either one enters a super state
            if self.winner == "None":
                #Player 1
                if self.player1.superSkill and self.player2.superSkill == False:
                    self.player2.pause = True
                else:
                    self.player2.pause = False
                #Player 2
                if self.player2.superSkill and self.player1.superSkill == False:
                    self.player1.pause = True
                else:
                    self.player1.pause = False
                    
            #Start Game
            if self.startGame:
                self.targetOpacity = 0
                self.startTimer += .8
                self.roundCall.text = "Round " + str(self.round)
                if self.startTimer > self.startTime:
                    self.roundCall.text = "Round " + str(self.round)+ "\n  Fight"
                    if self.startTimer > self.startTime + 20:
                        self.player1.isControlled = True
                        self.player2.isControlled = True
                        self.startTimer = 0
                        self.startGame = False
            self.roundCall.draw()

            #Player Directions
            for champ in self.champions:
                self.UpdatePlayerDirections(champ)

            #Check Blocking
            self.UpdateBlocking(self.player1, self.player2)
            self.UpdateBlocking(self.player2, self.player1)
            
            ########### Combos ###############
            
            self.MakeCombos(self.player1, self.player2)
            self.MakeCombos(self.player2, self.player1)
            
            ########### end ##################
            
            ########### Collisions ###########
            
            #Champions
            #Player 1
            for p in self.player1.balls:
                for p2 in self.player2.balls:
                    self.hit_collide(p, p2)
            #Attacking
            #Player 1
            self.hit_collide(self.player1, self.player2)
            #Player 2
            self.hit_collide(self.player2, self.player1)
            
            #Projectiles
            for b in self.player1.balls:
                self.hit_collide(self.player2, b)
            for b2 in self.player2.balls:
                self.hit_collide(self.player1, b2)

            ##### end #####



def MakeWindow():
    global window
    window = GameWindow(1000, 700, "Street Fighter X", resizable=False, vsync=True)
##    pyglet.clock.schedule_interval_soft(window.update, window.frame_rate)
##    cursor = window.get_system_mouse_cursor(window.CURSOR_WAIT)
##    window.set_mouse_cursor(cursor)
    window.set_fullscreen(fullscreen=fullScreen)
    pyglet.clock.schedule_interval(window.update, 1/100)
    pyglet.app.run()

class SplashScreen(pyglet.window.Window):
    #Initilize the Game Window
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(850,350)

        self.time = 100

    def on_draw(self):
        self.clear()
        sprite = pyglet.sprite.Sprite(pyglet.image.load("UI/splash.png"))
        sprite.draw()

    def update(self, dt):
        self.time -= 1
        if self.time <= 0:
##            self.time = math.inf
            self.close()
            pyglet.app.exit()
            MakeWindow()

if __name__ == "__main__":
    splashScreen = SplashScreen(200, 200, style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
    pyglet.clock.schedule_interval(splashScreen.update, 1/100)
    pyglet.app.run()








