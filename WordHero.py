import pygame
import random
from PyDictionary import PyDictionary
import enchant
import sys

#dictionary=PyDictionary()

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
GREEN = (0, 255, 0)
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
        self.outline_color = BLACK
        #self.action = False
        
    def draw(self, text_color, scale):
        action = False
        pos = pygame.mouse.get_pos()
                
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), scale)
        pygame.draw.rect(screen, self.outline_color, (self.x, self.y, self.width, self.height), 1)
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
            #action = False
        
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
shuffle_button = Button('Shuffle', GREEN,675,610,100,100)
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
m1 = Monster(50,20)




# Game loop
game_state = "menu"
turn = "player"
print(stack)
n = []
h = 0
ok = []
no = 0
x = 1
clear = False
running = True
while running:
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Check for left mouse button click
                for button in table:
                    action = button.draw(BLACK, 0)
                    pygame.time.wait(10)
                    if action:
                        h += 1
                        #print('Clicked on:', button.text)    
                        k = Button(button.text, GRAY, h *60, 100 , table_width, table_height)
                        n.append((k,button.x,button.y))
                        #print('x',((button.x-420)/60))
                        #print('y',((button.y-480)/60))
                        stack.remove(button.text)
                        table.remove(button)
                        words.append(button.text)
                        #print(stack)
                        #print(words)
                        atk += button.text
                        #print(atk)
                        #turn = "monster"  # Switch to monster turn after player's turn
                        #print(n)
                        #print(len(n))
                for g in n:
                    actions = g[0].draw(BLACK, 0)
                    if actions:
                        pygame.time.wait(10)
                        if g[0].text == '':
                            #print('nothing')
                            continue
                        g[0].color_clicked = background_color
                        kuy = Button(g[0].text, WHITE, g[1], g[2], table_height, table_height)
                        table.append(kuy)
                        stack.append(g[0].text)
                        words.remove(g[0].text)
                        #print('s',stack)
                        #print('w',words)
                        h-=1
                        atk = atk[:-1]
                        #print('atk:',atk)
                        #print(g[1])
                        #print(g[2])
                        n.remove(g)
                        #print('a',len(n))
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
        
        #hoo = 0
        #for i in words:
            #Button(i, GRAY, hoo*60, 50,60,60).draw(BLACK,0)
            #hoo +=1 
            
            
        if turn == "player":
            #attack_button.clicked = False
            shuffle_button.clicked = False
            #print('HAI')
            #print(len(atk))
            if attack_button.draw(BLACK,0) and len(atk) >= 3:
                pygame.time.wait(100)
                if us.check(atk):
                    p1.Attack(m1)
                    m1.showHp(800,25)
                    m1.Attack(p1)
                    p1.showHp(10,25)
                    words=[]
                    dictionary=PyDictionary(atk)
                    o = dictionary.meaning(atk)
                    print(o['Noun'][0])
                    atk = ""
                #print(m1.hp)
                if m1.hp <= 0:
                    x = x + 1
                    p1.hp = p1.maxhp
                    m1 = Monster(25+(x*25),10+(x*10))
                h=0   
                clear = True
                
                for button in n:
                    #n.remove(button)
                    button[0].color = background_color
                    button[0].color_clicked = background_color
                    button[0].outline_color = background_color
                    button[0].text = ''
                    button[0].draw(background_color,0)
                    
                    #แก้ตรงนี้หน่อยยยยโว้ยยยยย รันโค้ดเด่วเข้าใจเองแหละสู้วๆๆ เหมือนจะได้นะแต่แค่เหมือนน
                    # stack มันสุ่มทะลุแบบ สุ่มเกินให้เหี้ยมี 16 ช่องพอมุงกดใช้ไป 4 ช่องแล้วกดปุ่มตี มันสุ่มลงในช่องกะจิง
                    # stack แต่มันสุ่มให้มึงเพิ่มอีกควย ฝากทีนะเพื่อนๆๆๆ
                    letter = random.choice(list(c.keys()))
                    nahee = Button(letter,WHITE,button[1], button[2], table_width, table_height)
                    table.append(nahee)
                    stack.append(letter)  
                n=[]
            #else:
                #attack_button.clicked = False
                #print('b',len(n))    
                #print(stack)
                #print(words)
                #print(atk)
                #print(clear)
            if shuffle_button.draw(BLACK,0) and len(words) == 0:
                pygame.time.wait(100)
                table = []
                stack = []
                for i in range(4):
                    for j in range(4):
                        letter = random.choice(list(c.keys()))
                        button = Button(letter, WHITE, j * table_width + 420, i * table_height + 480, table_width, table_height)
                        table.append(button)
                        stack.append(letter)

                m1.Attack(p1)
                p1.showHp(10,25)
                
        #TABLE        
        for button in table:
            button.draw(BLACK, 0)
        
        
        
        for but in n:
            but[0].draw(BLACK,0)
            #n.remove(but)
        #pygame.draw.rect(screen, background_color,(x[1],x[2],60,60))
            
        #for bda in ok:
            #bda.draw(BLACK, 0)
        
        
        #BG_TABLE
        for i in range(4):
            for j in range(4):
                pygame.draw.rect(screen, BLACK, (j * table_width + 420, i * table_height + 480, table_width, table_height), 1)    
                
        
    pygame.display.flip()
    timer.tick(fps)

# Quit the game
pygame.quit()

sys.exit()

