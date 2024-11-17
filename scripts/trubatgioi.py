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
        self.dan=''
        self.ditheognguoichoi = True
        self.xuathienkhunghinhmap2=0
        self.loithoai =  Loithoai(self.game,'batgioi')
        self.targets = [] 
        
    def update(self, tilemap, movement=(0, 0)):
        self.xuathienkhunghinhmap2+=1
        if self.xuathienkhunghinhmap2 <700 and self.xuathienkhunghinhmap2 >100:
            self.game.capnhatvitriplayer = False
            self.game.scroll[0]+=(self.rect().centerx-self.game.screen.get_width()/2-self.game.scroll[0])/50
            self.game.scroll[1]+=(self.rect().centery-90-self.game.screen.get_height()/2-self.game.scroll[1])/3
            self.loithoai.update()
            self.loithoai.render(self.game.screen,(0,self.game.screen.get_height() - 400))

        else:
            self.game.capnhatvitriplayer = True

            

        dis_x = self.game.player.rect().centerx - self.rect().centerx
        dis_y = self.game.player.rect().centery - self.rect().centery

        dis = (dis_x, dis_y)
        # Cập nhật hướng di chuyển theo người chơi
       
        if abs(dis_x) < 50000 and abs(dis_x) >120:  # Chỉ di chuyển khi khoảng cách phạm vi 400m vì là abs
            speed = min(0.9, max(0.5, abs(dis_x) / 100))
            movement = (speed if dis_x > 0 else -speed, movement[1]) # di chuyển trái phải  theo ng chs
            #if random.randint(0,100) >90:
            
                
            self.flip = dis_x < 0  # Lật nhân vật nếu cần
            
        #if abs(dis_y) > 100:
        # movement = (movement[0], -0.01)
        if self.walking:# xử lý đi trên vùng ok , chạm trái phải thì lật
            if tilemap.solid_check((self.rect().centerx + (-20 if self.flip else 20), self.rect().centery+25)):
                if (self.collision['right'] or self.collision['left']):
                    self.flip = not self.flip
                    
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)

            if not self.walking:
                #kc giữa pl và en
                try:
                        # Cập nhật danh sách các vị trí mục tiêu
                        self.targets =   [clone.rect() for clone in self.game.enemies]
                        
                        # Tìm mục tiêu gần nhất
                        closest_target = min(self.targets, key=lambda t: math.hypot(t.centerx - self.rect().centerx, t.centery - self.rect().centery))
                        # Tính khoảng cách đến mục tiêu gần nhất
                        dis_x =  closest_target.centerx - self.rect().centerx
                        dis_y =  closest_target.centery - self.rect().centery

                        
                    
                except:
                    dis_x = self.game.player.rect().centerx - self.rect().centerx
                    dis_y = self.game.player.rect().centery - self.rect().centery          
                dis = (dis_x, dis_y)
                      
                        #gan thi danh
                if (abs(dis[0])<=150 and abs(dis[1]<150)) and not self.attacking:
                    if (self.flip and dis[0] < 0) :
                            self.attacking = True
                            
                            self.set_action('attack')
                            
                            self.animation.framecuoi[0]= self.animation.img_duration *5+1
                            self.animation.framecuoi[1]= self.animation.img_duration *3+1
                            
                            
                    if (not self.flip and dis[0] > 0):
                        self.attacking = True
                        
                        self.set_action('attack')                              
                        self.animation.framecuoi[0]= self.animation.img_duration *5+1
                        self.animation.framecuoi[1]= self.animation.img_duration *3+1
                #cao thì nhảy lên     
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
           
        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)
        
        super().update(tilemap, movement=movement)
        if not self.attacking:
            if movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')
        if self.action=='attack':

            if self.animation.done:
                self.attacking = False
                self.can_move = True
       
    
            
        
    