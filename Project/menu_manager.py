import pyglet, math



class MenuManager():
    def __init__(self):
        self.stage = "Main"
        self.mode = "Menu"
        self.menu_objects = []
        self.draw_list = []
        self.charSelect = []
        paths = self.LoadBGFile("bg/data.txt")
        self.bgs = paths[0]
        self.music = paths[1]
        
        self.variation = None
        self.variationSelectID = 0
        self.charSelectID = 0
        self.stageSelectID = 0
        self.iconSelectID = 0
        self.skillCheckID = 0
        self.oneShot = False
        self.enemy = None
        self.player = None
        self.selectedItem = None
        self.starter = True
        self.updateMenu = True

    def LoadBGFile(self, file):
        f = open(file,'r')
        data = f.read()
        f.close()
        data = data.split('\n')
        BGS = []
        sounds = []

        #Store the BG path
        for d in range(len(data)):
            data2 = data[d].split(';')
            resource = data2[0].split(';')
            BGS.append(resource[0].split(':')[1])

        #Store the Sound path
        for d in range(len(data)):
            data2 = data[d].split(';')
            resource = data2[1].split(';')
            sounds.append(resource[0].split(':')[1])
        return BGS, sounds

    def update_menu_objects(self, resetButton=True):
        self.draw_list = []
        for m in self.menu_objects:
            if m.stage == self.stage:
                self.draw_list.append(m)
            if m.stage == self.stage[:-1]:
                self.draw_list.append(m)
                
        #Update the visuals
        for b in self.draw_list:
            if b.name == "Variation":
                b.sprite = self.variation
                b.sprite.x = b.pos[0]
                b.sprite.y = b.pos[1]

        for d in self.draw_list:
            d.IsHover(-1000,-1000)
                
            if resetButton:
                if d.first:
                    if self.starter:
                        self.starter = False
                        d.IsHover(d.pos[0] + 1,d.pos[1] + 1)
                        self.selectedItem = d
                    if self.selectedItem == None:
                        self.selectedItem = d
            elif d.name ==self.selectedItem.name:
                d.IsHover(d.pos[0] + 1,d.pos[1] + 1)

        if self.stage == "GAME":
            self.mode = "Game"

    def Move_Cursor(self, direction, forced=False):
            
        if self.selectedItem != None:
            item = self.selectedItem
            item.IsHover(-1000,-1000)
            #Moving the cursor left
            if direction == "Left":
                value = math.inf
                newItem = None
                newList = []
                for d in self.draw_list:
                    if d.pos[0] < self.selectedItem.pos[0]:
                        if d.type == "Button":
                            newList.append(d)
                        if d.pos[1] < self.selectedItem.pos[1] + (self.selectedItem.sprite.height * 2) \
                            and d.pos[1] > self.selectedItem.pos[1] - (self.selectedItem.sprite.height * 2):
                            if d.type == "Button":
                                dist = math.sqrt(math.pow(self.selectedItem.pos[0] - d.pos[0], 2))
                                if dist < value:
                                    value = dist
                                    item = d
                                    newItem = d

                #Check if the first attempt didn't work
                if newItem == None:
                    value = math.inf
                    for d in newList:
                        dist = math.sqrt(math.pow(self.selectedItem.pos[1] - d.pos[1], 2) + math.pow(self.selectedItem.pos[0] - d.pos[0], 2))
                        if dist < value:
                            value = dist
                            item = d
                    
            #Moving the cursor Right
            if direction == "Right":
                value = math.inf
                newItem = None
                newList = []
                for d in self.draw_list:
                    if d.pos[0] > self.selectedItem.pos[0]:
                        if d.type == "Button":
                            newList.append(d)
                        if d.pos[1] < self.selectedItem.pos[1] + (self.selectedItem.sprite.height * 2) \
                            and d.pos[1] > self.selectedItem.pos[1] - (self.selectedItem.sprite.height * 2):
                            if d.type == "Button":
                                dist = math.sqrt(math.pow(self.selectedItem.pos[0] - d.pos[0], 2))
                                if dist < value:
                                    value = dist
                                    item = d
                                    newItem = d

                #Check if the first attempt didn't work
                if newItem == None:
                    value = math.inf
                    for d in newList:
                        dist = math.sqrt(math.pow(self.selectedItem.pos[1] - d.pos[1], 2) + math.pow(self.selectedItem.pos[0] - d.pos[0], 2))
                        if dist < value:
                            value = dist
                            item = d
                            
                    
            #Moving the cursor Right
            if direction == "Up":
                value = math.inf
                newItem = None
                newList = []
                for d in self.draw_list:
                    if d.pos[1] > self.selectedItem.pos[1]:
                        if d.type == "Button":
                            newList.append(d)
                        if d.pos[0] < self.selectedItem.pos[0] + (self.selectedItem.sprite.width * 2) \
                            and d.pos[0] > self.selectedItem.pos[0] - (self.selectedItem.sprite.width * 2):
                            if d.type == "Button":
                                dist = math.sqrt(math.pow(self.selectedItem.pos[1] - d.pos[1], 2))
                                if dist < value:
                                    value = dist
                                    item = d
                                    newItem = d

                #Check if the first attempt didn't work
                if newItem == None:
                    value = math.inf
                    for d in newList:
                        dist = math.sqrt(math.pow(self.selectedItem.pos[1] - d.pos[1], 2) + math.pow(self.selectedItem.pos[0] - d.pos[0], 2))
                        if dist < value:
                            value = dist
                            item = d
                    
            #Moving the cursor Right
            if direction == "Down":
                value = math.inf
                newItem = None
                newList = []
                for d in self.draw_list:
                    if d.pos[1] < self.selectedItem.pos[1]:
                        if d.type == "Button":
                            newList.append(d)
                        if forced == False:
                            if d.pos[0] < self.selectedItem.pos[0] + (self.selectedItem.sprite.width * 2) \
                                and d.pos[0] > self.selectedItem.pos[0] - (self.selectedItem.sprite.width * 2):
                                if d.type == "Button":
                                    dist = math.sqrt(math.pow(self.selectedItem.pos[1] - d.pos[1], 2))
                                    if dist < value:
                                        value = dist
                                        item = d
                                        newItem = d

                #Check if the first attempt didn't work
                if newItem == None:
                    value = math.inf
                    for d in newList:
                        dist = math.sqrt(math.pow(self.selectedItem.pos[1] - d.pos[1], 2) + math.pow(self.selectedItem.pos[0] - d.pos[0], 2))
                        if dist < value:
                            value = dist
                            item = d
                    
                            
                            
                                    
            item.IsHover(item.pos[0] + 1,item.pos[1] + 1)
            self.selectedItem = item
            
            try:
                if item.name == self.selectedItem.name:
                    item.IsHover(item.pos[0] + 1,item.pos[1] + 1)
            except:
                pass

            self.selectedItem.IsHover(self.selectedItem.pos[0] + 1,self.selectedItem.pos[1] + 1)
            

    def full_screen(self, big_screen=[0,0]):
        for m in self.menu_objects:
            m.pos[0] +=  big_screen[0]
            m.pos[1] += big_screen[1]
            if m.type == "InputField":
                m.text.x = m.pos[0] + 15
                m.text.y = m.pos[1] + 23
            m.sprite.x = m.pos[0]
            m.sprite.y = m.pos[1]
            
    def update_all_menu_objects(self):
        self.updateMenu = True
        
        for c in self.charSelect:
            if self.variationSelectID < len(c.variation_names):
                c.targetVariation = c.variation_names[self.variationSelectID]
            #Character Description
            for des in self.draw_list:                    
                if des.type == "Image":
                    #Champions Potrait
                    if des.name == "UI_Potrait":
                        pos = des.pos
                        sprite = pyglet.sprite.Sprite(pyglet.image.load("sprites/Heads/"+self.player.name+"_head.png"))
                        des.sprite.image = sprite.image
                        des.sprite.x = pos[0]
                        des.sprite.y = pos[1]
                        
                    #Enemy Champion Potrait
                    if des.name == "Enemy_UI_Potrait":
                        pos = des.pos
                        sprite = self.enemy.select_head
                        des.sprite.image = sprite.image
                        des.sprite.x = pos[0]
                        des.sprite.y = pos[1]
                        
                    #Champions Win Icon
                    if des.name == "UI_Potrait_Finish":
                        pos = des.pos
                        sprite = self.player.finishImage
                        des.sprite.image = sprite.image
                        des.sprite.x = pos[0]
                        des.sprite.y = pos[1]
                        
                    #Enemy Champion  Win Icon
                    if des.name == "UI_Enemy_Potrait_Finish":
                        pos = des.pos
                        sprite = self.enemy.finishImage
                        des.sprite.image = sprite.image
                        des.sprite.x = pos[0]
                        des.sprite.y = pos[1]
                        
                    if des.name == "UI_BG":
                        pos = des.pos
                        sprite = pyglet.sprite.Sprite(pyglet.image.load(self.bgs[self.stageSelectID][:6]+ "UI_BG.png"), x=pos[0], y=pos[1])
                        des.sprite.image = sprite.image

                    if des.name == "Icon":
                        pos = des.pos
                        sprite = self.charSelect[self.iconSelectID].select_head
                        des.sprite.image = sprite.image

                #TEXT
                if des.type == "Text":
                    #Champions Names
                    if des.name == "Text_Name":
                        des.sprite.text = self.charSelect[self.charSelectID].name
                        
                    #Champions Description
                    if des.name == "Text_Des":
                        des.sprite.text = ""
                        des.sprite.text = self.charSelect[self.charSelectID].description

                    #Champions Variation Description
                    if des.name == "Text_Des_Var":
                        des.sprite.text = self.charSelect[self.charSelectID].variation_description[self.variationSelectID]
                    
                    #Give texts the correct BG name
                    if des.name == "Text_Base":
                        data = open(self.bgs[self.stageSelectID], "r")
                        f = data.read()
                        data = f.split('\n')
                        des.sprite.text = data[0].split(':')[1]
                    
    def Change(self, mb):
        stageID = ["Champion_Select", "Stage_Select", "Variation_Select"]
        if mb.name == "next" or mb.name == "prev" or mb.name == "right" or mb.name == "left":
            self.starter = False
        else:
            self.starter = True
            
        if mb.name == "Back":
            self.variationSelectID = 0
            if mb.next == "Main":
                self.charSelectID = 0
                self.stageSelectID = 0

        #Champion Select
        if mb.next == "Champion_Select":
            if mb.name == "next" and self.charSelectID < len(self.charSelect) -1:
                self.charSelectID += 1
            if mb.name == "prev" and self.charSelectID > 0:
                self.charSelectID -= 1    
            self.stage = mb.next + str(self.charSelectID)
            
        #Variation Select
        if mb.next == "Variation_Select":
            if mb.name == "next" and self.variationSelectID < len(self.charSelect[self.charSelectID].variation_images) -1:
                self.variationSelectID += 1
            if mb.name == "prev" and self.variationSelectID > 0:
                self.variationSelectID -= 1
            self.variation = self.charSelect[self.charSelectID].variation_images[self.variationSelectID]
            self.stage = mb.next + str(self.charSelectID)
            
        #Stage Select
        if mb.next == "Stage_Select":
            if mb.name == "next" and self.stageSelectID < len(self.bgs) -1:
                self.stageSelectID += 1
            if mb.name == "prev" and self.stageSelectID > 0:
                self.stageSelectID -= 1
            self.stage = mb.next + str(self.stageSelectID)

        if mb.next == "PlayerIcon":
            if mb.name == "right" and self.iconSelectID < len(self.charSelect) - 1:
                self.iconSelectID += 1
            if mb.name == "left" and self.iconSelectID > 0:
                self.iconSelectID -= 1
            
                
        if mb.next not in stageID:
            self.stage = mb.next
        self.update_all_menu_objects()
        self.update_menu_objects()
            

class MenuObject():
    def __init__(self, pos=(0,0), size=(1,1), name="MenuObject", stage="Main", type="Button", next="None", color=[0,0,0,255], first=False, font="Times New Romans"):
        self.pos = list(pos)
        self.first = first
        self.type = type
        self.name = name
        self.size = list(size)
        self.stage = stage
        self.color = color
        self.defualt = 200

        self.sprite = pyglet.sprite.Sprite(pyglet.image.load("UI/Select_Image.png"), x=self.pos[0], y=self.pos[1])
        self.sprite.opacity = color[3]
        
        #Graphics
        if self.type == "Button" or self.type == "Image":
            try:
                self.sprite = pyglet.sprite.Sprite(pyglet.image.load("UI/" +name+ ".png"), x=self.pos[0], y=self.pos[1])
                self.sprite.scale_x = float(self.size[0])
                self.sprite.scale_y = float(self.size[1])
                self.sprite.opacity = self.color[3]
                if self.type == "Button":
                    self.sprite.opacity = self.defualt
            except:
                self.sprite = pyglet.sprite.Sprite(pyglet.image.load("UI/UI_Base.png"), x=self.pos[0], y=self.pos[1])
                self.sprite.scale_x = float(self.size[0])
                self.sprite.scale_y = float(self.size[1])

        if self.type == "InputField":
            self.text = pyglet.text.Label(self.name, x=self.pos[0], y=self.pos[1], multiline=False, width=500)
            self.sprite = pyglet.sprite.Sprite(pyglet.image.load("UI/InputField.png"), x=self.pos[0], y=self.pos[1])
            self.sprite.font_size = self.size[0]
            self.holder = name
            self.textType = next
            self.active = False
            self.user_text = ""
            self.text.font_name = font
            
        if self.type == "Text":
            self.sprite = pyglet.text.Label(self.name, x=self.pos[0], y=self.pos[1], multiline=True, width=610)
            self.sprite.color = (self.color[0], self.color[1], self.color[2], self.color[3])
            self.sprite.font_size = self.size[0]
            self.sprite.font_name = font

        #Button Actions
        self.next = next

    def get_click(self):
        if self.type == "InputField":
            self.active = not self.active
            if self.active:
                self.text.text = self.user_text
                return self
            else:
                self.text.text = self.holder
                return None

    def IsHover(self, x, y):
        #If the hover type is a text: do nothing
        if self.type == "Text":
            return
        
        if x < self.pos[0] + self.sprite.width and x > self.pos[0] \
           and y < self.pos[1] + self.sprite.height and y > self.pos[1]:
            if self.type == "Button":
                self.sprite.opacity = 255
                self.sprite.color = [255,255,0]
        else:
            if self.type == "Button":
                self.sprite.opacity = self.defualt
                self.sprite.color = [200,200,200]
        
    def on_click(self, x, y):        
        if self.type == "Text":
            return
        if x < self.pos[0] + self.sprite.width and x > self.pos[0] \
           and y < self.pos[1] + self.sprite.height and y > self.pos[1]:
            return self.next


#Create Menus
menuManager = MenuManager()

f = open("UI/Menu/data.txt",'r')
data = f.read()
f.close()
data = data.split('\n')
menu = []
for row in data:
    menu.append(row)
    
for m in range(len(menu)):
    ignore = False
    #Position
    if menu[m].startswith("//"):
        ignore = True

    if ignore == False:
        pos = [int(menu[m].split(';')[0].split(':')[1].split(',')[0]), int(menu[m].split(';')[0].split(':')[1].split(',')[1])]
        size = [float(menu[m].split(';')[1].split(':')[1].split(',')[0]), float(menu[m].split(';')[1].split(':')[1].split(',')[1])]
        name = menu[m].split(';')[2].split(':')[1][1:]
        stage = menu[m].split(';')[3].split(':')[1][1:]
        type = menu[m].split(';')[4].split(':')[1][1:]
        next = menu[m].split(';')[5].split(':')[1][1:]

        #Color
        try:
            color = menu[m].split(';')[6].split(':')[1].split(',')
            if len(color) <= 3:
                color.append(255)
            for c in range(len(color)):
                color[c] = int(color[c])
        except:
            color = [255,255,255,255]
        
        #First
        try:
            first = menu[m].split(';')[7].split(':')[1][1:]
        except:
            first = False

        #Font_Type
        try:
            font = menu[m].split(';')[8].split(':')[1][1:]
        except:
            font = "Constantia"
            
                    
        menuManager.menu_objects.append(MenuObject(pos=pos, size=size, name=name, stage=stage, type=type, next=next, color=color, first=first, font=font))

menuManager.update_menu_objects()
#Check
##print(menuManager.menu_objects[-1].name)




















