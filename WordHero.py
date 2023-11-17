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
        text = font.render(self.text, True, text_color)
        text_rect = text.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(text, text_rect)
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if self.clicked:
            pygame.draw.rect(screen, self.color_clicked, (self.x, self.y, self.width, self.height), scale)
            

        return action


letter_values = {
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
table_button = []
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
        letter = random.choice(list(letter_values.keys()))
        button = Button(letter, WHITE, j * table_width + 420, i * table_height + 480, table_width, table_height)
        table_button.append(button)
        stack.append(letter)




class Charecter:
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
        text = font.render(hp_text, True, BLACK)
        screen.blit(text, (self.posx_text, self.posy_text))


    def Attack(self, Target):
        Target.hp -= self.Damage

    def show_info(self):
        RD_rect = pygame.Rect(800, 480, 280, 240)
        pygame.draw.rect(screen, (124, 0, 0), RD_rect)
        dmg_text = str(self.Damage)
        name_text = "enemy name"
        enemy_name = font.render(name_text,True,(0,0,0))
        dmg = font.render(dmg_text,True,(0,0,0))
        screen.blit(enemy_name,(850,500))
        screen.blit(dmg,(940,600))
    
    def show_meaning(self):
        font20 = pygame.font.Font(None, 20)
        LD_rect = pygame.Rect(0, 480, 420, 240)
        pygame.draw.rect(screen, (124, 0, 0), LD_rect)
        word_text = "word"
        text_noun = "noun meaning p p p p p p pppppppppppppp pp p p p p p p p p p p p p p p p p"
        text_verb = "verb meaning very very long long very very long long very very long long very very long long very very long long very very long long very very long long very very long long "
        rendered_word_text = font.render(word_text, True, (0, 0, 0))
        screen.blit(rendered_word_text,(20,500))
        draw_wrapped_text(text_noun, font20, (0,0,0), screen, 5, 560, 410)
        draw_wrapped_text(text_verb, font20, (0,0,0), screen, 5, 620, 410)


def draw_wrapped_text(text, font, color, surface, x, y, max_width):
    words = [word.split(' ') for word in text.splitlines()]  # แบ่งข้อความเป็นคำ
    space = font.size(' ')[0]  # ขนาดของช่องว่างระหว่างคำ

    x_pos, y_pos = x, y
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()

            if x_pos + word_width >= x + max_width:
                    x_pos = x  # ย้ายไปที่จุดเริ่มต้นของบรรทัดถัดไป
                    y_pos += word_height  # ขึ้นบรรทัดใหม่

            surface.blit(word_surface, (x_pos, y_pos))
            x_pos += word_width + space
        x_pos = x
        y_pos += word_height






#Player
p1 = Charecter(100,20)
m1 = Charecter(50,20)




# Game loop
game_state = "menu"
turn = "player"
#print(stack)
stack_button = []
clicked_times = 0

running = True
while running:
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Check for left mouse button click
                
                #Click in table
                for button in table_button:
                    draw_button_inTable = button.draw(BLACK, 0)
                    pygame.time.wait(10)
                    #Clicked
                    if draw_button_inTable:
                        clicked_times += 1
                        stack.remove(button.text)
                        table_button.remove(button)
                        words.append(button.text)
                        create_button_onstack = Button(button.text, GRAY, clicked_times *60, 100 , table_width, table_height)
                        stack_button.append((create_button_onstack,button.x,button.y,clicked_times))
                        atk += button.text
                        
                for pos,button in enumerate(stack_button):
                    draw_button_inStack = button[0].draw(BLACK, 0)
                    if draw_button_inStack:
                        pygame.time.wait(10)
                        
                        button[0].color_clicked = background_color
                        
                        if button[0].text == '':
                            continue
                        
                        if button[3] <= len(stack_button):
                            for i in range(button[3]-1,len(stack_button)):
                                stack.append(words[pos])
                                create_button_intable = Button(words[pos], WHITE, stack_button[pos][1],stack_button[pos][2], table_height, table_height)
                                table_button.append(create_button_intable)
                                del words[pos]
                                del stack_button[pos]       
                                atk = atk[:-1]
                                clicked_times-=1
    
    #SET BACKGROUND
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
        m1.show_info()
        m1.show_meaning()
        p1.Load_Skin(100,200)
        p1.showHp(10,25)
        m1.Load_Skin(800,200)
        m1.showHp(800,25)
        
            
        if turn == "player":
            attack_button.clicked = False
            shuffle_button.clicked = False
            
            if attack_button.draw(BLACK,0) and len(atk) >= 3:
                pygame.time.wait(100)
        
                if us.check(atk):
                    p1.Attack(m1)
                    m1.showHp(800,25)
                    m1.Attack(p1)
                    p1.showHp(10,25)

                    words=[]
                    #dictionary=PyDictionary(atk)
                    #o = dictionary.meaning(atk)
                    #print(o['Noun'][0])
                    atk = ''
                    
                    for button in stack_button:
                        button[0].color = background_color
                        button[0].color_clicked = background_color
                        button[0].outline_color = background_color
                        button[0].text = ''
                        
                        letter = random.choice(list(letter_values.keys()))
                        randomly_button = Button(letter,WHITE,button[1], button[2], table_width, table_height)
                        table_button.append(randomly_button)
                        stack.append(letter)  
                else:
                    for button in stack_button:
                        button[0].color = background_color
                        button[0].color_clicked = background_color
                        button[0].outline_color = background_color
                        create_button_intable = Button(button[0].text, WHITE, button[1],button[2], table_height, table_height)
                        table_button.append(create_button_intable)
                        stack.append(button[0].text)
                    words = []
                    stack_button=[]
        
                if m1.hp <= 0:
                    x = x + 1
                    p1.hp = p1.maxhp
                    m1 = Charecter(25+(x*25),10+(x*10))
                    
                clicked_times = 0   
                stack_button=[]
           
            if shuffle_button.draw(BLACK,0) and len(words) == 0:
                pygame.time.wait(100)
                table_button = []
                stack = []
                for i in range(4):
                    for j in range(4):
                        letter = random.choice(list(letter_values.keys()))
                        button = Button(letter, WHITE, j * table_width + 420, i * table_height + 480, table_width, table_height)
                        table_button.append(button)
                        stack.append(letter)

                m1.Attack(p1)
                p1.showHp(10,25)
                
        #TABLE        
        for button in table_button:
            button.draw(BLACK, 0)
        
        
        
        for button in stack_button:
            button[0].draw(BLACK,0)
        
        
        #BG_TABLE
        for i in range(4):
            for j in range(4):
                pygame.draw.rect(screen, BLACK, (j * table_width + 420, i * table_height + 480, table_width, table_height), 1)    
                
        
    pygame.display.flip()
    timer.tick(fps)

# Quit the game
pygame.quit()

sys.exit()
