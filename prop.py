import pyglet, random, math

class Prop:
    def __init__(self, pos=(0,0), velX=0, velY=0, anim='True', img="None", child=False, zpos=1, cameraType=1, length=4, soundTime=0, volume=.6, soundPath="", speed=.5):
        self.pos = list(pos)
        self.zpos = zpos
        self.vel_x = velX
        self.vel_y = velY
        choice = [speed - .12, speed - .13, speed - .1, speed - 0.05, speed, speed + .05, speed + .1, speed + .15, speed + .2]
        if child:
            choice = [0.15, .16, .17, .18, .19, .2]
        self.speed = random.choice(choice)
        self.cell = []
        self.frame = 0
        self.lifeTime = 15
        self.anim = anim
        self.sprite = pyglet.sprite.Sprite(self.preload_image(img + "_1.png"))

        self.cameraType = cameraType

        self.maxSoundTime = soundTime
        self.soundPath = soundPath        
        #Sounds
        if self.maxSoundTime > 0:
            self.volume = volume
            self.fade = 0
            self.soundTime = 0
            sound = pyglet.resource.media("Audio/" + soundPath, streaming=True)
            sound.play()
                
                

        for i in range(length):
            if anim == 'True':
                self.Add_Single(img=img + "_" + str(i+1) + ".png")

    def Add_Single(self, img):
        self.cell.append(self.preload_image(img))

    def preload_image(self, image):
        img = pyglet.image.load(image)
        return img


    def Animate(self):     
        self.frame += self.speed
        if int(self.frame) >= len(self.cell):
            self.frame = 0
        if len(self.cell) > 0:
            self.sprite = pyglet.sprite.Sprite(self.cell[int(self.frame)])
            
        
    def update(self):
        if self.anim:
            self.Animate()
        self.pos[0] += self.vel_x
        self.pos[1] += self.vel_y

        if self.maxSoundTime > 0:
            self.soundTime -= .05
            if self.soundTime <= 0:
                self.soundTime = self.maxSoundTime
                self.sound = pyglet.resource.media("Audio/" + self.soundPath, streaming=True)
                self.sound.play()
        #Update Positions
        self.sprite.x = self.pos[0]
        self.sprite.y = self.pos[1]


