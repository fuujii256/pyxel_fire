import sys
import random
import cv2
import numpy as np
import time

import pyxel

        
pattern_MAX = 24
char_ptn = [0,0,1,1,1,1,2,3,3,3,4,4,4,4,5,6,6,6,7,7,8,9,9,10,11,11]
char_ang = [0,0,30,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#char_pos_x=[0,88,86,88,90,95,99,101,104,106,110,111,115,120,
#        125,130,135,139,143,148,151,155,164,171,0,0]
#char_pos_y=[0,68,74,83,91,103,93,84,75,68,76,85,94,103,
#        94,85,76,85,94,103,94,85,94,93,0,0]
char_pos_x=[0,40,43,45,50,60,68,73,78,83,90,98,100,110,
                120,130,140,148,158,165,173,180,198,213,0,0]
char_pos_y=[0,70,83,100,118,140,120,105,85,70,88,105,123,140,
                123,105,88,105,123,140,123,105,123,120,0,0]
p_pos_x=[27,85,143]
p_pos_y=[138,138,138]    
#出現パターン
ap_ptn = [
    "11010101000000010000000100000000",
    "01000001000000001000000100000000",
    "01000000000001000000000010100000",
    "01000000100000000010000000000000",
    "EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE"
]
#     "00000000000000000000000000000000",
#     "00000000000000000000000000000000",
#     "00000000000000000000000000000000",
#     "00000000000000000000000000000000",
#     "00000000000000000000000000000000",
#     "00000000000000000000000000000000",



p_pos = 1    #ゲーム開始時のプレイヤーの位置
b_key=None

game_mode = 1    #仮　0=time_screen_mode  1=game_modeA   2=game modeB 
score = 0
char_locate = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
pt_cnt = 0
cnt = 0
ptn_cnt = 0
cnt_speed = 10
char_safe = [0,0,0]   
char_dead = [0,0,0]       #charの落下フラグ　0=落下なし　1=rakka 

         

class app:

    def __init__(self):
        pyxel.init(255, 255, 
                   title="blue_arc_fire",
                   fps = 24,
                   quit_key =0,
                   display_scale = 3)     
        #pyxel.load('image/my_resource.pyxres')
        #pyxel.image(1).load(0,0,"image/karibg2.png")     
        pyxel.image(0).load(0,0,"image/char_sp16_4.png")
                #pyxel.image(0).load(0,0,"image/char_sp32_3.png")              
        pyxel.image(2).load(0,0,"image/fire 0.png")  
        pyxel.run(self.update, self.draw)

    def update(self):
        global game_mode,score,p_pos,cnt,cnt_speed,pt_cnt,char_locate,char_dead,char_safe
        
        #自キャラの移動
        key1 = 0
        key3 = 0
        
        if pyxel.btnr(pyxel.KEY_1) :
            key1 = 0
        if pyxel.btnr(pyxel.KEY_3) :
            key3 = 0     

        if  pyxel.btnp(pyxel.KEY_1) == 1 and key1 == 0 :
            if p_pos > 0:
                p_pos -= 1
        if  pyxel.btnp(pyxel.KEY_3) == 1 and key3 == 0 :
            if p_pos < 2: 
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


        if game_mode == 0:
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
           
            #title -> game_start
            if pyxel.btnp(pyxel.KEY_0) == 1 :
               game_mode =1         #ゲームスタート
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
        
            #キャラクタの生成・移動
            cnt = cnt + 1
            if cnt%cnt_speed == 0 :           #charの移動スピード          
            
                ptn = ap_ptn[cnt//cnt_speed//32]
                pt_cnt = (pt_cnt +1)%32 
                                  
                temp = ptn[pt_cnt]
                if ptn[pt_cnt] == "1":
#                if cnt%cnt_phase == 0 :  #新規キャラクターの生成

                    char_locate[0] = 1                
                    
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



        #ゲームモード(char dead)
        if game_mode == 2:
            
             game_mode = 1 

    def draw(self):
        global gamemode,p_pos,p_pos_x,p_pos_y,char_locate
        
       
        pyxel.cls(0)
        
        pyxel.blt(0, 0, 1, 0, 0, 256, 212)
        pyxel.blt(8, 41, 2, 0, 0, 256, 212,0)   

        #プレイヤーの表示  
        pyxel.blt( p_pos_x[p_pos],p_pos_y[p_pos],0,0,16,64,32,0)

        if game_mode == 0:
        
        #キャラの表示
            i = 1   
            while i < pattern_MAX:
                pyxel.blt( char_pos_x[i],char_pos_y[i],0,char_ptn[i]*16,0,16,16,1 ) 
                i += 1


        if game_mode == 1:

        #キャラの表示
            i = 1   
            while i < pattern_MAX:
                if char_locate[i] == 1:
                    pyxel.blt( char_pos_x[i],char_pos_y[i],0,char_ptn[i]*16,0,16,16,0 ) 
                i += 1

            



app()