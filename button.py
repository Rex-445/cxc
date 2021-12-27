
class Button:
    def __init__(self, pos=(0,0), wrd="Defualt", width=(60,20), mode="Menu", isActive=True, itr=False):
        self.pos = list(pos)
        self.color = (0,10,50)
        self.word = wrd
        self.width = width
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width[0], self.width[1])
        self.selected = False
        self.mode = [mode]
        self.active = isActive
        self.itr = itr
        self.title = "Duel"
        self.words = ["An Epic One versus One between two fighters each having", "unique skills. Every Victory grants a point, '2' points",
                      "for the win. Either fighter with the highest point is ", "declared the Winner."]

    def Update(self, screen, mouse):
        if self.selected == True:
            self.rect.x = mouse[0] -self.rect.width/2
            self.rect.y = mouse[1] -self.rect.height/2
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (255,0,0), self.rect, 1)
        text = pygame.font.Font(None, 20).render(self.word, True, (225,225,225), (self.color))
        screen.blit(text, (self.rect.x + 5, self.rect.y + self.rect.height / 2 - 7))
        
    def IsHover(self):
        mouse = pygame.mouse.get_pos()
        if mouse[0] > self.rect.x and mouse[0] < self.rect.x + self.rect.width:
            if mouse[1] > self.rect.y and mouse[1] < self.rect.y + self.rect.height:
                return True
        else:
            return False
