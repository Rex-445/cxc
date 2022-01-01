import pyglet, random, math


class Ball:
    def __init__(self, pos=(0,0), velX=0, velY=0, length=2, direction=1, fade=False, name="Fireball", damage=50, force=[4,0], loop=True, destroy=0, speed=.3, row=0,
                 col=0, width=0, height=0, img="sprites/Medium_Energy_Ball.png", owner=None, broken="sprites/Ryu/Balls/broken_ball.png", size=[1,1], amber=None, bonusDamage=0):
        self.pos = list(pos)
        self.vel_x = velX        
        self.vel_y = velY
        self.name = name
        self.size = size
        self.destroy = destroy
        self.bonusDamage = bonusDamage
        self.owner = owner
        self.direction = direction
        self.force = force
        self.damage = damage
        self.cell = []
        self.hit_sprite = pyglet.sprite.Sprite(pyglet.image.load("sprites/hitBox.png"))
        self.canDestroy = False
        self.canDestroy = self.destroy > 0
        self.broken_sheet = broken
        self.vfx_sheet = amber

        self.alive = True
        self.fade = fade
        self.alpha = 255

        self.vfx = []
        self.vfxTime = 0
        #Animation
        self.frame = 0
        self.animLength = length
        self.animSpeed = speed
        self.loop = loop

        self.__init__self__(img=img, width=width, height=height, row=row, col=col)
        try:
            self.sprite = pyglet.sprite.Sprite(self.cell[0], x=self.pos[0], y=self.pos[1])
        except (Exception):
            pass

        #Collisions
        self.hitBox = [self.pos[0], 19, 82, 41]

        
    #function was made to make GameObject's Initilization easier       
    def __init__self__(self, row, col, width, height, img):
        img = pyglet.image.load(img)
        width = int(pyglet.sprite.Sprite(img).width / row)
        height = int(pyglet.sprite.Sprite(img).height / col)
        sprite_sheet = pyglet.image.ImageGrid(img, col, row, item_width=width, item_height=height)

        self.cell = sprite_sheet
        
            
    def Hit_Connect(self, victim):
        blocks = [13, 13.5, 14, 14.5]
        self.alive = False

        if victim.name != "Fireball":
            if victim.action in blocks:
                victim.Get_Hit(attacker=self, damage=self.damage, typeHit="Block", force=self.force)
                return
            victim.Get_Hit(attacker=self, damage=self.damage, typeHit="FireBall", force=self.force)
            if self.owner.name == "Anti-Ryu":
                self.owner.healLength += self.damage/2
            
    def update(self, big_screen=[0,0]):
        #Particle
        if self.vfx_sheet != None:
            self.vfxTime -= .15
            if self.vfxTime <= 0:
                self.vfxTime = 1
                pos = [random.randint(-20, 20), random.randint(-20,20)]
                self.vfx.append(Ball(pos=(self.pos[0] + pos[0] + 20, self.pos[1] + 20 + pos[1]), destroy=1, width=27, height=28, length=3, speed=.4, direction=self.direction,
                                    img=self.vfx_sheet, row=4, loop=False, velX=random.randint(-2,2)*self.direction, velY=random.randint(-1,1), col=1))
        #Animate
        self.frame += self.animSpeed
        if int(self.frame) > self.animLength:
            self.frame = 0
            if self.loop == False:
                self.alive =  False

        if self.alive:
            self.sprite = pyglet.sprite.Sprite(self.cell[int(self.frame)])
                
            self.pos[0] += self.vel_x * self.direction
            self.pos[1] += self.vel_y
            
            #Update Positions
            self.sprite.x = self.pos[0]
            self.sprite.y = self.pos[1] + big_screen[1]

            if self.direction == -1:
                self.hitBox = [self.pos[0] - 55, self.pos[1] + 19, 82, 41]
            if self.direction == 1:
                self.hitBox = [self.pos[0] - 15, self.pos[1] + 19, 82, 41]
                
            self.hit_sprite.x = self.hitBox[0]
            self.hit_sprite.y = self.hitBox[1]
            self.hit_sprite.scale_x = self.hitBox[3]/30
            self.hit_sprite.scale_y = self.hitBox[3]/30

            self.sprite.scale_x = self.size[0] * self.direction
            self.sprite.scale_y = self.size[1]
        #Fade
        if self.fade:
            self.alpha -= 5
            if self.alpha > 0:
                self.sprite.opacity = self.alpha
            if self.alpha <= 0:
                self.alive = False

class Broken:
    def __init__(self, pos=(0,0), velX=0, velY=0, speed=.3, direction=1, name="Broken", row=0,
                 col=0, img="sprites/Broken_Ball.png", size=[.7,.7]):
        self.pos = list(pos)
        self.img = img
        self.velX = velX
        self.size = size
        self.velY = velY
        self.alive = True
        self.cell = []
        self.speed = speed

        self.frame = 0
        self.direction = direction


        self.__init__self__(row, col, img)
        
    #function was made to make GameObject's Initilization easier       
    def __init__self__(self, row, col, img):
        img = pyglet.image.load(img)
        width = int(pyglet.sprite.Sprite(img).width / row)
        height = int(pyglet.sprite.Sprite(img).height / col)
        sprite_sheet = pyglet.image.ImageGrid(img, col, row, item_width=width, item_height=height)

        self.cell = sprite_sheet
        self.sprite = pyglet.sprite.Sprite(self.cell[int(self.frame)])
        
    def update(self, big_screen=[0,0]):
        self.frame += .3
        if int(self.frame) >= len(self.cell):
            self.alive = False

        if self.alive:
            self.sprite = pyglet.sprite.Sprite(self.cell[int(self.frame)])
            
            #Update Positions
            self.sprite.x = self.pos[0]
            self.sprite.y = self.pos[1]

            self.sprite.scale_x = self.size[0] * self.direction
            self.sprite.scale_y = self.size[1]

##            self.sprite.y -= big_screen[1]

vfx_list = []













        
























        
