import sys
import random
import cv2
import numpy as np
import pygame
import time



def main(): # メイン

    img_bg = [ 
        pygame.image.load("image/Fire 0.png"),
        pygame.image.load("image/Fire 1.png"),            
        pygame.image.load("image/Fire 2.png"),
        pygame.image.load("image/Fire 3.png"),
        pygame.image.load("image/Fire 4.png"),
        pygame.image.load("image/Fire 5.png"),
        pygame.image.load("image/Fire 6.png"),
        pygame.image.load("image/Fire 7.png"),
        pygame.image.load("image/Fire 8.png"),
        pygame.image.load("image/Fire 9.png"),
        pygame.image.load("image/Fire 10.png"),
        pygame.image.load("image/Fire 11.png"),
        pygame.image.load("image/Fire 12.png"),
        pygame.image.load("image/Fire 13.png"),
        pygame.image.load("image/Fire 14.png"),
        pygame.image.load("image/Fire 15.png"),
        pygame.image.load("image/Fire 16.png"),
        pygame.image.load("image/Fire 17.png"),
        pygame.image.load("image/Fire 18.png"),
        pygame.image.load("image/Fire 19.png"),
        pygame.image.load("image/Fire 20.png")            
    ]
            
            
    img_scn_bg0= pygame.image.load('image/karibg.png') 

    pygame.init()
    pygame.display.set_caption("Game watch Fire")

    scn_width = 1024 
    scn_height = 768
    
    screen = pygame.display.set_mode((scn_width, scn_height))
    scn =pygame.Surface((scn_width,scn_height),flags=pygame.SRCALPHA)
    
    #フォントの用意
    font1 = pygame.font.SysFont('meiryo', 40)   
    
    clock = pygame.time.Clock()

   
    pwidth = 1024
    pheight = 768      #画像表示サイズの変更

    counter = 0 
    pattern_MAX = 23
    char_ptn = [0,1,1,1,1,2,3,3,3,4,4,4,4,5,6,6,6,7,7,8,9,9,10,11,11]
    char_ang = [0,0,30,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    char_pos_x=[0,350,345,350,360,380,395,405,415,425,440,455,460,480,
                500,520,540,555,575,590,605,620,655,685,0,0]
    char_pos_y=[0,270,295,330,365,410,370,335,300,270,305,340,375,410,
                375,340,305,340,375,410,375,340,375,370,0,0]
    p_pos_x=[330,435,540]
    p_pos_y=[400,400,400]    
    #出現パターン
    ap_ptn = [
        "10000000100000001000000010000000",
        "01000001000000001000000100000000",
   #     "01000000000000000000000000000000",
   #     "00000000000000000000000000000000",
   #     "00000000000000000000000000000000",
   #     "00000000000000000000000000000000",
   #     "00000000000000000000000000000000",
   #     "00000000000000000000000000000000",
   #     "00000000000000000000000000000000",
   #     "00000000000000000000000000000000",
        "EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE"
        ]

    p_pos = 1    #ゲーム開始時のプレイヤーの位置
    b_key=None

    game_mode = 1    #仮　0=time_screen_mode  1=game_modeA   2=game modeB 
    score = 0
    char_locate = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    pt_cnt = 0
    cnt = 0
    ptn_cnt = 0
    cnt_speed = 10
    char_safe = [0,0,0]   
    char_dead = [0,0,0]       #charの落下フラグ　0=落下なし　1=rakka 


    #メインルーチン

    while True:
        if game_mode == 0:

            scn.fill((0,0,0,0)) 
            screen.blit(img_scn_bg0,[0,0])

            i = 0   
            while i < pattern_MAX:
                img = pygame.transform.rotozoom(img_bg[char_ptn[i]],char_ang[i],1.0)
                screen.blit(img,[char_pos_x[i],char_pos_y[i]]) 
                i += 1
           
            key = pygame.key.get_pressed()
            #title -> game_start
            if key[pygame.K_0] == 1 :
               game_mode =1
               score = 0
               char_locate = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
               pt_cnt = 0
               cnt = 0
               ptn_cnt = 0
               cnt_speed = 5
               char_safe = [0,0,0]   
               char_dead = [0,0,0]       #charの落下フラグ　0=落下なし　1=rakka               
            
        #ゲームモード通常
        if game_mode == 1:              
        
            scn.fill((0,0,0,0)) 
            screen.blit(img_scn_bg0,[0,0])
#           screen.blit(img_bg[0], [0,0])

            #for debug            
            text1 = font1.render("SCORE:"+str(score) + ":"+ str(cnt) +":"+ str(cnt_speed),
                     True, (0,0,0))
            screen.blit(text1, (0,0))



            #キャラクタの生成・移動
            cnt = cnt + 1
            if cnt%cnt_speed == 0 :           #charの移動スピード

                text1 = font1.render("●",True, (0,0,0))     #for debug
                screen.blit(text1, (0,50)) 
            
                ptn = ap_ptn[cnt//cnt_speed//32]
                pt_cnt = (pt_cnt +1)%32 
                                  
                if ptn[pt_cnt] == "1":
#                if cnt%cnt_phase == 0 :  #新規キャラクターの生成

                    char_locate[0] = 1                
                
                    text1 = font1.render("●",True, (255,0,0))     #for debug
                    screen.blit(text1, (0,200)) 
                    
                if ptn[pt_cnt] == "E":
                    game_mode = 0
                    cnt = 0
                    
  
                #キャラクターの移動
                i= pattern_MAX
                while i >= 0 :
                    if char_locate[i] == 1:
                        char_locate[i] = 0
                        
                        if i == pattern_MAX: 
                            score += 1    
                            screen.blit(text1, (0,300)) 
                    
                        elif i==5 and char_safe[0] ==0 :
                            char_dead[0]=1
                            game_mode = 2
                        elif i==13 and char_safe[1] ==0 :
                            char_dead[1]=1
                            game_mode = 2
                        elif i==19 and char_safe[2] ==0 :
                            char_dead[2]=1
                            game_mode = 2    
                            
                        else:
                            char_locate[i+1] = 1
                            
                    
                    i -= 1
                char_safe = [0,0,0]  

        #キャラクターの表示        
        i = 0   
        while i < pattern_MAX+1:
            if char_locate[i] == 1:
                img = pygame.transform.rotozoom(img_bg[char_ptn[i]],char_ang[i],1.0)
                screen.blit(img,[char_pos_x[i],char_pos_y[i]]) 
            i += 1

                    
        #ゲームモード(char dead)
        if game_mode == 2:
            
             game_mode = 1       


        scn.blit(img_bg[20],[p_pos_x[p_pos],p_pos_y[p_pos]])  #print_player
                    # 半透明のfillが有効
                    #scn.fill((255,255,255,10))
                    # ベースのsurfaceに貼り付け
        screen.blit(scn,(0,0)) 

        #自キャラの移動
        key = pygame.key.get_pressed()
        if b_key != key :
            b_key = key
            if key[pygame.K_1] == 1 and p_pos > 0:
                p_pos -= 1
            if key[pygame.K_3] == 1 and p_pos < 2:
                p_pos += 1
                
        #自キャラの当たり判定
        if p_pos == 0 and char_locate[5] == 1 and char_safe[0] == 0:
            char_safe[0] = 1
            #after pi sound add
        elif p_pos == 1 and char_locate[13] == 1 and char_safe[1] == 0:
            char_safe[1] = 1
            #after pi sound add
        elif p_pos == 2 and char_locate[19] == 1 and char_safe[2] == 0:
            char_safe[2] = 1
            #after pi sound add    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    screen = pygame.display.set_mode((pwidth, pheight), pygame.FULLSCREEN)
                if event.key == pygame.K_F2 or event.key == pygame.K_ESCAPE:
                    screen = pygame.display.set_mode((pwidth, pheight))
                if event.type == pygame.K_F3:
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()



