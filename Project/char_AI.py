import pyglet, random, math



class Human_AI():
    def __init__(self, name="Ryu", mode="Aggressive", champion=None, opponent=None):
        self.champion = champion
        self.opponent = opponent
        self.rangeEgo = 0
        self.abilityEgo = random.randint(5,10)
        self.ego = 0
        self.skillEgo = 30
        self.restCap = random.choice([40, 70])
        self.rest = self.restCap
        self.restTime = 0
        self.restTimer = 0

        #Avoid
        self.walkWait = 0
        self.jumpWait = 10
        self.jumpTime = 0
        self.crouchWait = 0
        self.crouchTime = 5
        self.jump = 0
        self.crouchWait = 5

        #States
        self.opponentInAir = False
        self.farRange = False
        self.midRange = False
        self.lowHealth = False
        self.healthAdvantage = False
        self.rageBarAdvantage = False
        self.defensive = False
        self.AIValues = open("data/AI/"+self.champion.name+".txt", "r")
        self.AIType = []

        #Checking for projectiles
        self.projectileCheck = 0
        self.projectileTime = 10
        
        for row in self.AIValues:
            self.AIType.append(row)
            
        #Actions
        #Remove the '\n' at the end of the skill
        self.closeRangeSkill = self.AIType[0].split(':')[1].split(',')
        self.closeRangeSkill[-1] = self.closeRangeSkill[-1][:-1]
        
        #Remove the '\n' at the end of the skill
        self.midRangeSkill = self.AIType[1].split(':')[1].split(',')
        self.midRangeSkill[-1] = self.midRangeSkill[-1][:-1]

        #Remove the '\n' at the end of the skill (split)
        self.farRangeSkill = self.AIType[2].split(':')[1].split(',')
        
        #Remove the '\n' at the end of the skill
        self.airborneSkill = self.AIType[3].split(':')[1].split(',')
        self.airborneSkill[-1] = self.airborneSkill[-1][:-1]
        
        #Remove the '\n' at the end of the skill
        self.defensiveSkill = self.AIType[4].split(':')[1].split(',')
        self.defensiveSkill[-1] = self.defensiveSkill[-1][:-1]
        
        

        #Kombat
        self.inRange = False
        self.punches = ["WP", "MP"]
        self.kicks = ["WK", "MK"]
        self.attackTime = random.choice([.7, .8, .9])
        self.attackTimer = 0

        
        #Suprise Super
        self.suprise = random.choice(["True", "False"])

    def Distance(self):
        dist = ((self.champion.pos[0] + self.champion.body[0]) - (self.opponent.pos[0] + self.opponent.body[0]))
        if dist < 0:
            dist = dist * -1
        return dist

    def CheckRange(self):
        self.opponentInAir = self.opponent.jump == True or self.opponent.fall == True
        self.farRange = self.Distance() >= 400
        self.midRange = self.Distance() >= 100 and self.Distance() < 400
        
    def Skill(self):
        self.CheckRange()
        mainAttack = random.choice(["W", "M"])
        choiceAttack = random.choice(["P", "K"])
        #If already performing a skill that might require input for a perfect combo
        #Then the AI should try one
        if self.champion.state == "Skill":
            if choiceAttack == "P":
                self.champion.hitPunch = "MP"
            if choiceAttack == "K":
                self.champion.hitKick = "MK"
                return
            
        #Check Ranges
        if self.rangeEgo >= self.abilityEgo:
            neutral = [0,1]
            if self.champion.direction == self.opponent.direction and self.champion.action not in neutral:
                self.rangeEgo -= 5
                self.champion.key_combo_time = 0
                self.champion.key_combo = ""
                return
            #If far range
            if self.farRange:
                self.champion.key_combo_time = 0
                if len(self.farRangeSkill) > 1:
                    self.champion.key_combo = random.choice(self.farRangeSkill)
                else:
                    self.champion.key_combo = self.farRangeSkill[0]
                self.rangeEgo = 0
                return
                
            #If mid range
            if self.midRange:
                if not self.opponentInAir:
                    self.champion.key_combo_time = 0
                    self.champion.key_combo = random.choice(self.midRangeSkill)
                    self.rangeEgo = 0
                    self.ego += 10
                if self.opponentInAir:
                    self.champion.key_combo_time = 0
                    self.champion.key_combo = random.choice(self.airborneSkill)
    
    def Movement(self):
        walk_states = [0, 1]
        self.champion.hitPunch = "MP"
        self.champion.hitKick = "MK"
##        attacking_actions = [2, 2.5, 3, 3.5, 9, 10, 10.5, 11, 11.5, 12, 17.3, 12.5, 12.8, 13, 13.5, 14, 14.5, 19, 19.1, 19.2, 21, 22]
        if self.champion.action in walk_states:
            if self.champion.state == "Grounded":
                if self.jumpTime >= 5:
                    choice = random.choice([0,1,2,3])
                    if choice == 0:
                        self.champion.KeyDown("Up")
                    self.jumpTime = -10
                else:
                    self.champion.KeyUp("Up")
                #Right
                if self.champion.body[0] + self.champion.body[2] < self.opponent.body[0]:
                    self.champion.KeyDown("Right")
                else:
                    self.champion.KeyUp("Right")
                    
                #Left
                if self.champion.body[0] > self.opponent.body[0] + self.opponent.body[2]:
                    self.champion.KeyDown("Left")
                else:
                    self.champion.KeyUp("Left")
        else:
            self.Reset()
                    
    def Attack(self):
        self.attackTimer -= .1
        if self.attackTimer <= 0:
            self.attackTimer = self.attackTime
            mainAttack = random.choice(["W", "M"])
            choiceAttack = random.choice(["P", "K"])

            #Skill for an epic combo
            if self.opponent.hitCombo > 2 and self.ego > 20:
                skillChoice = random.choice(self.closeRangeSkill)
                self.ego = 0

                if self.champion.direction != self.opponent.direction:
                    self.ego += 5
                    self.champion.key_combo_time = 0
                    self.champion.key_combo = skillChoice
                return
            
            if choiceAttack == "P":
                self.champion.Attack_Punch(mainAttack + choiceAttack)
            if choiceAttack == "K":
                self.champion.Attack_Kick(mainAttack + choiceAttack)

    #Back Away from opponent and even block possible attacks or projectiles
    def Avoid(self):
        if self.Distance() < 600:
            self.walkWait -= .5
            if self.walkWait <= 0:
                #Right
                if self.champion.body[0] < self.opponent.body[0]:
                    self.champion.KeyDown("Left")
                else:
                    self.champion.KeyUp("Left")
                    
                #Left
                if self.champion.body[0] > self.opponent.body[0]:
                    self.champion.KeyDown("Right")
                else:
                    self.champion.KeyUp("Right")
                    

                #Check for low attacks and not blocking actions
                blocks = [14, 14.5]
                if self.opponent.state == "Crouch":
                    self.champion.KeyDown("Down")
                else:
                    self.crouchWait -= .1
                    if self.crouchWait <= 0:
                        self.crouchWait = self.crouchTime
                        self.champion.KeyUp("Down")

            #If the opponent is not downed
            if self.opponent.action != 7.9:
                #If mid range
                if self.midRange and self.rangeEgo > self.abilityEgo:
                    if not self.opponentInAir:
                        self.champion.key_combo_time = 0
                        self.champion.key_combo = random.choice(self.defensiveSkill)
                        self.rangeEgo = self.abilityEgo - 10
                        self.ego += 10
                    if self.opponentInAir:
                        self.champion.key_combo_time = 0
                        self.champion.key_combo = random.choice(self.airborneSkill)

        else:
            self.Reset()
            self.walkWait = 5

    def Defend(self):
        for b in self.opponent.balls:
            dist = ((b.pos[0] + b.sprite.width) - (self.champion.pos[0] + self.champion.body[0]))
            if dist < 0:
                dist *= -1
            self.defensive = True
            attacking = [-1, -1.2, -1.5, 2, 2.5, 3, 3.5, 9, 10, 10.5, 11, 11.5, 12, 17, 17.3, 17.5, 12.5, 12.8, 13, 13.5, 14, 14.5, 19, 19.1, 19.2, 21, 22, 30, 30.2, 30.3]
            if dist < 500 or self.opponent.action in attacking:
                if self.champion.pos[0] < b.pos[0]:
                    self.champion.KeyDown("Left")
                if self.champion.pos[0] > b.pos[0]:
                    self.champion.KeyDown("Right")

    #AI playing aggressive
    def Aggressive(self):
        dodge_actions = [2, 2.5, 3, 3.5, 9, 10, 10.5, 11, 11.5, 12, 17.3, 12.5, 7] 
        if self.opponent.alive:
            self.rest -= .1
            self.Movement()
            self.Skill()
            if self.Distance() < 150 and self.champion.win == False:
                forget_states = [7.9]
                if self.opponent.action not in forget_states and self.champion.action not in dodge_actions:
                    self.Attack()
        else:
            self.Reset()
  

    def Reset(self):
        self.champion.KeyUp("Left")
        self.champion.KeyUp("Right")
        self.champion.KeyUp("Down")
        self.champion.KeyUp("Up")

        
    def Control(self):
        self.lowHealth = self.champion.health
        self.healthAdvantage = self.champion.health >= self.opponent.health
        self.rageBarAdvantage = self.champion.rageBar >= self.opponent.rageBar


        healthDiff = self.champion.health - self.opponent.health
        #Advanced AI
##        self.defensive = math.sqrt(math.pow(healthDiff, 2)) < 20

        #Block Projeciles when necessary
        self.Defend()
        if self.projectileCheck > self.projectileTime:
            self.Defend()
            if self.projectileCheck > self.projectileTime + 5:
                self.projectileCheck = 0
                self.defensive = False
            
        if self.healthAdvantage == False:
            self.rest -= .3
        
        if self.suprise == "True":
            self.suprise = "False"
            self.rangeEgo = self.abilityEgo
            self.Skill()
            
        self.ego += .4
        self.projectileCheck += .1
        self.rangeEgo += .1
        self.jumpTime += .1

        #Update Rest Time
        if self.rest <= 0:
            self.restTime -= .1
            if self.restTime <= 0:
                self.restTime = 20
                perc = (self.champion.health / self.champion.maxHealth) * 100
                #Stay safe if low on health
                if self.healthAdvantage == False and perc <= 50:
                    self.rest = self.restCap + 20
                else:
                    self.rest = self.restCap
        
                
        #Check Rest and Time 
        if self.rest > 0 and self.champion.pause == False and self.defensive == False:
            #Engage only if alive
            if self.champion.action == 0 or self.champion.action == 1:
                self.Aggressive()
        if self.rest <= 0 or self.opponent.action == 7.9:
            self.Avoid()

        if self.opponent.alive == False:
            self.Reset()
            







