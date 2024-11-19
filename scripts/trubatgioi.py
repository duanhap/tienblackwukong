import math
import random

import pygame

from scripts.particle import Particle
from scripts.spark import Spark
from scripts.entities import PhysicsEntity
from scripts.loithoai import Loithoai
class TruBatGioi(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'trubatgioi', pos, size)
        self.attacking = False
        self.walking = 0
        self.air_time=0
        self.dan=''
        self.ditheognguoichoi = True
        self.xuathienkhunghinhmap2=0
        self.loithoai =  Loithoai(self.game,'batgioi')
        self.targets = [] 
        self.hp=5
        self.hp_max=5
        self.dead= False
        
    def update(self, tilemap, movement=(0, 0)):
        #print(f'{self.hp}  dead chua {self.dead}'  )
        if self.game.level == 3 :
            self.xuathienkhunghinhmap2 =1000
        else:
            self.xuathienkhunghinhmap2+=1
        if self.xuathienkhunghinhmap2 <700 and self.xuathienkhunghinhmap2 >100:
            self.game.capnhatvitriplayer = False
            self.game.scroll[0]+=(self.rect().centerx-self.game.screen.get_width()/2-self.game.scroll[0])/50
            self.game.scroll[1]+=(self.rect().centery-90-self.game.screen.get_height()/2-self.game.scroll[1])/3
            self.loithoai.update()
            self.loithoai.render(self.game.screen,(0,self.game.screen.get_height() - 400))

        else:
            self.game.capnhatvitriplayer = True

        self.air_time+=1
            
        if self.collision['down'] :
            self.air_time =0   
        if not self.dead:
            dis_xx = self.game.player.rect().centerx - self.rect().centerx
            dis_yy = self.game.player.rect().centery - self.rect().centery

            dis_main = (dis_xx, dis_yy)
            # Cập nhật hướng di chuyển theo người chơi
        
            if abs(dis_xx) < 50000 and abs(dis_xx) >120 and self.ditheognguoichoi:  # Chỉ di chuyển khi khoảng cách phạm vi 400m vì là abs
                speed = min(0.9, max(0.5, abs(dis_xx) / 100))
                movement = (speed if dis_xx > 0 else -speed, movement[1]) # di chuyển trái phải  theo ng chs
                #if random.randint(0,100) >90:
                
                    
                self.flip = dis_xx < 0  # Lật nhân vật nếu cần
            self.targets =   [clone.rect() for clone in self.game.enemies]
            try:    
                # Tìm mục tiêu gần nhất
                closest_target = min(self.targets, key=lambda t: math.hypot(t.centerx - self.rect().centerx, t.centery - self.rect().centery))
                # Tính khoảng cách đến mục tiêu gần nhất
                dis_x =  closest_target.centerx - self.rect().centerx
                dis_y =  closest_target.centery - self.rect().centery
                dis = (dis_x,dis_y)
            except:
                dis_x =  dis_xx
                dis_y = dis_yy
                dis = dis_main
                
            
            if self.walking:
                if tilemap.solid_check((self.rect().centerx + (-20 if self.flip else 20), self.rect().centery+25)):
                    if (self.collision['right'] or self.collision['left']) and not self.attacking and not self.bidanh:
                        self.flip = not self.flip
                        
                    else:
                        movement = (movement[0] - 0.6 if self.flip else 0.6, movement[1])
                else:
                    self.flip = not self.flip
                self.walking = max(0, self.walking - 1)
                if(abs(dis[0])<=1000):
                    self.ditheognguoichoi = False
                    if  abs(dis_x) >100 and abs(dis_y) <150  and self.action!='attacklocxoaydai':  # Chỉ di chuyển khi khoảng cách phạm vi 400m vì là abs

                        speed = max(0.6, abs(dis_x) / 250)
                        movement = (speed if dis_x > 0 else -speed, movement[1])                      
                        self.flip = dis_x < 0  # Lật nhân vật nếu cần
                    
                
                
                else:
                    self.ditheognguoichoi=True
                if not self.walking:
                    chieu = random.randint(0,3)
                    if(abs(dis_main[0]<=300)):
                        if chieu ==3 and self.xuathienkhunghinhmap2 >700:
                            if (self.flip and dis_main[0] < 0) :
                                        self.attacking = True                               
                                        self.set_action('healing')                               
                            if (not self.flip and dis_main[0] > 0):
                                    self.attacking = True                           
                                    self.set_action('healing')
                                #gan thi danh
                    if (abs(dis[0])<=150 and abs(dis[1]<150)) and not self.attacking:
                        
                        if chieu ==1:
                            if (self.flip and dis[0] < 0) :
                                    self.attacking = True                               
                                    self.set_action('attacklocxoay')                               
                            if (not self.flip and dis[0] > 0):
                                self.attacking = True                           
                                self.set_action('attacklocxoay')                              
                        if chieu ==0:
                            if (self.flip and dis[0] < 0) :
                                    self.attacking = True                              
                                    self.set_action('attack')
                                                                
                            if (not self.flip and dis[0] > 0):
                                self.attacking = True                          
                                self.set_action('attack') 
                        if chieu ==2:
                            if (self.flip and dis[0] < 0) :
                                    self.attacking = True                              
                                    self.set_action('attacklocxoaydai')
                                                                
                            if (not self.flip and dis[0] > 0):
                                self.attacking = True                          
                                self.set_action('attacklocxoaydai') 
                        
                        


                    #cao thì nhảy lên 
                    if not self.ditheognguoichoi:

                        if (abs(dis[0])<365 and  abs(dis[1])>100) and abs(dis[1])<500:    
                            if self.flip:
                                                                                
                                if dis[0]<0:
                                                                
                                    if dis[1]<0:
                                        self.velocity[1]=-max(1,min(5,abs(dis[1])/250*5))
                                        self.velocity[0]=-max(3,dis[0]/200*3)
                                    else:
                                        self.velocity[0]=-max(3,dis[0]/200*3)
                                        self.velocity[1]=-2                                                     
                            else:                                                                      
                                if dis[0]>0:
                                    
                                    if dis[1]<0:                                   
                                        self.velocity[1]=-max(1,min(5,abs(dis[1])/250*5))
                                        self.velocity[0]=max(3,dis[0]/200*3)  
                                    else:                                      
                                        self.velocity[0]=max(3,dis[0]/200*3) 
                                        self.velocity[1]=-2  
                    else:
                        if (abs(dis_main[0])<365 and  abs(dis_main[1])>100) and abs(dis_main[1])<500:    
                            if self.flip:
                                                                                
                                if dis_main[0]<0:
                                                                
                                    if dis_main[1]<0:
                                        self.velocity[1]=-max(1,min(5,abs(dis_main[1])/250*5))
                                        self.velocity[0]=-max(3,dis_main[0]/200*3)
                                    else:
                                        self.velocity[0]=-max(3,dis_main[0]/200*3)
                                        self.velocity[1]=-2                                                     
                            else:                                                                      
                                if dis_main[0]>0:
                                    
                                    if dis_main[1]<0:                                   
                                        self.velocity[1]=-max(1,min(5,abs(dis_main[1])/250*5))
                                        self.velocity[0]=max(3,dis_main[0]/200*3)  
                                    else:                                      
                                        self.velocity[0]=max(3,dis_main[0]/200*3) 
                                        self.velocity[1]=-2  

            elif random.random() < 0.13:
                self.walking = random.randint(30, 120)
            
            super().update(tilemap, movement=movement)
            #hãm phanh
            if self.velocity[0] > 0:
                self.velocity[0] = max(self.velocity[0] - 0.1, 0)
            else:
                self.velocity[0] = min(self.velocity[0] + 0.1, 0)
            if self.bidanh or self.attacking:                        
                if self.collision['right']:  
                    self.flip = True   
                    self.pos[0]-=100
                    
                    
                elif  self.collision['left']  :
                    self.flip = False                            
                    self.pos[0]+=100
            if not self.attacking and not self.bidanh:
                if self.air_time > 4:
                        self.set_action('jump')
                elif movement[0] != 0:
                    self.set_action('run')
                else:
                    self.set_action('idle')
            if self.action == 'attacklocxoay':
                self.bidanh = False
                self.rectAttack=(-100,0,250,200,190)
                self.rectTuongTacEdit=(138,-100,0,0) 
                self.animation.framecuoi[0]= self.animation.img_duration *9+1
                self.animation.framecuoi[1]= self.animation.img_duration *2+1
                
                if self.flip:
                    if self.animation.doneToDoSomething:
                        self.pos[0]-=5               
                    
                else:
                    if self.animation.doneToDoSomething:
                        self.pos[0]+=5    


                if self.animation.done:

                    self.attacking = False
                    self.can_move = True
                    self.rectTuongTacEdit=(132,100,45,70)
                    self.rectAttack=(20,70,100,100,55)
                    if random.randint(0,1)==1:
                        self.attacking = True
                        self.set_action('attacklocxoay')
            if self.action == 'healing':
                self.bidanh = False
                self.rectAttack=(-100,0,0,0,190)
                self.game.player.duochealing = True
                if self.game.player.hp<10:
                    self.game.player.hp +=0.1

                if self.animation.done:
                    self.game.player.duochealing = False
                    self.attacking = False
                    self.can_move = True
                    self.rectTuongTacEdit=(132,100,45,70)
                    self.rectAttack=(20,70,100,100,55)
                    
            if self.action=='attack':
                self.bidanh = False
                self.animation.framecuoi[0]= self.animation.img_duration *9+1
                self.animation.framecuoi[1]= self.animation.img_duration *2+1
                
                if self.flip:
                    if self.animation.doneToDoSomething:
                        self.pos[0]-=5               
                    
                else:
                    if self.animation.doneToDoSomething:
                        self.pos[0]+=5    


                if self.animation.done:
                    self.attacking = False
                    self.can_move = True
            if self.action=='attacklocxoaydai':
                self.bidanh = False
                self.animation.framecuoi[0]= self.animation.img_duration *30+1
                self.animation.framecuoi[1]= self.animation.img_duration *2+1
                if self.flip:
                    if self.animation.doneToDoSomething:
                    
                        self.pos[0]-=7
                        
                    else:
                        self.pos[0]-=2          
                    self.rectTuongTacEdit=(-8,-100,0,0)     
                    self.rectAttack=(-100,0,250,200,190)
                else:
                    if self.animation.doneToDoSomething:
                        
                        self.pos[0]+=7
                    else:
                        self.pos[0]+=2
                        self.rectTuongTacEdit=(138,-100,0,0)     
                        self.rectAttack=(-100,0,250,200,190)
                if self.flip:
                    if self.animation.doneToDoSomething:
                        self.pos[0]-=5               
                    
                else:
                    if self.animation.doneToDoSomething:
                        self.pos[0]+=5    


                if self.animation.done:
                    self.attacking = False
                    self.can_move = True
                    self.rectTuongTacEdit=(132,100,45,70)
                    self.rectAttack=(20,70,100,100,55)
            for enemy in self.game.enemies:
                    if self.recttuongtac().colliderect(enemy.rectattack()):
                        if enemy.attacking  and enemy.animation.doneToDoSomething:
                            if self.hp <=0:
                                self.set_action('die')
                            else:  
                                                    
                                self.set_action('hurt')
                                self.hp-=0.1
        if self.action == 'hurt' :
            self.bidanh = True
            
            if self.flip:
                self.pos[0] +=random.randint(1,5)
                
            else:
                self.pos[0] -=random.randint(1,3)

            if self.attacking:
               self.attacking = False
            self.can_move = False
            if self.animation.done:
                
                self.bidanh = False
                self.can_move = True
                self.attacking = False
                
        if self.action =='die':
                if not self.bidanh: # ko bi danh trung , kiểu đnag bị đáng lại bị đánh
                    self.bidanh =True  
                if self.attacking:
                    self.attacking = False
                    self.game.player.duochealing = False

                self.can_move = False
                self.dead = True
                
                if self.hp <5:
                    self.hp+=0.005
                else:
                    self.animation.done = True
                    self.can_move = True
                    self.dead = False
                    self.set_action('run')
                    
                    
                       
        else:
            self.dead = False
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset) 

        bar_width = 90
        bar_height = 5
        # Tính toán chiều rộng của thanh máu dựa trên HP
        fill_width = int((self.hp / self.hp_max) * bar_width)
        disx = self.rect().centerx -self.game.player.rect().centerx
        disy = self.rect().centery -self.game.player.rect().centery
        

        if abs(disx) <500 and abs(disy)<200 and self.dead:
            pygame.draw.rect(surf, (128, 128, 128), (self.recttuongtac().x-offset[0]-25,self.recttuongtac().y-offset[1]-50, bar_width, bar_height))
            pygame.draw.rect(surf, (0,0,0), (self.recttuongtac().x-offset[0]-25,self.recttuongtac().y-offset[1]-50, fill_width, bar_height))               
    
            
        
    