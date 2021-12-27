import pickle, pyglet

class StoryManager():
    def __init__(self):
        #Casual Variables
        self.timer = 0
        self.phase = 22
        self.ACT = 1
        self.scene = 1
        self.champions = []
        self.characters = []

        #Scene Variables
        self.bg = 0
        self.heads = ["UI/Story_Headshots/Ken_head.png", "UI/Story_Headshots/Ryu_head.png", "UI/Story_Headshots/Bison_head.png",
                      "UI/Story_Headshots/Cammy_head.png", "UI/Story_Headshots/Akuma_head.png", "UI/Story_Headshots/Akuma_head.png"]
        self.head = pyglet.sprite.Sprite(pyglet.image.load(self.heads[0]), x=15, y=424)
        self.targetDirection = None

        #Data
        # 0 - Ken, 1 - Ryu, 2 - M.Bison, 3 - Cammy, 4 - Akuma
        self.characterPositions = [[600,100], [-100,100], [1900,100], [1900,100], [-900,100], [-900,100], [-900, 100], [-900, 100]]

        #Tools
        self.canDraw = False
        self.currentPhase = 0
        self.camFocus = None
        self.chat = ""
        self.canPlayMusic = False
        self.music = "BGM/Story/stage1.mp3"
        self.champTalking = None
        self.mode = "Game"
        self.currentMode = "None"
        self.italic = False

        #Other UI
        self.speechBubble = None

        #Data: Label - [ Act:[ Scene:[ Phase:[] ] ] ]
        self.data = [ [], [], [] ]

        

    def SetPositions(self):
        for i in range(len(self.champions)):
            self.champions[i].isControlled = True
            self.champions[i].pos = self.characterPositions[i]
            self.champions[i].pos = self.characterPositions[i]
        self.targetDirection = self.champions[2]
        self.camFocus = self.champions[1]
        self.champs = [self.champions[1], self.champions[0]]

        #Load
##        self.LoadPositions()


    def Change_Head(self, id):
        self.head = pyglet.sprite.Sprite(pyglet.image.load(self.heads[id]), x=15, y=424)

    def Change_Head_With_File(self, file):
        self.head = pyglet.sprite.Sprite(pyglet.image.load(file), x=15, y=424)

    def update(self):
        self.timer -= .1

        if self.timer <= 0:
            self.NextScene()

    #Saving and loading all positions
    def SavePositions(self):
        data = []
        for i in range(len(self.champions)):
            data.append(self.champions[i].pos)
            
        self.data[self.ACT-1].append(data)
        pickle.dump(self.data, open("data/StoryData.txt", "wb"))
        print(self.data)

    def LoadPositions(self):
        data = pickle.load(open("data/StoryData.txt", "rb"))
        print(data[0])
        for i in range(len(self.champions)):
            try:
                self.champions[i].pos = data[0][i]
            except:
                print("'StoryData' list is longer than the 'champions' list")
    
    def NextScene(self):
        self.timer = 20
        self.phase += .5
        self.champTalking = None
        goOn = True

##        if len(self.data[self.ACT-1]) < self.phase:
##            self.SavePositions()
            
        if str(self.phase).endswith(".5"):
            self.canDraw = False
            self.timer = .3
        else:
            self.canDraw = True

        if self.ACT == 1:
            if self.scene == 1:
                #Phase 1
                if self.phase == 1:
                    self.canPlayMusic = True
                    self.canDraw = False
                    self.camFocus = self.champions[1]
                    self.camFocus.KeyDown("Right")
                    self.timer = 30

                #Phase 2
                if self.phase == 2:
                    self.camFocus.Attack_Punch("WP")
                    self.camFocus.KeyUp("Right")
                    self.currentPhase = self.phase
                    self.timer = 20
                    self.chat = "So you wanted to see me Ken?"
                    self.camFocus = self.champions[1]
                    self.targetDirection = self.champions[1]
                    
                #Phase 3
                if self.phase == 3:
                    self.currentPhase = self.phase
                    self.timer = 10
                    self.chat = "Yes"
                    self.camFocus = self.champions[0]
                    
                #Phase 4
                if self.phase == 4:
                    self.currentPhase = self.phase
                    self.timer = 20
                    self.chat = "I wanted to know if you were interested in a duel"
                    self.camFocus = self.champions[0]
                    
                #Phase 5
                if self.phase == 5:
                    self.currentPhase = self.phase
                    self.timer = 10
                    self.chat = "You know?"
                    self.camFocus = self.champions[0]
                    
                #Phase 6
                if self.phase == 6:
                    self.timer = 20
                    self.currentPhase = self.phase
                    self.chat = "For old time sake"
                    self.camFocus = self.champions[0]

                #Phase 7
                if self.phase == 7:
                    self.timer = 20
                    self.currentPhase = self.phase
                    self.chat = "I really don't have much 'interest' in a 1v1"
                    self.camFocus = self.champions[1]
                    self.camFocus.action = 1
                    
                #Phase 8
                if self.phase == 8:
                    self.timer = 20
                    self.currentPhase = self.phase
                    self.targetDirection = self.champions[1]
                    self.chat = "I'd prefer to save my energy for a fight unseen"
                    self.camFocus = self.champions[1]
                    
                    #Ryu Walks Away
                    self.camFocus.direction = -1
                    self.camFocus.KeyDown("Left")

                #Phase 9
                if self.phase == 9:
                    self.timer = 25
                    self.currentPhase = self.phase
                    self.targetDirection = self.champions[0]
                    self.chat = "Heh, typical Ryu, always expecting the unexpected..."
                    self.camFocus = self.champions[0]
                    self.camFocus.PlayVoice("Audio/Champs/Ken/Wins/Combos/combo4.wav")
                    self.champions[1].KeyUp("Left")
                    self.targetDirection = self.champions[0]

                #Phase 10
                if self.phase == 10:
                    self.currentPhase = self.phase
                    self.timer = 25
                    self.chat = "..and typical Ken, always oblivious to the unseen!"
                    self.camFocus = self.champions[1]

                #Phase 11
                if self.phase == 11:
                    self.currentPhase = self.phase
                    self.timer = 20
                    self.chat = "You've never think to take a break do you?"
                    self.camFocus = self.champions[0]
                    self.champions[0].KeyDown("Left")

                #Phase 12
                if self.phase == 12:
                    self.champions[0].KeyUp("Left")
                    self.currentPhase = self.phase
                    self.timer = 20
                    self.chat = " We're not exactly in a war right now."

                #Phase 13
                if self.phase == 13:
                    self.currentPhase = self.phase
                    self.timer = 8.5
                    self.camFocus.PlayVoice("Audio/popup.wav", .4)
                    self.speechBubble = pyglet.sprite.Sprite(pyglet.image.load_animation("sprites/speechless.gif"))
                    self.canDraw = False
                    self.camFocus = self.champions[1]

                #Phase 14
                if self.phase == 14:
                    self.currentPhase = self.phase
                    self.timer = 20
                    self.speechBubble = None
                    self.chat = "I get it ur always vigilant..."
                    self.camFocus = self.champions[0]

                #Phase 15
                if self.phase == 15:
                    self.currentPhase = self.phase
                    self.timer = 30
                    self.chat = "Heck, you might just be one of the most serious fighters in Dragon"
                    self.camFocus = self.champions[0]
                    self.champions[0].Attack_Punch("WP")

                #Phase 16
                if self.phase == 16:
                    self.currentPhase = self.phase
                    self.timer = 20
                    self.chat = "But every fighter needs his rest"
                    self.camFocus = self.champions[0]

                #Phase 17
                if self.phase == 17:
                    self.currentPhase = self.phase
                    self.timer = 20
                    self.canDraw = False
                    self.camFocus.PlayVoice("Audio/popup.wav", .4)
                    self.speechBubble = pyglet.sprite.Sprite(pyglet.image.load_animation("sprites/speechless.gif"))
                    self.camFocus = self.champions[1]

                #Phase 18
                if self.phase == 18:
                    self.currentPhase = self.phase
                    self.timer = 20
                    self.canDraw = False
                    self.speechBubble = None
                    self.camFocus = self.champions[1]

                #Phase 19
                if self.phase == 19:
                    self.currentPhase = self.phase
                    self.timer = 20
                    self.canDraw = False
                    self.camFocus.PlayVoice("Audio/050.wav", .2)
                    self.speechBubble = pyglet.sprite.Sprite(pyglet.image.load_animation("sprites/speechless.gif"))
                    self.camFocus = self.champions[0]

                #Phase 20
                if self.phase == 20:
                    self.currentPhase = self.phase
                    self.timer = 10
                    self.canDraw = False
                    self.speechBubble = None
                    self.camFocus = self.champions[1]
                    self.champions[1].Attack_Punch("MP")
                    self.camFocus.PlayVoice("Audio/Champs/Ryu/Dialogues/A.wav")

                #Phase 21
                if self.phase == 21:
                    self.currentPhase = self.phase
                    self.timer = 20
                    self.canDraw = True
                    self.camFocus = self.champions[1]
                    self.chat = "I'll only stay for a single match then I return to the gate"

                #Phase 22
                if self.phase == 22:
                    self.currentPhase = self.phase
                    self.timer = 20
                    self.canDraw = True
                    self.camFocus = self.champions[0]
                    self.chat = "Someon's finally listening. Let's do this"
                    self.champions[0].Attack_Punch("MP")
                    self.camFocus.PlayVoice("Audio/Champs/Ken/Dialogues/F.wav")

                if self.phase == 23:
                    self.currentMode = "Game"
                    self.canDraw = False
                    self.champions[0].pos[0] = 400
                    self.champions[1].pos[0] = 350
                    self.canPlayMusic = True
                    self.music = "BGM/02.mp3"
                    self.scene += 1
                    self.timer = 0
                    self.phase = 0

            if self.scene == 2:
                #Phase 1
                if self.phase == 1:
                    self.canDraw = False
                    self.camFocus = self.champions[1]
                    self.camFocus.Attack_Punch("WP")
                    self.timer = 1

                #Phase 2
                if self.phase == 2:
                    self.canDraw = False
                    self.camFocus = self.champions[1]
                    self.camFocus.Attack_Punch("WP")
                    self.timer = 1

                #Phase 3
                if self.phase == 3:
                    self.canDraw = False
                    self.camFocus = self.champions[1]
                    self.camFocus._skill("Hurricane Kick")
                    self.timer = 10

                #Phase 4
                if self.phase == 4:
                    self.canDraw = False
                    self.champions[1].KeyDown("Left")
                    self.timer = 3

                #Phase 5
                if self.phase == 5:
                    self.canDraw = False
                    self.camFocus = self.champions[0]
                    self.camFocus._skill("Hurricane Kick")
                    self.timer = 10

                #Phase 6
                if self.phase == 6:
                    self.champions[1].KeyUp("Left")
                    self.camFocus = self.champions[0]
                    self.chat = "Your speed is impressive as always"
                    self.timer = 10

                #Phase 7
                if self.phase == 7:
                    self.currentPhase = self.phase
                    self.camFocus = self.champions[1]
                    self.chat = "As is yours"
                    self.timer = 15

                #Phase 8
                if self.phase == 8:
                    self.currentPhase = self.phase
                    self.camFocus = self.champions[0]
                    self.chat = "I get the feeling you're supposed to say that"
                    self.timer = 10

                #Phase 9
                if self.phase == 9:
                    self.currentPhase = self.phase
                    self.camFocus = self.champions[1]
                    self.chat = "Only when I feel superior"
                    self.italic = True
                    self.timer = 10

                #Phase 10
                if self.phase == 10:
                    self.currentPhase = self.phase
                    self.camFocus = self.champions[1]
                    self.camFocus._skill("Super Hurricane Kick")
                    self.timer = 10
                    self.italic = False
                    self.canDraw = False

                #Phase 11
                if self.phase == 11:
                    self.currentPhase = self.phase
                    self.camFocus = self.champions[1]
                    self.camFocus._skill("Super Hurricane Kick")
                    self.timer = 10
                    self.italic = False
                    self.canDraw = False
                    


        if goOn and self.phase == self.currentPhase: 
            if self.camFocus != None:
                self.chat = self.camFocus.name + ": " + self.chat
                self.Change_Head_With_File("UI/Story_Headshots/" + self.camFocus.name + "_head.png")
                return
            
            if self.champTalking != None:
                self.chat = self.champTalking.name + ": " + self.chat
                self.Change_Head_With_File("UI/Story_Headshots/" + self.champTalking.name + "_head.png")

















        

storyManager = StoryManager()

