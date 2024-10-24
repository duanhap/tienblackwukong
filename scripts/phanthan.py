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
        self.dead = False
        self.diquaivat = False
        self.attacking = False
        self.timetontai =0
        self.targets = []  # Danh sách các vị trí mục tiêu, gồm cả nhân vật chính và phân thân
        
        
    def update(self, tilemap, movement=(0, 0)):
        
        if (self.dead or self.hp<=0) and self.action=='die' and self.animation.done:
             return True
            
             
        elif   not self.dead : # die thì ko đc lam j cả
            
                    
                    
            # Tính toán khoảng cách đến người chơi
            # Cập nhật danh sách các vị trí mục tiêu
            self.targets = [clone.rect() for clone in self.game.enemies]
            
            # Tìm mục tiêu gần nhất
            try:
                closest_target = min(self.targets, key=lambda t: math.hypot(t.centerx - self.rect().centerx, t.centery - self.rect().centery))
                 # Tính khoảng cách đến mục tiêu gần nhất
                dis_x = closest_target.centerx - self.rect().centerx
                dis_y = closest_target.centery - self.rect().centery

                dis = (dis_x, dis_y)
                # Cập nhật hướng di chuyển theo người chơi
            
                if abs(dis_x) < 900 and  abs(dis_x) >130 and abs(dis_y) <150 and random.randint(0,100)<99:  # Chỉ di chuyển khi khoảng cách phạm vi 400m vì là abs

                    speed = max(0.6, abs(dis_x) / 250)
                    movement = (speed if dis_x > 0 else -speed, movement[1]) # di chuyển trái phải  theo ng chs
                    #if random.randint(0,100) >90:
                    
                        
                    self.flip = dis_x < 0  # Lật nhân vật nếu cần
                    self.diquaivat = True
                #if abs(dis_y) > 100:
                # movement = (movement[0], -0.01)
                else:
                    
                    self.diquaivat = False
            except:
                closest_target=0
              
           
            
            if self.walking:# xử lý đi trên vùng ok , chạm trái phải thì lật
                if tilemap.solid_check((self.rect().centerx + (-20 if self.flip else 20), self.rect().centery+25)):
                    if (self.collision['right'] or self.collision['left']):
                        self.flip = not self.flip
                        
                    else:
                        movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
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

                        dis = (dis_x, dis_y)
                      
                        #gan thi danh
                        if (abs(dis[0])<=150 and abs(dis[1]<150)):
                            if (self.flip and dis[0] < 0):
                                    self.attacking = True
                                    self.set_action('attack')
                                    self.animation.framecuoi[0]= self.animation.img_duration *5+1
                                    self.animation.framecuoi[1]= self.animation.img_duration *3+1
                                    
                                    if self.animation.done:
                                        self.attacking = False
                                        
                                

                            if (not self.flip and dis[0] > 0):
                                self.attacking = True
                                self.set_action('attack')
                                self.animation.framecuoi[0]= self.animation.img_duration *5+1
                                self.animation.framecuoi[1]= self.animation.img_duration *3+1
                                
                                if self.animation.done:
                                    self.attacking = False
                    
                    except:
                         self.can_move = False           
                    
                                


            elif random.random() < 0.01:
                self.walking = random.randint(30, 120)
            
            super().update(tilemap, movement=movement)
            
            for enemy in self.game.enemies:
                if self.recttuongtac().colliderect(enemy.rectattack()):
                    if enemy.attacking  and enemy.animation.doneToDoSomething:
                        if not self.bidanh and not self.dead: # ko bi danh trung , kiểu đnag bị đáng lại bị đánh
                            self.bidanh =True
                            self.set_action('hurt')
                        if self.hp <=0:
                            self.set_action('die')
            if self.action =='attack':
                if random.randint(0,100)<50:
                    self.game.sfx['wukongvoicechieudai'].play()
                if self.animation.done:
                    self.attacking = False 
                    self.can_move= True  
            
            # dung va chay
            if not self.attacking and not self.bidanh:
                
                if movement[0] != 0:
                    self.set_action('run')
                else:
                    self.set_action('idle')

        
            self.timetontai+=1
            if self.timetontai>2000 or self.game.dead!=0:
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
                         
        if self.action == 'hurt' :
            
            if self.flip == False:
                self.pos[0] +=5.5
                self.pos[1] -=15
                
            else:
                self.pos[0] -=5.5 
                self.pos[1] -=15

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
    
