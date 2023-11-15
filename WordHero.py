import pygame
import random
from PyDictionary import PyDictionary
import enchant
import sys

dictionary=PyDictionary()

# Initialize the pygame library
pygame.init()


screen_width = 1080
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("WordHero")


# Colors
background_color = (135, 206, 235)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (169,169,169)
# FPS and timer
fps = 60
timer = pygame.time.Clock()

# Font
font = pygame.font.Font(None, 42)

#LANGUAGE
us = enchant.Dict('en_US')
#UI
# Define Button class
class Button:
    def __init__(self, text, color, x, y, width, height):
        self.text = text
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.clicked = False
        self.color_clicked = GRAY
        #self.action = False
        
    def draw(self, text_color, scale):
        action = False
        pos = pygame.mouse.get_pos()
                
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), scale)
        img = font.render(self.text, True, text_color)
        img_rect = img.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(img, img_rect)
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                #print('clicked')
                self.clicked = True
                #self.action = True
                action = True
        if self.clicked:
            pygame.draw.rect(screen, self.color_clicked, (self.x, self.y, self.width, self.height), scale)
            #self.clicked = False
        #else:
            #self.clicked = True
        
        #return action
        return action

table = []
c = {
    'A':1,'E':1,'I':1,'O':1,'U':1,'L':1,'N':1,'S':1,'T':1,'R':1,
    'D':2,'G':2,
    'B':3,'C':3,'M':3,'P':3,
    'F':4,'H':4,'V':4,'W':4,'Y':4,
    'K':5,
    'J':8,'X':8,
    'Q':10,'Z':10
    }

stack = []
words = []
atk = ''

#CREATE EACH BUTTON!!!
button_width = 200
button_height = 60
play_button = Button('PLAY', RED, (screen_width - button_width) // 2, (screen_height - button_height) // 2, button_width, button_height)
exit_button = Button('EXIT', RED, (screen_width - button_width) // 2, (screen_height - button_height) // 2 + 100, button_width, button_height)
attack_button = Button('Attack', RED,675,495,100,100)
#CREATE EACH BUTTON IN TABLE!!!
table_width = 60
table_height = 60
for i in range(4):
    for j in range(4):
        letter = random.choice(list(c.keys()))
        button = Button(letter, WHITE, j * table_width + 420, i * table_height + 480, table_width, table_height)
        table.append(button)
        stack.append(letter)
        
class Player:
    def __init__(self, maxhp, dmg):
        self.maxhp = maxhp
        self.Damage = dmg
        self.hp = maxhp
    def Load_Skin(self, x, y):
        self.x_load = x
        self.y_load = y
        pygame.draw.rect(screen, (255,0,255), (self.x_load, self.y_load, 100, 150))

    def showHp(self,x,y):
        self.posx_text = x
        self.posy_text = y
        hp_text = f"HP: {self.hp}/{self.maxhp}"
        img = font.render(hp_text, True, BLACK)
        screen.blit(img, (self.posx_text, self.posy_text))

    def Create_table(self):
        pass



    def Attack(self, Target):
        Target.hp -= self.Damage


class Monster(Player):
    pass


#Player
p1 = Player(100,20)
m1 = Monster(50,25)




# Game loop
game_state = "menu"
turn = "player"
print(stack)
n = []
h = 0
ok = []
no = 0
running = True
while running:
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Check for left mouse button click
                for button in table:
                    action = button.draw(BLACK, 0)
                    if action:
                        h += 1
                        print('Clicked on:', button.text)    
                        k = Button(button.text, GRAY, h *60, 100 , table_width, table_height)
                        n.append(k)
                        print('x',((button.x-420)/60))
                        print('y',((button.y-480)/60))
                        stack.remove(button.text)
                        words.append(button.text)
                        print(stack)
                        print(words)
                        atk += button.text
                        print(atk)
                        #turn = "monster"  # Switch to monster turn after player's turn
                for button in n:
                    actions = button.draw(BLACK, 0)
                    if actions:
                        button.color_clicked = background_color
                        no += 1
                        kuy = Button(button.text, GRAY, no*100, 400,table_height, table_height) 
                        ok.append(kuy)
    screen.fill(background_color)
    
    if game_state == 'menu':
        if play_button.draw(WHITE,0):
            #print('PLAY')
            game_state = 'play'
        if exit_button.draw(WHITE,0):
            #print('BYE')
            running = False
            
    elif game_state == 'play':
        screen.fill(BLACK)
        #This for playing
        screen.fill(background_color)
        pygame.draw.rect(screen, GRAY, (0, 480, 1080, 300))
        p1.Load_Skin(100,200)
        p1.showHp(10,25)
        m1.Load_Skin(800,200)
        m1.showHp(800,25)
        
        for but in n:
            but.draw(BLACK,0)
        
        for bda in ok:
            bda.draw(BLACK, 0)
            
        if turn == "player":
            attack_button.clicked = False
            #print(len(atk))
            if attack_button.draw(BLACK,0) and len(atk) >= 3:
                if us.check(atk):
                    p1.Attack(m1)
                    m1.showHp(800,25)
                    m1.Attack(p1)
                    p1.showHp(10,25)
                    dictionary=PyDictionary(atk)
                    o = dictionary.meaning(atk)
                    print(o['Noun'][0])
                    atk = ""
        #TABLE        
        for button in table:
            button.draw(BLACK, 0)
        
        #BG_TABLE
        for i in range(4):
            for j in range(4):
                pygame.draw.rect(screen, BLACK, (j * table_width + 420, i * table_height + 480, table_width, table_height), 1)    
                
        
    pygame.display.flip()
    timer.tick(fps)

# Quit the game
pygame.quit()

sys.exit()

