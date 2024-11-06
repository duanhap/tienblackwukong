import math
import random

import pygame

from scripts.particle import Particle
from scripts.spark import Spark
from scripts.entities import PhysicsEntity
class BossNguoiDa(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'bossnguoida', pos, size)
        self.walking = 0
        self.dan=''
        self.banchua= False
        self.chuanbixong = True
        self.attacking = False
        self.hp =20
        self.hp_max = 20
        self.dead = False
        self.air_time =0
        self.chuanbixong = False
        self.targets = [] 
        self.blocking = False

        self.landaugap= True
        
    def update(self, tilemap, movement=(0, 0)):
        disx1 = self.rect().centerx -self.game.player.rect().centerx
        disy1 = self.rect().centery -self.game.player.rect().centery
        
        
        if not self.chuanbixong:
            self.set_action('xuathien')
            super().update(tilemap, movement=movement)
            
            if abs(disx1) >10 and self.landaugap:
                self.animation.ngatchieu = True
                
            else:
                self.animation.ngatchieu = False
                self.landaugap= False
            
           
            

        else:
             
            if not self.dead :  # die thì ko đc lam j 
                
                # dang đánh mà die thì cút
                
                
                # trường hợp rơi thì cx die
                    self.air_time+=1
                    if self.air_time>150:
                        return True
                    if self.collision['down'] :
                        self.air_time =0

                        
                    dis_main9 = self.game.player.rect().centerx - self.rect().centerx
                    if self.walking:# xử lý đi trên vùng ok , chạm trái phải thì lật
                        if tilemap.solid_check((self.rect().centerx + (-20 if self.flip else 20), self.rect().centery+25)):
                            if (self.collision['right'] or self.collision['left']):
                                self.flip = not self.flip
                                
                            else:
                                movement = (movement[0] - 0.9 if self.flip else 0.9, movement[1])
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
                            if (abs(dis[0])<150 and abs(dis[0])>=10) :
                                if (self.flip and dis[0] < 0):
                                    self.blocking = True                                       
                                    self.set_action('block')                                               
                                if (not self.flip and dis[0] > 0):
                                    self.blocking = True                                    
                                    self.set_action('block')
                            
                            elif (abs(dis[0])<300 and abs(dis[0])>=50 and abs(dis[1])<1200):
                                if (self.flip and dis[0] < 0):
                                        self.attacking = True
                                        self.set_action('attackgan')
                                        
                                    
                                if (not self.flip and dis[0] > 0):
                                    self.attacking = True
                                    self.set_action('attackgan')
                                    
                                 
                            elif (abs(dis[0])<=600 and abs(dis[0])>=250 and abs(dis[1])<1200):
                                if (self.flip and dis[0] < 0):
                                        self.attacking = True
                                        self.set_action('attackchocxa')
                                        
                                    
                                if (not self.flip and dis[0] > 0):
                                    self.attacking = True
                                    self.set_action('attackchocxa')
                                    
                            
                                 
                            
                            if random.randint(0,100)<25  and abs(dis_x)<300:
                                if self.flip and dis_x>30:
                                        
                                        self.pos[0]+=random.randint(15,20)
                                        self.flip = False
                                if self.flip == False and dis_x<-30:
                                    
                                    self.pos[0]-=random.randint(15,20) 
                                    self.flip = True
                            
                    elif   random.randint(0,100)< 2  and self.hp>0 and not self.attacking:
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

                    if self.action == 'block' :
                        self.bidanh=True
                        
                        if self.game.player.flip == False:
                            self.pos[0] +=random.randint(1,3)
                            
                                
                        else:
                            self.pos[0] -=random.randint(1,3)
                            
                        
                        
                        
                        if self.animation.done:
                            self.bidanh = False
                            self.blocking = False 
                            self.can_move = True
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

                            
                              
                       
                    if self.action =='attackchocxa':
                                self.animation.framecuoi[0]= self.animation.img_duration *14+1
                                self.animation.framecuoi[1]= self.animation.img_duration *3+1
                                self.rectAttack=(380,250,100,400,100)
                                
                                self.bidanh= False
                                self.blocking = False
                                
                                if self.animation.done:
                                    self.attacking = False 
                                    self.can_move= True
                                    
                    if self.action =='attackgan':
                                self.animation.framecuoi[0]= self.animation.img_duration *7.5+1
                                self.animation.framecuoi[1]= self.animation.img_duration *3+1
                                self.rectAttack=(0,550,500,100,500) 
                                self.bidanh= False
                                self.blocking = False
                                
                                if self.animation.done:
                                    self.attacking = False 
                                    self.can_move= True
                                    if self.flip and self.animation.doneToDoSomething:
                                        self.velocity[0]=-1.5
                                    else:
                                        self.velocity[0]=1.5   
                    if not self.attacking and not self.bidanh and not self.blocking:
                                        
                                        if movement[0] != 0:
                                            self.set_action('idle')
                                        else:
                                            self.set_action('idle')
                                            
                                        
                                             
                    if self.game.player.attacking:
                                if self.game.player.animation.doneToDoSomething:
                                    if self.recttuongtac().colliderect(self.game.player.rectattack()):
                                               
                                            if not self.blocking:
                                                       
                                                if self.hp <=0:
                                                    self.set_action('die')
                                                else:
                                                    if self.game.player.action=='attack4':
                                                        self.hp-=0.05
                                                    else:
                                                        self.hp-=0.02
                                                    self.set_action('hurt')
                                                     
                    for phanthan in self.game.phanthans:
                        if phanthan.animation.doneToDoSomething:
                                if self.recttuongtac().colliderect(phanthan.rectattack()):
                                                 
                                        if not self.blocking:
                                                       
                                                if self.hp <=0:
                                                    self.set_action('die')
                                                else:
                                                    self.hp-=0.02
                                                    self.set_action('hurt')
                                                         
        if self.action =='xuathien':
            self.flip = True
            if self.animation.done:
                self.flip = not self.flip
                self.chuanbixong = True
        if self.action == 'hurt' :
            self.bidanh = True
            if self.game.player.flip == False:
                self.pos[0] +=random.randint(1,5)
                
            else:
                self.pos[0] -=random.randint(1,3)

            if self.attacking:
               self.attacking = False
            self.can_move = False
            if self.animation.done:
                
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
        if self.action == 'die':
            if not self.flip:
                self.anim_offset=(140,-20)
            else:
                self.anim_offset=(-50,-20)
        else:
            self.anim_offset=(0,0)  
        if self.action == 'xuathien':
            
            self.anim_offset=(145,-20)
            
          
        super().render(surf, offset=offset)
        
        
        bar_width = 90
        bar_height = 5
        # Tính toán chiều rộng của thanh máu dựa trên HP
        fill_width = int((self.hp / self.hp_max) * bar_width)
        disx = self.rect().centerx -self.game.player.rect().centerx
        disy = self.rect().centery -self.game.player.rect().centery
        

        if abs(disx) <2000 and abs(disy)<2000:
            pygame.draw.rect(surf, (128, 128, 128), (self.recttuongtac().x-offset[0]+25,self.recttuongtac().y-offset[1]-50, bar_width, bar_height))
            pygame.draw.rect(surf, (255,0,0), (self.recttuongtac().x-offset[0]+25,self.recttuongtac().y-offset[1]-50, fill_width, bar_height))
        
        
    