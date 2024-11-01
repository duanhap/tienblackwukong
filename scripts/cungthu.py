from scripts.entities import PhysicsEntity
import math
import random

import pygame

from scripts.particle import Particle
from scripts.spark import Spark

class CungThu(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'cungthu', pos, size)
        
        self.walking = 0
        self.dan='cungten'
        self.banchua= False
        self.chuanbixong = True
        self.attacking = False
        self.hp =2
        self.hp_max = 2
        self.dead = False
        self.air_time =0
       
        
        self.targets = []  # Danh sách các vị trí mục tiêu, gồm cả nhân vật chính và phân thân
        
        
    def update(self, tilemap, movement=(0, 0)):
        
       
        if not self.dead :  # die thì ko đc lam j 
            
            # dang đánh mà die thì cút
            
            
            # trường hợp rơi thì cx die
                self.air_time+=1
                if self.air_time>150:
                    self.hp =-1
                    self.set_action('die')
                if self.collision['down'] :
                    self.air_time =0
                if self.walking:# xử lý đi trên vùng ok , chạm trái phải thì lật
                    if tilemap.solid_check((self.rect().centerx + (-20 if self.flip else 20), self.rect().centery+25)):
                        if (self.collision['right'] or self.collision['left']):
                            self.flip = not self.flip
                            
                        else:
                            movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
                    else:
                        self.flip = not self.flip
                    self.walking = max(0, self.walking - 1)

                    if not self.walking  and self.hp>0 and self.dead== False:
                        

                        # Cập nhật danh sách các vị trí mục tiêu
                        self.targets = [self.game.player.rect()] + [clone.rect() for clone in self.game.phanthans]
                        
                        # Tìm mục tiêu gần nhất
                        closest_target = min(self.targets, key=lambda t: math.hypot(t.centerx - self.rect().centerx, t.centery - self.rect().centery))
                        
                        # Tính khoảng cách đến mục tiêu gần nhất
                        dis_x = closest_target.centerx - self.rect().centerx
                        dis_y = closest_target.centery - self.rect().centery

                        dis = (dis_x, dis_y)
                        #kc Y <16 và X
                        #gan thi danh
                        if (abs(dis[0])<=100 and abs(dis[1])<80):
                            if (self.flip and dis[0] < 0):
                                    self.attacking = True
                                    self.set_action('attackgan')
                                    self.animation.framecuoi[0]= self.animation.img_duration *4+1
                                    self.animation.framecuoi[1]= self.animation.img_duration *2+1
                                    
                                    #if self.animation.done:
                                    #    self.attacking = False
                                        
                                

                            if (not self.flip and dis[0] > 0):
                                self.attacking = True
                                self.set_action('attackgan')
                                self.animation.framecuoi[0]= self.animation.img_duration *4+1
                                self.animation.framecuoi[1]= self.animation.img_duration *2+1
                                
                                #if self.animation.done:
                                #   self.attacking = False
                        # cx gan thi đâm
                        elif (abs(dis[0])<=300 and abs(dis[1])<80) and random.randint(0,50)<40:
                            if (self.flip and dis[0] < 0):
                                self.attacking = True
                                self.set_action('attackchuanbigandam')
                                            
                                    

                            if (not self.flip and dis[0] > 0):
                                self.attacking = True
                                self.set_action('attackchuanbigandam')
                        # thâp thi ngồi bắn        
                        elif((dis[1]) >=0)and((dis[1]) <=35) and abs(dis[0])<=3000 and random.randint(0,50)<50:
                            if (self.flip and dis[0] < 0):
                                    self.attacking = True
                                    self.set_action('attackngoi')
                                    self.banchua = False
                                    if self.animation.done:
                                        self.attacking = False
                                        
                                

                            if (not self.flip and dis[0] > 0):
                                self.attacking = True
                                self.set_action('attackngoi')
                                self.banchua = False
                                if self.animation.done:
                                    self.attacking = False
                        # cao thì đứng bắn
                        if (dis[1]) > -100 and (dis[1]) <100 and abs(dis[0])<=3000 and abs(dis[0])>=10 and random.randint(0,50)<8.5:
                            
                                # đang quay trái bắn trái nếu gặp
                                if (self.flip and dis[0] < 0):
                                    #self.attacking = True
                                    self.set_action('attack')
                                    self.banchua = False
                                    if self.animation.done:
                                        self.attacking = False
                                        
                                        
                                

                                if (not self.flip and dis[0] > 0):
                                    
                                    #self.attacking = True
                                    self.set_action('attack')
                                    self.banchua = False
                                    if self.animation.done:
                                        self.attacking = False
                        if random.randint(0,100)<25  and abs(dis_x)<300:
                            if self.flip and dis_x>30:
                                    
                                    self.pos[0]+=random.randint(15,20)
                                    self.flip = False
                            if self.flip == False and dis_x<-30:
                                
                                self.pos[0]-=random.randint(15,20) 
                                self.flip = True         
                elif random.randint(0,100)< 25 :
                    self.walking = random.randint(30, 120)
                    # người chs đến gần thì dí
                    dis_x = self.game.player.rect().centerx - self.rect().centerx
                    if random.randint(0,100)<25  and abs(dis_x)<300:
                            if self.flip and dis_x>30:
                                    
                                    self.pos[0]+=random.randint(15,20)
                                    self.flip = False
                            if self.flip == False and dis_x<-30:
                                
                                self.pos[0]-=random.randint(15,20) 
                                self.flip = True 
                
                super().update(tilemap, movement=movement)
                
                if self.action =='attack':
                    self.animation.framecuoi[0]= self.animation.img_duration *3+1
                    if self.animation.doneToDoSomething and not self.banchua:
                        if self.flip:
                            self.game.projectiles.append([[self.rect().centerx - 120, self.rect().centery-90], -8, 0,'cungten2'])
                            for i in range(4):
                                self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5 + math.pi, 2 + random.random()))
                            self.banchua = True   
                        else:
                            self.game.projectiles.append([[self.rect().centerx +120, self.rect().centery-90], 8, 0,'cungten1'])
                            for i in range(4):
                                self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5, 2 + random.random()))
                            self.banchua = True 
                if self.action =='attackgan':
                    if self.animation.done:
                        self.attacking = False 
                        self.can_move= True  
                if self.action =='attackngoi':
                    self.animation.framecuoi[0]= self.animation.img_duration *3+1
                    if self.animation.doneToDoSomething and not self.banchua:
                        if self.flip:
                            self.game.projectiles.append([[self.rect().centerx - 120, self.rect().centery-45], -8, 0,'cungten2'])
                            for i in range(4):
                                self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5 + math.pi, 2 + random.random()))
                            self.banchua = True   
                        else:
                            self.game.projectiles.append([[self.rect().centerx +120, self.rect().centery-45], 8, 0,'cungten1'])
                            for i in range(4):
                                self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5, 2 + random.random()))
                            self.banchua = True  

                if self.action =='attackchuanbigandam':
                        # Cập nhật danh sách các vị trí mục tiêu
                    self.targets = [self.game.player.rect()] + [clone.rect() for clone in self.game.phanthans]
                    
                    # Tìm mục tiêu gần nhất
                    closest_target = min(self.targets, key=lambda t: math.hypot(t.centerx - self.rect().centerx, t.centery - self.rect().centery))
                    
                    # Tính khoảng cách đến mục tiêu gần nhất
                    dis_x = closest_target.centerx - self.rect().centerx
                    dis_y = closest_target.centery - self.rect().centery

                    dis = (dis_x, dis_y)
                    

                    if self.animation.done:
                        if  self.flip:
                            
                            for i in range(30):
                                angle = random.random() * math.pi * 2
                                speed = random.random() *5
                                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                            self.pos[0]-=max(80,(abs(dis[0])-60))
                            self.game.sfx['tocbienquai'].play()
                            
                            self.set_action('attackgandam')
                            self.animation.framecuoi[0]= self.animation.img_duration *8+1
                            self.animation.framecuoi[1]= self.animation.img_duration *2+1
                            self.banchua = False
                            self.banchua = False
                            if self.animation.done:
                                self.attacking = False

                        else:
                            for i in range(30):
                                    angle = random.random() * math.pi * 2
                                    speed = random.random() * 5
                                    self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed *0.5], frame=random.randint(0, 7)))
                                
                            self.pos[0]+=max(80,(abs(dis[0])-60))
                            self.game.sfx['tocbienquai'].play()
                            self.set_action('attackgandam')
                            self.animation.framecuoi[0]= self.animation.img_duration *8+1
                            self.animation.framecuoi[1]= self.animation.img_duration *2+1
                            self.banchua = False
                            if self.animation.done:
                                self.attacking = False

                # dung va chay
                if not self.attacking and not self.bidanh:
                    
                    if movement[0] != 0:
                        self.set_action('run')
                    else:
                        self.set_action('idle')

            

                if self.game.player.attacking:
                    if self.game.player.animation.doneToDoSomething:
                        if self.recttuongtac().colliderect(self.game.player.rectattack()):
                                if not self.bidanh: # ko bi danh trung , kiểu đnag bị đáng lại bị đánh
                                    self.bidanh =True          
                                if self.hp <=0:
                                    self.set_action('die')
                                else:
                                    self.set_action('hurt')
                for phanthan in self.game.phanthans:
                    if phanthan.animation.doneToDoSomething:
                            if self.recttuongtac().colliderect(phanthan.rectattack()):
                                    if not self.bidanh: # ko bi danh trung , kiểu đnag bị đáng lại bị đánh
                                        self.bidanh =True          
                                    if self.hp <=0:
                                        self.set_action('die')
                                    else:
                                        
                                        self.set_action('hurt')               
                    
                     
        if self.action == 'hurt' :
            
            if self.game.player.flip == False:
                self.pos[0] +=random.randint(1,5)
                
            else:
                self.pos[0] -=random.randint(1,3)

            if self.attacking:
               self.attacking = False
            self.can_move = False
            if self.animation.done:
                self.hp-=1
                if self.game.player.flip:
                    if self.flip:
                        self.flip = False
                        self.attacking = True
                        self.set_action('attackgan')
                    else:
                        self.attacking = True
                        self.set_action('attackgan')

                else:
                    if self.flip:
                        self.attacking = True
                        self.set_action('attackgan')
                    else:
                        self.flip = False
                        self.attacking = True
                        self.set_action('attackgan')

                self.bidanh = False
                self.can_move = True  
       
        if self.action =='die':
            # 3 dòng nì quan trọng

            if not self.bidanh: # ko bi danh trung , kiểu đnag bị đáng lại bị đánh
                self.bidanh =True  
            if self.attacking:
                self.attacking = False
            self.can_move = False
            if self.animation.done:
                self.dead = True
                for i in range(30):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 10
                    self.game.sparks.append(Spark(self.recttuongtac().center, angle, 4 + random.random()))
                    self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                    self.game.sfx['boom'].play()
                #self.game.sparks.append(Spark(self.rect().center, 0, 5+ random.random()))
                #self.game.sparks.append(Spark(self.rect().center, math.pi, 5 + random.random()))
                return True    
        else:
            self.dead = False
            return False               
               
                
            
            

    def render(self, surf, offset=(0, 0)):
        if self.attacking:
            self.anim_offset=(-8,-1)
            super().render(surf, offset=offset)
        else:
            self.anim_offset=(0,0)
            super().render(surf, offset=offset)
        
        super().render(surf, offset=offset)
        bar_width = 90
        bar_height = 5
        # Tính toán chiều rộng của thanh máu dựa trên HP
        fill_width = int((self.hp / self.hp_max) * bar_width)
        disx = self.rect().centerx -self.game.player.rect().centerx
        disy = self.rect().centery -self.game.player.rect().centery
        

        if abs(disx) <200 and abs(disy)<200:
            pygame.draw.rect(surf, (128, 128, 128), (self.recttuongtac().x-offset[0]-10,self.recttuongtac().y-offset[1]-30, bar_width, bar_height))
            pygame.draw.rect(surf, (255,0,0), (self.recttuongtac().x-offset[0]-10,self.recttuongtac().y-offset[1]-30, fill_width, bar_height))
        
            
        
    