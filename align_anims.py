import pyglet, pickle
from pyglet.window import key


def preload_image(img):
    return pyglet.image.load(img)

class Button():
    def __init__(self, x, y, image, name):
        self.x = x
        self.y = y
        self.name = name
        self.sprite = pyglet.sprite.Sprite(preload_image(image), x=x, y=y)

    def IsHover(self, x, y):
        if x < self.x + self.sprite.width and x > self.x \
           and y < self.y + self.sprite.height and y > self.y:
            return True

class Champion():
    def __init__(self, x=0, y=0, name=""):
        self.pos = [x,y]
        self.name = name
        self.defualt = ["sprites/"+name+"/"+name+".png", "sprites/"+name+"/"+name+"_2.png","sprites/burn.png"]
        self.champsAlignment = {"Chun'Li": [[10, 10, 150, 150], [10,10,150,150]], "Fei'Long": [[10, 10, 150, 150], [10,10,150,150]],
                                "Ryu": [[10, 10, 150, 100], [10,4,150,150]], "Ken": [[10, 10, 150, 100], [10,2,150,150]],
                                "Cammy": [[10, 10, 150, 100], [10,5,150,100]], "M.Bison": [[10, 10, 150, 100], [10,4,150,100]],
                                "Akuma": [[10, 10, 150, 100], [10,10,150,150]], "Anti-Ryu": [[10, 10, 150, 100], [10,4,150,150]],
                                "Monk": [[10, 7, 80, 80], [10,7,80,80]]}
        
        self.alignment = self.champsAlignment[name]
        
        #Frames and Animation
        self.targetCell = None
        self.cell = []
        self.frame = 90
        self.frames1 = []
        self.bdy = None
        self.switch = False

        self.hitBox = pyglet.sprite.Sprite(preload_image("sprites/hitBox.png"))

        
        #Align On The X Axis
        self.alignX = []

        #Align On The Y Axis
        self.alignY = []

        #HitBox Align On The X Axis
        self.hitBoxX = []
        
        #HitBox Align On The Y Axis
        self.hitBoxY = []
##        for vel in range(150):
##            self.alignX.append(0)
##            self.alignY.append(0)
##            self.hitBoxX.append(0)
##            self.hitBoxY.append(0)


    #function was made to make GameObject's Initilization easier       
    def __init__self__(self, row, col, width, height, img):
        image = pyglet.image.load(img)
        sprite_sheet = pyglet.image.ImageGrid(image, col, row, item_width=width, item_height=height)

        cell = sprite_sheet
        counting = len(cell)
        for d in range(col):
            counting -= row
            for n in range(row):
                self.cell.append(cell[counting + n])
        self.targetCell = self.cell


    def Save(self):
        data = [self.alignX, self.alignY, self.hitBoxX, self.hitBoxY]
        pickle.dump(data, open("data/" + self.name + ".txt", "wb"))

    def ResetFrame(self):
        self.hitBoxX[int(self.frame)] = 60
        self.hitBoxY[int(self.frame)] = 40

    def RemoveFrame(self):
        if self.frame > len(self.hitBoxX) - 1:
            for i in range(self.frame - len(self.hitBoxX)):
                self.hitBoxX.append(0)
                
        if self.frame > len(self.hitBoxY) - 1:
            for i in range(self.frame - len(self.hitBoxY)):
                self.hitBoxX.append(0)
        self.hitBoxX[int(self.frame)] = 1000
        self.hitBoxY[int(self.frame)] = 1000
        

    def Update(self):
        if self.frame > len(self.alignX) - 1:
            self.alignX.append(0)
            self.alignY.append(0)
            self.hitBoxX.append(0)
            self.hitBoxY.append(0)
            
        #Onion Skin
        if not self.switch:
            try:
                self.ghost = pyglet.sprite.Sprite(self.cell[self.frame - 1])
                self.ghost.x = self.pos[0] + self.alignX[int(self.frame)-1]
                self.ghost.y = self.pos[1] + self.alignY[int(self.frame)-1]
            except:
                self.ghost = pyglet.sprite.Sprite(self.cell[0])
                self.ghost.x = self.pos[0] + self.alignX[0]
                self.ghost.y = self.pos[1] + self.alignY[0]
                
        if self.switch:
            self.ghost = pyglet.sprite.Sprite(self.cell[0])
            self.ghost.x = self.pos[0] + self.alignX[0]
            self.ghost.y = self.pos[1] + self.alignY[0]
            
        self.ghost.opacity = 100

        #Sprite
        if int(self.frame) > len(self.cell):
            self.frame = len(self.cell) - 1
        self.bdy = pyglet.sprite.Sprite(self.cell[int(self.frame)])
        self.bdy.x = self.pos[0] + self.alignX[int(self.frame)]
        self.bdy.y = self.pos[1] + self.alignY[int(self.frame)]
            
        try:
            #HitBox
            self.hitBox.x = self.bdy.x + self.hitBoxX[int(self.frame)]
            self.hitBox.y = self.bdy.y + self.hitBoxY[int(self.frame)]

        except:
            #HitBox
            self.hitBoxX.append(0)
            self.hitBoxY.append(0)
            self.hitBox.x = self.bdy.x + self.hitBoxX[int(self.frame)]
            self.hitBox.y = self.bdy.y + self.hitBoxY[int(self.frame)]
    
class GameWindow(pyglet.window.Window):
    #Initilize the Game Window
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(100,70)
        self.frame_rate = 1/100.0

        self.batch = pyglet.graphics.Batch()
        self.buttons = []
        self.frame = 0
        self.shiftKey = False
        self.value = 1

        #Character List
        self.characterList = ["Chun'Li", "Fei'Long", "Ryu", "Ken", "Cammy", "M.Bison", "Monk", "Akuma", "Anti-Ryu"]
        self.listID = 0
        
        #Make the Sprite Container
        self.container = pyglet.sprite.Sprite(preload_image("AlignAnims/Sprite_Container.png"), x=224, y=174.5, batch=self.batch)

        self.LoadFile()

##        for f in range(len(self.object.alignX) - 1):
##            self.object.alignX[f] -= 20

        #UI
        self.wait = 10
        self.saved = True
        self.alpha = 255
        self.timer = self.wait
        self.pulseText = True

        #Texts
        self.dataState = "Saved Data"
        self.frameText = pyglet.text.Label("Frame: ", x=270, y=150, multiline=False, batch=self.batch)
        self.savedText = pyglet.text.Label(self.dataState, font_name="Broadway",  x=10, y=480, multiline=False, batch=self.batch)
        self.savedText.color = (255, 0, 0, 255)
##        self.savedText.document.set_style(0, 0, {'font_name': 'Algerian'})
        
        #Buttons
        #Whole File
        self.reset2 = Button(image="AlignAnims/reset.png", x=260, y=50, name="reset2")
        self.switch = Button(image="AlignAnims/switch.png", x=340, y=50, name="Switch")
        
        #Frames
        self.left_frame = Button(image="AlignAnims/left_frame.png", x=150, y=100, name="LeftFrame")
        self.right_frame = Button(image="AlignAnims/right_frame.png", x=389, y=100, name="RightFrame")
        self.reset = Button(image="AlignAnims/reset.png", x=140, y=400, name="Reset")
        self.remove = Button(image="AlignAnims/remove.png", x=380, y=400, name="Remove")
        
        #Alignment (Sprite)
        self.up = Button(image="AlignAnims/up.png", x=160, y=360, name="up")
        self.down = Button(image="AlignAnims/down.png", x=160, y=310, name="down")
        self.left =Button(image="AlignAnims/left.png", x=130, y=334.5, name="left")
        self.right = Button(image="AlignAnims/right.png", x=188, y=334.5, name="right")

        #Alignment (HitBox)
        self.upHitBox = Button(image="AlignAnims/up.png", x=430, y=360, name="upHitBox")
        self.downHitBox = Button(image="AlignAnims/down.png", x=430, y=310, name="downHitBox")
        self.leftHitBox =Button(image="AlignAnims/left.png", x=400, y=334.5, name="leftHitBox")
        self.rightHitBox = Button(image="AlignAnims/right.png", x=460, y=334.5, name="rightHitBox")
        

        #Save
        self.save = Button(image="AlignAnims/save.png", x=270, y=350, name="save")

        self.AddButtons()

    def LoadFile(self, name="Chun'Li"):
        #Sprite Object
        self.object = Champion(name=name, x=245, y=190)
        self.object.__init__self__(row=self.object.alignment[0][0], col=self.object.alignment[0][1], width=self.object.alignment[0][2], height=self.object.alignment[0][3], img=self.object.defualt[0])
        self.object.__init__self__(row=self.object.alignment[1][0], col=self.object.alignment[1][1], width=self.object.alignment[1][2], height=self.object.alignment[1][3], img=self.object.defualt[1])
        self.object.__init__self__(row=2, col=4, width=150, height=150, img=self.object.defualt[2])
##        self.object.__init__self__(row=10, col=10, width=150, height=150, img="sprites/"+self.object.name+"/"+self.object.name+"_glow.png")
        data = pickle.load(open("data/" + self.object.name + ".txt", "rb"))
        self.object.alignX = data[0]
        self.object.alignY = data[1]
        self.object.hitBoxX = data[2]
        self.object.hitBoxY = data[3]

    def AddButtons(self):
        self.buttons.append(self.left_frame)
        self.buttons.append(self.right_frame)
        self.buttons.append(self.up)
        self.buttons.append(self.down)
        self.buttons.append(self.left)
        self.buttons.append(self.right)
        self.buttons.append(self.upHitBox)
        self.buttons.append(self.downHitBox)
        self.buttons.append(self.leftHitBox)
        self.buttons.append(self.rightHitBox)
        self.buttons.append(self.reset)
        self.buttons.append(self.remove)
        self.buttons.append(self.save)
        self.buttons.append(self.reset2)
        self.buttons.append(self.switch)

    def SetSaved(self, state):
        if self.saved != state:
            self.saved = state
            self.timer = 10
            self.alpha = 255


    def on_mouse_motion(self, x, y, dx, dy):
        for b in self.buttons:
            if b.IsHover(x, y):
                b.sprite.opacity = 255
            else:
                b.sprite.opacity = 200
            
    def on_mouse_press(self, x, y, button, modifiers):
        for b in self.buttons:
            if b.IsHover(x, y):
                self.frame = self.object.frame
                
                #This reloads the whole file
                if b.name == "reset2":
                    self.LoadFile(self.characterList[self.listID])
                    if self.frame >= len(self.object.cell) - 1:
                        self.frame = len(self.object.cell) - 1
                    self.object.frame = self.frame
                    return
                
                #This reloads the whole file and makes a new character
                if b.name == "Switch":
                    self.listID += 1
                    oldFrame = self.object.frame
                    if self.listID > len(self.characterList) - 1:
                        self.listID = 0
                        
                    self.LoadFile(self.characterList[self.listID])
                    self.object.frame = oldFrame
                    print(self.object.frame)
                    return

                    
                if b.name == "RightFrame":
                    if self.object.frame < len(self.object.cell) - 1:
                        self.object.frame += 1
                if b.name == "LeftFrame":
                    if self.object.frame > 0:
                        self.object.frame -= 1

                #Alignment (Sprite)
                if b.name == "left":
                    self.object.alignX[self.object.frame] -= 1
                    self.SetSaved(False)
                if b.name == "right":
                    self.object.alignX[self.object.frame] += 1
                    self.SetSaved(False)
                if b.name == "up":
                    self.object.alignY[self.object.frame] += 1
                    self.SetSaved(False)
                if b.name == "down":
                    self.object.alignY[self.object.frame] -= 1
                    self.SetSaved(False)

                #Alignment (HitBox)
                if b.name == "leftHitBox":
                    self.object.hitBoxX[self.object.frame] -= 3
                    self.SetSaved(False)
                if b.name == "rightHitBox":
                    self.object.hitBoxX[self.object.frame] += 3
                    self.SetSaved(False)
                if b.name == "upHitBox":
                    self.object.hitBoxY[self.object.frame] += 3
                    self.SetSaved(False)
                if b.name == "downHitBox":
                    self.object.hitBoxY[self.object.frame] -= 3
                    self.SetSaved(False)

                #Saving and Loading
                if b.name == "save":
                    self.SetSaved(True)
                    self.object.Save()
                    
                #Reset HitBox and Frame
                if b.name == "Reset":
                    self.SetSaved(False)
                    self.object.ResetFrame()
                    
                #Remove HitBox and Frame
                if b.name == "Remove":
                    self.SetSaved(False)
                    self.object.RemoveFrame()


    
    #Inputs_Begin
    #Check For Key Presses
    def on_key_press(self, symbol, modifiers):
        if symbol == 65505:
            self.shiftKey = True
            
        #This reloads the whole file
        if symbol == key.R:
            self.LoadFile(self.characterList[self.listID])
            if self.frame >= len(self.object.cell) - 1:
                self.frame = len(self.object.cell) - 1
            self.object.frame = self.frame
            return
                
        #This reloads the whole file and makes a new character
        if symbol == key.T:
            self.listID += 1
            oldFrame = self.object.frame
            if self.listID > len(self.characterList) - 1:
                self.listID = 0
                
            self.LoadFile(self.characterList[self.listID])
            self.object.frame = oldFrame
            return

        if symbol == key.Q:
            self.object.switch = not self.object.switch
            
        if symbol == key.SPACE:
            self.SetSaved(True)
            self.object.Save()
            
        if symbol == key.RIGHT:
            if self.object.frame < len(self.object.cell) - 1:
                self.object.frame += 1
        if symbol == key.LEFT:
            if self.object.frame > 0:
                self.object.frame -= 1
            
        if symbol == key.W:
            self.object.alignY[self.object.frame] += self.value
            self.SetSaved(False)
        if symbol == key.S:
            self.object.alignY[self.object.frame] -= self.value
            self.SetSaved(False)
        if symbol == key.A:
            self.object.alignX[self.object.frame] -= self.value
            self.SetSaved(False)
        if symbol == key.D:
            self.object.alignX[self.object.frame] += self.value
            self.SetSaved(False)
            
        if symbol == key.ESCAPE:
            self.close()
            pyglet.app.exit()
            
    #Release
    def on_key_release(self, symbol, modifiers):
        if symbol == 65505:
            self.shiftKey = False

    def update(self, dt):
        self.clear()
        self.frameText.text = "Frame: " + str(self.object.frame)
        
        if self.shiftKey:
            self.value = 10
        else:
            self.value = 1


        #Text Fading in and out            
        if self.pulseText:
            self.timer -= .1
            if self.timer < 0:
                if self.alpha > 2:
                    self.alpha -= 2

 
        if self.saved:
            self.savedText.color = (0,255,0, self.alpha)
            self.dataState = "Saved Data"
        else:
            self.savedText.color = (255,0,0, self.alpha)
            self.dataState = "Save"
            
        for b in self.buttons:
            b.sprite.draw()
            
        self.savedText.text = self.dataState

        self.batch.draw()
        self.object.Update()
        self.object.ghost.draw()
        self.object.bdy.draw()
        self.object.hitBox.draw()


if __name__ == "__main__":
    window = GameWindow(600,500, "Layering Test", resizable=False)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
