from scripts.entities import PhysicsEntity
import math
import random

import pygame

from scripts.particle import Particle
from scripts.spark import Spark

class PhanThan(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'phanthan', pos, size)
        
        self.walking = 0
        self.dan=''
        self.banchua= False
        self.chuanbixong = True
        self.hp =3
        self.hp_max =3
        self.dead = False
        self.diquaivat = False
        self.attacking = False
        self.timetontai =0
        self.targets = []  # Danh sách các vị trí mục tiêu, gồm cả nhân vật chính và phân thân
        self.air_time =0
        
    def update(self, tilemap, movement=(0, 0)):
        
       
        if   not self.dead : # die thì ko đc lam j cả
            
            self.air_time+=1
            
            if self.collision['down'] :
                self.air_time =0


            # Tính toán khoảng cách đến người chơi
            # Cập nhật danh sách các vị trí mục tiêu
            self.targets = [clone.rect() for clone in self.game.enemies]
            
            # Tìm mục tiêu gần nhất
            try:
                closest_target = min(self.targets, key=lambda t: math.hypot(t.centerx - self.rect().centerx, t.centery - self.rect().centery))
                 # Tính khoảng cách đến mục tiêu gần nhất
                dis_x = closest_target.centerx - self.rect().centerx
                dis_y = closest_target.centery - self.rect().centery

                
                # Cập nhật hướng di chuyển theo người chơi
            
                
            except:
                dis_x = self.game.player.rect().centerx - self.rect().centerx
                dis_y = self.game.player.rect().centery - self.rect().centery
            dis = (dis_x, dis_y)
            if abs(dis_x) < 900 and  abs(dis_x) >100 and abs(dis_y) <150 :  # Chỉ di chuyển khi khoảng cách phạm vi 400m vì là abs

                    speed = max(0.6, abs(dis_x) / 250)
                    movement = (speed if dis_x > 0 else -speed, movement[1]) # di chuyển trái phải  theo ng chs
                    #if random.randint(0,100) >90:
                    
                        
                    self.flip = dis_x < 0  # Lật nhân vật nếu cần
                    self.diquaivat = True
                #if abs(dis_y) > 100:
                # movement = (movement[0], -0.01)
                
            else:
                    
                 self.diquaivat = False
                           
            if self.walking:# xử lý đi trên vùng ok , chạm trái phải thì lật
                if tilemap.solid_check((self.rect().centerx + (-20 if self.flip else 20), self.rect().centery+25)):
                    if (self.collision['right'] or self.collision['left']):
                        self.flip = not self.flip
                        
                    else:
                        movement = (movement[0] - 0.8 if self.flip else 0.8, movement[1])
                else:
                    self.flip = not self.flip
                self.walking = max(0, self.walking - 1)

                if not self.walking :
                    
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
            
            for enemy in self.game.enemies:
                if self.recttuongtac().colliderect(enemy.rectattack()):
                    if enemy.attacking  and enemy.animation.doneToDoSomething:
                        if not self.bidanh : # ko bi danh trung , kiểu đnag bị đáng lại bị đánh
                            self.bidanh =True
                            self.set_action('hurt')
                        if self.hp <=0:
                            self.set_action('die')
            if self.action =='attack':
                
                if random.randint(0,100)<2:
                    self.game.sfx['wukongvoicechieudai'].play()
                if self.animation.done:
                    self.attacking = False 
                    self.can_move= True 
                    # NEWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW cách ko bị đơ
                     
                    self.bidanh = False
               
                     
                     
                    
            # dung va chay
            if not self.attacking and not self.bidanh:
                
                if self.air_time > 4:
                    self.set_action('jump')
                elif movement[0] != 0:
                    self.set_action('run')
                else:
                    self.set_action('idle')

        
            self.timetontai+=1
            if self.timetontai>3000 or self.game.dead!=0:
                    if not self.bidanh: # ko bi danh trung , kiểu đnag bị đáng lại bị đánh
                            self.bidanh =True          
                    if self.hp <=0:
                            self.set_action('die')
                    else:
                        self.hp=-1
                        
            if self.game.player.attacking:
                if self.game.player.animation.doneToDoSomething:
                    if self.recttuongtac().colliderect(self.game.player.rectattack()):
                            if not self.bidanh: # ko bi danh trung , kiểu đnag bị đáng lại bị đánh
                                self.bidanh =True          
                            if self.hp <=0:
                                self.set_action('die')
                            else:
                                self.set_action('hurt')
            for danlac  in self.game.projectiles:
                if  danlac[3] =='kiemnangluong1' or danlac[3] =='kiemnangluong2':
                    if self.recttuongtac().collidepoint(danlac[0][0]+random.randint(-5,5),danlac[0][1]+random.randint(-45,45)):
                        self.game.projectiles.remove(danlac)
                        if not self.bidanh: # ko bi danh trung , kiểu đnag bị đáng lại bị đánh
                                self.bidanh =True          
                        if self.hp <=0:
                                self.set_action('die')
                        else:
                                self.set_action('hurt')
                            
                            
                        
                        #self.dead = True
                        
                elif self.recttuongtac().collidepoint(danlac[0]): #cho biết điểm pos của đạn có nằm trong hình chữ nhật hay không.
                    # còn thêm colliderList nữa
                    self.game.projectiles.remove(danlac)
                    if not self.bidanh: # ko bi danh trung , kiểu đnag bị đáng lại bị đánh
                                self.bidanh =True          
                    if self.hp <=0:
                            self.set_action('die')
                    else:
                            self.set_action('hurt')
        #hãm phanh
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)       


        if self.action == 'hurt' :
            
            if self.flip == False:
                self.pos[0] +=5.5
                self.pos[1] -=random.randint(5,13)
                
            else:
                self.pos[0] -=5.5 
                self.pos[1] -=random.randint(5,13)

            if self.attacking:
               self.attacking = False
            self.can_move = False
            if self.animation.done:
                self.hp-=1
                self.attacking = True
                self.set_action('attack')
                self.bidanh = False
                self.can_move = True  

        if self.action =='die':
            if not self.bidanh: # ko bi danh trung , kiểu đnag bị đáng lại bị đánh
                self.bidanh =True  
            if self.attacking:
                self.attacking = False
            self.can_move = False
            if self.animation.done:
                self.dead = True
                self.game.sfx['tocbien'].play()
                return True    
        else:
            self.dead = False
            return False   
            
    # chỉnh lại vị trí animation phù hợp với vị trí đang ở hiện tại
    def render(self, surf, offset=(0, 0)):
        if self.action == 'attack':
            self.anim_offset=(-90,-75)
            super().render(surf, offset=offset)
        elif self.action == 'die':
            self.anim_offset=(-70,-60)
            super().render(surf, offset=offset)
        else:
            self.anim_offset=(0,0)
            super().render(surf, offset=offset)
        super().render(surf, offset=offset)
        bar_width = 90
        bar_height = 5
        # Tính toán chiều rộng của thanh máu dựa trên HP
        fill_width = int((self.hp / self.hp_max) * bar_width)
       
        #pygame.draw.rect(surf, (128, 128, 128), (self.recttuongtac().x-offset[0]+25,self.recttuongtac().y-offset[1]-50, bar_width, bar_height))
        #pygame.draw.rect(surf, (255,0,0), (self.recttuongtac().x-offset[0]+25,self.recttuongtac().y-offset[1]-50, fill_width, bar_height))

