import pygame
import threading
import time


#變數
Px = 0
Py = 0
WIDTH = 960
HEIGHT = 540
SPEED = 2
score = 0
score_text = 'score:' + str(score)
tile_size = 10
cols = 0
rows = 0
MAP_DATA = [[0 for _ in range(96)] for _ in range(54)]
mapdata = []
walls = []
bings = []

#顏色
YELLOW = (255, 255, 0)
BLACK = (0,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)

#遊戲初始化 和 創建視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('吃豆人')
FPS = 60
clock = pygame.time.Clock()
running = True

#讀取圖片
BING = pygame.image.load('bing.png') 
BING = pygame.transform.scale(BING, (tile_size, tile_size))
P1 = pygame.image.load('player1.png') 
P1 = pygame.transform.scale(P1, (30, 30))
P2 = pygame.image.load('player2.png') 
P2 = pygame.transform.scale(P2, (30, 30))
E1 = pygame.image.load('enemy1.png') 
E1 = pygame.transform.scale(E1, (30, 30))
E2 = pygame.image.load('enemy2.png') 
E2 = pygame.transform.scale(E2, (30, 30))
E3 = pygame.image.load('enemy3.png') 
E3 = pygame.transform.scale(E3, (30, 30))
E4 = pygame.image.load('enemy4.png') 
E4 = pygame.transform.scale(E4, (30, 30))
present_image2 = P2
present_image1 = P1




#讀取地圖
F = open('mapdata.txt','r')
maprawdata = F.read()
for i in range(len(maprawdata)):
     if maprawdata[i] == '0':
         mapdata.append(0)
     elif maprawdata[i] == '1':
         mapdata.append(1)
     elif maprawdata[i] == '2':
         mapdata.append(2)
     else :
         continue
for i in range(len(mapdata)):
     MAP_DATA[rows][cols] = mapdata[i]
     cols += 1
     if cols == 96:
         rows += 1
         cols = 0
for y in range(len(MAP_DATA)):
         for x in range(len(MAP_DATA[0])):
             if MAP_DATA[y][x] == 0:
                 pygame.draw.rect(screen,BLACK,(x * tile_size, y * tile_size, tile_size, tile_size))
             elif MAP_DATA[y][x] == 1:
                pygame.draw.rect(screen,BLUE,(x * tile_size, y * tile_size, tile_size, tile_size))
                wall_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                walls.append(wall_rect)
             else:
                 screen.blit(BING, (x * tile_size, y * tile_size))
                 bing_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                 bings.append(bing_rect)

     
 #分數
def show_score():
    score_text = 'score:' + str(score)
    #文字渲染
    font = pygame.font.Font(None, 25)
    score_surface = font.render(score_text, False, WHITE)
        
    #文字位置
    score_rect = score_surface.get_rect()
    score_rect.x = 0
    score_rect.y = 0
    screen.blit(score_surface, score_rect)
           

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = P2
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        



    def update(self):
        global Px, Py, WIDTH, HEIGHT, score, present_image2, present_image1
        
        #取得嘗試移動前座標
        PXb = self.rect.x
        PYb = self.rect.y
                
        #移動
        self.rect.x += Px
        self.rect.y += Py
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w]:
            Py = -SPEED
            Px = 0
            present_image2 = pygame.transform.rotate(P2,90)
            present_image1 = pygame.transform.rotate(P1,90)
        if key_pressed[pygame.K_s]:
            Py = SPEED
            Px = 0
            present_image2 = pygame.transform.rotate(P2,270)
            present_image1 = pygame.transform.rotate(P1,270)
        if key_pressed[pygame.K_a]:
            Px = -SPEED
            Py = 0
            present_image2 = pygame.transform.rotate(P2,180)
            present_image1 = pygame.transform.rotate(P1,180)
        if key_pressed[pygame.K_d]:
            Px = SPEED
            Py = 0
            present_image2 = P2
            present_image1 = P1
              
        #牆壁
        player_rect = pygame.Rect(self.rect.x, self.rect.y, 30, 30)
        player_rect = pygame.Rect(self.rect.x, self.rect.y, 30, 30)
        for wall_rect in walls:
            if player_rect.colliderect(wall_rect):
                self.rect.x = PXb
                self.rect.y = PYb
                
        #邊界
        self.rect.x = min(self.rect.x, WIDTH-30)
        self.rect.x = max(0, self.rect.x)
        self.rect.y = min(self.rect.y, HEIGHT-30)
        self.rect.y = max(0, self.rect.y)
        
        #豆子
        for bing_rect in bings:
            if player_rect.colliderect(bing_rect):
                pygame.draw.rect(screen, (BLACK), bing_rect)
                score += 1
                bings.remove(bing_rect)
               
         
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        
        
enemies = [Enemy(510, 430, E1), Enemy(540, 430, E2), Enemy(570, 430, E3), Enemy(600, 430, E4)]

#切換玩家圖片
def change_picture():
    global present_image2, present_image1
    while running:
        for i in range(0,4):
            player.image = present_image1
            time.sleep(0.05)
        for i in range(0,4):
            player.image = present_image2
            time.sleep(0.05)


#分組
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for enemy in enemies:
    all_sprites.add(enemy)

#多線程
change_picture_thread = threading.Thread(target = change_picture)
change_picture_thread.start() 

#遊戲迴圈
while running:
    clock.tick(FPS)

     #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    
#更新遊戲
    all_sprites.update()

#畫面顯示
    pygame.draw.rect(screen, BLACK, pygame.Rect(50, 0, 30, 20))
    all_sprites.draw(screen)
    
#分數顯示
    show_score()
    
    pygame.display.update()

pygame.quit()