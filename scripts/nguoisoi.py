import math
import random

import pygame
from scripts.particle import Particle
from scripts.spark import Spark
from scripts.entities import PhysicsEntity
class NguoiSoi(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'nguoisoi', pos, size)
        self.walking = 0
        self.dan=''
        self.banchua= False
        self.chuanbixong = True
        self.attacking = False
        self.hp =10
        self.hp_max = 10
        self.dead = False
        self.air_time =0

        self.targets = [] 
        
    def update(self, tilemap, movement=(0, 0)):
        if not self.dead :  # die thì ko đc lam j 
            # thanh hp
            
            # trường hợp rơi thì cx die
                self.air_time+=1
                if self.air_time>150:
                    self.hp =-1
                    self.set_action('die')
                if self.collision['down'] :
                    self.air_time =0
                dis_main9 = self.game.player.rect().centerx - self.rect().centerx
                if self.walking:# xử lý đi trên vùng ok , chạm trái phải thì lật
                    if tilemap.solid_check((self.rect().centerx + (-20 if self.flip else 20), self.rect().centery+25)):
                        if (self.collision['right'] or self.collision['left']):
                            self.flip = not self.flip
                            
                        else:
                            movement = (movement[0] - 0.7 if self.flip else 0.7, movement[1])
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
                        if (abs(dis[0])<=170 and abs(dis[1])<120):
                            if (self.flip and dis[0] < 0):
                                    self.attacking = True
                                    self.set_action('attackgan1')
                                    self.animation.framecuoi[0]= self.animation.img_duration *14+1
                                    self.animation.framecuoi[1]= self.animation.img_duration *1+1
                                    
                                    #if self.animation.done:
                                    #    self.attacking = False
                                        
                                

                            if (not self.flip and dis[0] > 0):
                                self.attacking = True
                                self.set_action('attackgan1')
                                self.animation.framecuoi[0]= self.animation.img_duration *14+1
                                self.animation.framecuoi[1]= self.animation.img_duration *1+1
                                
                        #cao thì nhảy lên     
                        if (abs(dis[0])<365 and  abs(dis[1])>100) and abs(dis[1])<400:    
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
                                
                                    
                            
                        if random.randint(0,100)<25  and abs(dis_x)<300 and self.air_time==0:
                            if self.flip and dis_x>30:
                                    
                                    self.pos[0]+=random.randint(15,20)
                                    self.flip = False
                            if self.flip == False and dis_x<-30:
                                
                                self.pos[0]-=random.randint(15,20) 
                                self.flip = True
                         
                elif   random.randint(0,100)< 100  and self.air_time==0:
                    self.walking = random.randint(30, 120)
                    # người chs đến gần thì dí
                    
                    
                    if   abs(dis_main9)<500:
                            if self.flip and dis_main9>10:
                                    
                                    self.pos[0]+=random.randint(15,20)
                                    self.flip = False
                            if self.flip == False and dis_main9<-10:
                                
                                self.pos[0]-=random.randint(15,20) 
                                self.flip = True 
                    
                    
                
                super().update(tilemap, movement=movement)
                
                #hãm phanh
                if self.velocity[0] > 0:
                    self.velocity[0] = max(self.velocity[0] - 0.1, 0)
                else:
                    self.velocity[0] = min(self.velocity[0] + 0.1, 0)


                if self.action =='attackgan1':
                            if self.animation.done:
                                self.attacking = False 
                                self.can_move= True  
                if not self.attacking and not self.bidanh:
                                    if self.air_time > 4:
                                        self.set_action('jump')
                                    elif movement[0] != 0:
                                        self.set_action('walk')
                                    else:
                                        self.set_action('walk')
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
                        self.set_action('attackgan1')
                    else:
                        self.attacking = True
                        self.set_action('attackgan1')

                else:
                    if self.flip:
                        self.attacking = True
                        self.set_action('attackgan1')
                    else:
                        self.flip = False
                        self.attacking = True
                        self.set_action('attackgan1')

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
                    for i in range(30):
                        angle = random.random() * math.pi * 2
                        speed = random.random() * 10
                        self.game.sparks.append(Spark(self.recttuongtac().center, angle, 4 + random.random()))
                        self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                    self.game.sparks.append(Spark(self.rect().center, 0,5 + random.random()))
                    self.game.sparks.append(Spark(self.rect().center, math.pi, 5 + random.random()))
                    self.game.sfx['boom'].play()
                    return True    
        else:
            self.dead = False
            return False       
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)
        bar_width = 90
        bar_height = 5
        # Tính toán chiều rộng của thanh máu dựa trên HP
        fill_width = int((self.hp / self.hp_max) * bar_width)
        disx = self.rect().centerx -self.game.player.rect().centerx
        disy = self.rect().centery -self.game.player.rect().centery
        

        if abs(disx) <200 and abs(disy)<200:
            pygame.draw.rect(surf, (128, 128, 128), (self.recttuongtac().x-offset[0]+25,self.recttuongtac().y-offset[1]-50, bar_width, bar_height))
            pygame.draw.rect(surf, (255,0,0), (self.recttuongtac().x-offset[0]+25,self.recttuongtac().y-offset[1]-50, fill_width, bar_height))
        
    