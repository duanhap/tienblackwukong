from scripts.entities import PhysicsEntity
import math
import random

import pygame

from scripts.particle import Particle
from scripts.spark import Spark
from scripts.utils import load_image,load_images,Animation
from scripts.loithoai import Loithoai
class BossChim(PhysicsEntity):
    def __init__(self, game, pos, size,isMainBoss = True):
        super().__init__(game, 'bosschim', pos, size)
        
        self.walking = 0
        self.dan='nangluong'
        self.banchua= False
        self.chuanbixong = True
        self.hp =30
        self.hp_max = 30
        self.dead = False
        self.diplayer = False #dí player
        self.danhxa = False
        self.targets=[]
        self.air_time =0
        self.attacking = False
        self.mainBoss = isMainBoss
        self.soLanPhanthan=2
        self.loithoai =  Loithoai(self.game,'bosschim')
        self.demthoigiannoi =0


        self.posbandau = self.pos
        
        
        
        
    def update(self, tilemap, movement=(0, 0)):
            #print(self.pos[0],self.pos[1])
            if not self.dead  and (self.game.player.pos[0]>2850 and self.game.player.pos[0]<5490): #[5486, 430][2871, 480] : phạm vi di chuyển
                #loi noi
                disloinoi = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
       
                self.demthoigiannoi+=1
                if abs(disloinoi[0])<1500 and self.demthoigiannoi <300: 
                    self.loithoai.update()
                    if self.game.fullscreen:
                         self.loithoai.render(self.game.screen,(720,70))
                    else: self.loithoai.render(self.game.screen,(200,0))
                if self.demthoigiannoi >1200:
                    self.demthoigiannoi =0
                if random.randint(0,100)<5  and self.hp<= 13 and self.mainBoss==True and self.soLanPhanthan>0:
                     self.game.enemies.append(BossChim(self.game, self.pos, (75, 100),False))
                     self.game.enemies[len( self.game.enemies)-1].hp = 2
                     self.soLanPhanthan-=1
                     self.game.assets['bosschim/attackkiemchuanbi']= Animation(load_images('entities/bosschim/attackiemchuanbi',(400,400),(255,255,255)), img_dur=8,loop=False)
                     self.game.assets['bosschim/attackgan'] = Animation(load_images('entities/bosschim/attackgan',(400,400),(255,255,255)), img_dur=6,loop=False)


                self.air_time+=1
                if self.air_time>80 :
                    self.pos=self.posbandau
                    #3000,-100
                    
                    #self.game.player.hp=-10
                    #self.hp =-1
                    #self.set_action('die')
                if self.collision['down'] :
                    self.air_time =0
                
                if random.randint(0,100)<50 and self.attacking == False and self.bidanh == False and self.dead== False and self.diplayer == False :
                                dis_x = self.game.player.rect().centerx - self.rect().centerx
                                if dis_x <=0 and abs(dis_x)<2000:
                                        if not self.flip:
                                            
                                            for i in range(30):
                                                angle = random.random() * math.pi * 2
                                                speed = random.random() * 8
                                                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.3, math.sin(angle + math.pi) * speed * 0.3], frame=random.randint(0, 7)))
                                            self.pos[0]-=random.randint(5,10)
                                        else:
                                            for i in range(30):
                                                    angle = random.random() * math.pi *2 
                                                    speed = random.random() * 8 # độ dài tia
                                                    self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.3, math.sin(angle + math.pi) * speed *0.3], frame=random.randint(0, 7)))#0,3 0,2 độ chéo của êff
                                                
                                            self.pos[0]-=random.randint(5,10)
                                                                
                                else:     
                                        if not self.flip:
                                            
                                            for i in range(30):
                                                angle = random.random() * math.pi * 2
                                                speed = random.random() * 8
                                                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.3, math.sin(angle + math.pi) * speed * 0.3], frame=random.randint(0, 7)))
                                            self.pos[0]+=random.randint(5,10)
                                        else:
                                            for i in range(30):
                                                    angle = random.random() * math.pi * 2
                                                    speed = random.random() * 8 # độ dài tia
                                                    self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.3, math.sin(angle + math.pi) * speed *0.3], frame=random.randint(0, 7)))#0,3 0,2 độ chéo của êff
                                                
                                            self.pos[0]+=random.randint(5,10)
                
                # Tính toán khoảng cách đến người chơi
                # Cập nhật danh sách các vị trí mục tiêu
                self.targets = [self.game.player.rect()] + [clone.rect() for clone in self.game.phanthans]
                
                # Tìm mục tiêu gần nhất
                closest_target = min(self.targets, key=lambda t: math.hypot(t.centerx - self.rect().centerx, t.centery - self.rect().centery))
                
                # Tính khoảng cách đến mục tiêu gần nhất
                dis_x = closest_target.centerx - self.rect().centerx
                dis_y = closest_target.centery - self.rect().centery

                dis = (dis_x, dis_y)
                # Cập nhật hướng di chuyển theo người chơi
                if abs(dis_x+20) > 320  and self.attacking== False  and random.randint(0,100)<50 and abs(dis[1]<1500):
                    if abs(dis_x+20) < 500 and abs(dis_x+20) >120:  # Chỉ di chuyển khi khoảng cách phạm vi 400m vì là abs
                        self.diplayer = True
                        speed = min(0.9, max(0.5, abs(dis_x) / 100))
                        movement = (speed if dis_x > 0 else -speed, movement[1]) # di chuyển trái phải  theo ng chs
                        #if random.randint(0,100) >90:
                        
                            
                        self.flip = dis_x < 0  # Lật nhân vật nếu cần
                        
                    #if abs(dis_y) > 100:
                    # movement = (movement[0], -0.01)
                    else:
                      
                        self.diplayer = False
               
                if self.walking:# xử lý đi trên vùng ok , chạm trái phải thì lật
                    if tilemap.solid_check((self.rect().centerx + (-20 if self.flip else 20), self.rect().centery+25)):
                        if (self.collision['right'] or self.collision['left']):
                           
                            self.flip = not self.flip
                           
                            if (self.flip and dis[0] < 0):
                                        self.attacking = True
                                        self.set_action('attackkiemchuanbi')
                                        
                                        
                                        if self.animation.done:
                                            self.attacking = False
                                            
                                    

                            if (not self.flip and dis[0] > 0):
                                    self.attacking = True
                                    self.set_action('attackkiemchuanbi')
                                    
                                    
                                    if self.animation.done:
                                        self.attacking = False 
                            
                            
                        else:
                            movement = (movement[0] - 0.4 if self.flip else 0.4, movement[1])
                    #else:
                        #self.flip = not self.flip
                    self.walking = max(0, self.walking - 1)
                    if not self.walking   and self.hp>0 and self.dead== False:
                            #kc giữa pl và en
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
                            if abs(dis[0])<=150  and abs(dis[1]<150):
                                if (self.flip and dis[0] < 0):
                                    self.attacking = True
                                    self.set_action('attackgan')
                                    
                                
                                    

                                if (not self.flip and dis[0] > 0):
                                    self.attacking = True
                                    self.set_action('attackgan')
                                    
                            
                            elif (abs(dis[0])<=500 and abs(dis[1]<200)) and random.randint(0,50)<27:
                                if (self.flip and dis[0] < 0):
                                        self.attacking = True
                                        self.set_action('attackkiemchuanbi')
                                        
                                        
                                        if self.animation.done:
                                            self.attacking = False
                                            
                                    

                                if (not self.flip and dis[0] > 0):
                                    self.attacking = True
                                    self.set_action('attackkiemchuanbi')
                                    
                                    
                                    if self.animation.done:
                                        self.attacking = False 
                            if abs(dis[1])<150 and abs(dis[0])<=2000 and  random.randint(0,50)<20:
                                if (self.flip and dis[0] < 0):
                                    self.attacking = True
                                    self.danhxa = True
                                    self.set_action('attackgan')
                                    self.banchua = False
                                    if self.animation.done:
                                        self.attacking = False
                                            
                                    

                                if (not self.flip and dis[0] > 0):
                                    self.attacking = True
                                    self.danhxa = True
                                    self.set_action('attackgan')
                                    self.banchua = False
                                    if self.animation.done:
                                      self.attacking = False 
                            
                            if self.attacking:
                                if random.randint(0,100)<75:
                                    if self.flip and dis_x>30:
                                            
                                            self.pos[0]+=random.randint(15,20)
                                            self.flip = False
                                    if self.flip == False and dis_x<-30:
                                        
                                        self.pos[0]-=random.randint(15,20) 
                                        self.flip = True 
                                 
                elif random.randint(0,100)<68:
                        self.walking = random.randint(30, 120)
                        if random.randint(0,100)<50:
                            if self.flip and dis_x>30 and abs(dis_x)<500:
                                    
                                    self.pos[0]+=random.randint(15,20)
                                    self.flip = False
                            if self.flip == False and dis_x<-30 and  abs(dis_x)<500:
                                
                                self.pos[0]-=random.randint(15,20) 
                                self.flip = True 



              
                super().update(tilemap, movement=movement)

                if self.action =='attackgan' and not self.danhxa:
                    self.animation.framecuoi[0]= self.animation.img_duration *6+1
                    if self.animation.done:
                        self.game.screenshake = max(10,self.game.screenshake)
                        self.attacking = False 
                        self.can_move= True

                if self.action =='attackgan' and self.danhxa:
                    self.animation.framecuoi[0]= self.animation.img_duration *6+1
                    
                    if self.animation.doneToDoSomething  and not self.banchua:
                        self.game.screenshake = max(10,self.game.screenshake)
                        if self.flip:
                            for i in range(random.randint(1,4)):
                                self.game.projectiles.append([[self.rect().centerx - 120, self.rect().centery-random.randint(10,150)], -random.randint(9,15), 0,'kiemnangluong1'])
                            for i in range(4):
                                self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5 + math.pi, 5 + random.random()))
                            self.banchua = True   
                        else:
                            for i in range(random.randint(1,4)):
                                self.game.projectiles.append([[self.rect().centerx +120, self.rect().centery-random.randint(10,150)], random.randint(9,15), 0,'kiemnangluong2'])
                            for i in range(4):
                                self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5, 5 + random.random()))
                            self.banchua = True
                        self.danhxa = False    
                if self.action =='attackkiemchuanbi':

                # Cập nhật danh sách các vị trí mục tiêu
                    self.targets = [self.game.player.rect()] + [clone.rect() for clone in self.game.phanthans]
                    
                    # Tìm mục tiêu gần nhất
                    closest_target = min(self.targets, key=lambda t: math.hypot(t.centerx - self.rect().centerx, t.centery - self.rect().centery))
                    
                    # Tính khoảng cách đến mục tiêu gần nhất
                    dis_x = closest_target.centerx - self.rect().centerx
                    dis_y = closest_target.centery - self.rect().centery

                    dis = (dis_x, dis_y)
                    #dis = (self.game.player.rect().x - self.rect().x, self.game.player.rect().y - self.rect().y)

                    if self.animation.done:
                        self.game.screenshake = max(10,self.game.screenshake)
                        if self.flip:
                            
                            for i in range(30):
                                angle = random.random() * math.pi * 2
                                speed = random.random() * 13
                                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.3, math.sin(angle + math.pi) * speed * 0.3], frame=random.randint(0, 7)))
                            self.pos[0]-=min(400,(abs(dis[0])-60))
                            self.game.sfx['tocbienquai'].play()
                            self.set_action('attackkiem')
                            
                            self.animation.framecuoi[0]= self.animation.img_duration *9+1
                            self.animation.framecuoi[1]= self.animation.img_duration *1+1
                            self.banchua = False
                            if self.animation.done:
                                self.attacking = False

                        else:
                            for i in range(30):
                                    angle = random.random() * math.pi * 2
                                    speed = random.random() * 13 # độ dài tia
                                    self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.3, math.sin(angle + math.pi) * speed *0.3], frame=random.randint(0, 7)))#0,3 0,2 độ chéo của êff
                                
                            self.pos[0]+=min(400,(abs(dis[0])-60))
                            self.game.sfx['tocbienquai'].play()
                            self.set_action('attackkiem')
                            self.animation.framecuoi[0]= self.animation.img_duration *9+1
                            self.animation.framecuoi[1]= self.animation.img_duration *1+1
                            self.banchua = False
                            if self.animation.done:
                                self.attacking = False
                    
                    if abs(self.game.player.dashing) >30 :
                        if self.rectattack().colliderect(self.game.player.recttuongtac()) or  self.recttuongtac().colliderect(self.game.player.recttuongtac()) :
                            if self.game.player.flip:
                                
                                self.pos[0]+=random.randint(15,20)
                                self.flip = True
                            else:
                                
                                self.pos[0]-=random.randint(15,20) 
                                self.flip = False 
                    # đang đánh mà player nhảy ra phía sau
                    if random.randint(0,100)<50:
                        if self.flip and dis_x>30:
                                
                                self.pos[0]+=random.randint(15,20)
                                self.flip = False
                        if self.flip == False and dis_x<-30:
                            
                            self.pos[0]-=random.randint(15,20) 
                            self.flip = True 
                if self.bidanh:                        
                        if self.collision['right']:     
                            self.pos[0]-=15
                        elif  self.collision['left']  :                           
                            self.pos[0]+=15         
                # khiu khích chiến thắng
            if self.game.player.hp <=0:
                self.can_move = False
                
                self.set_action('win')
            if not self.attacking and not self.bidanh:
                if movement[0] != 0:
                        if self.diplayer:
                            self.set_action('tipcan')
                        else:
                            self.set_action('walk')
                else:
                        self.set_action('idle')

            for phanthan in self.game.phanthans:
                 if phanthan.animation.doneToDoSomething:
                        if self.recttuongtac().colliderect(phanthan.rectattack()):
                                if not self.bidanh: # ko bi danh trung , kiểu đnag bị đáng lại bị đánh
                                    self.bidanh =True
                                           
                                if self.hp ==0:
                                    self.set_action('die')
                                else :
                                    self.set_action('hurt')
                                    if self.hp <15:
                                        phanthan.pos[0] += random.randint(-10,10)
                                        phanthan.pos[1] -= random.randint(10,20)
                                        phanthan.set_action('hurt')


                                     
                                    
                                    
                
            if self.game.player.attacking:
                    if self.game.player.animation.doneToDoSomething:
                        if self.recttuongtac().colliderect(self.game.player.rectattack()):
                                if not self.bidanh: # ko bi danh trung , kiểu đnag bị đáng lại bị đánh
                                    self.bidanh =True
                                    
                                   
                                if self.hp ==0:
                                    self.set_action('die')
                                else :
                                    self.set_action('hurt')
                                
                                
                                    
                                         
            #hãm phanh
            if self.velocity[0] > 0:
                self.velocity[0] = max(self.velocity[0] - 0.1, 0)
            else:
                self.velocity[0] = min(self.velocity[0] + 0.1, 0)
                                        
            if self.action == 'hurt':
                self.game.sfx['bidanh'].play()
                self.game.screenshake = max(5,self.game.screenshake)
                if self.game.player.flip == False:
                        if not self.flip:
                            self.velocity[0]=-10
                            
                            for i in range(30):
                                angle = random.random() * math.pi * 2
                                speed = random.random() * 13
                                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.3, math.sin(angle + math.pi) * speed * 0.3], frame=random.randint(0, 7)))
                            if self.game.player.attacking:    
                                self.pos[0]+=random.randint(5,28)
                            else:
                                self.pos[0]+=random.randint(8,15)
                        else:
                            self.velocity[0]=10
                            for i in range(30):
                                    angle = random.random() * math.pi * 2
                                    speed = random.random() * 13 # độ dài tia
                                    self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.3, math.sin(angle + math.pi) * speed *0.3], frame=random.randint(0, 7)))#0,3 0,2 độ chéo của êff
                                
                            self.pos[0]+=random.randint(3,5)
                                                
                else:
                    
                    
                        if not self.flip:
                            self.velocity[0]=-10
                            
                            for i in range(30):
                                angle = random.random() * math.pi * 2
                                speed = random.random() * 13
                                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.3, math.sin(angle + math.pi) * speed * 0.3], frame=random.randint(0, 7)))
                            self.pos[0]-=random.randint(3,5)
                        else:
                            self.velocity[0]=10
                            for i in range(30):
                                    angle = random.random() * math.pi * 2
                                    speed = random.random() * 13 # độ dài tia
                                    self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.3, math.sin(angle + math.pi) * speed *0.3], frame=random.randint(0, 7)))#0,3 0,2 độ chéo của êff
                                
                            if self.game.player.attacking:    
                                self.pos[0]-=random.randint(5,28)
                            else:
                                self.pos[0]-=random.randint(8,15)
                            
                    
                    
                if self.attacking:
                    self.attacking = False
                self.can_move = False
                if self.animation.done:
                    self.attacking = True
                    
                    if self.game.player.flip == False :
                        if not self.flip:
                            self.flip = True
                            self.pos[0]+=random.randint(8,10)
                            if random.randint(0,49)<24:
                                self.set_action('attackkiemchuanbi')

                            else:
                                    self.set_action('attackgan')
                                    self.game.screenshake = max(5,self.game.screenshake)
                            
                        else:
                            self.pos[0]+=random.randint(8,10)
                            if random.randint(0,49)<24:
                                self.set_action('attackkiemchuanbi')
                            else:
                                    self.set_action('attackgan')
                                    self.game.screenshake = max(5,self.game.screenshake)
                    else:
                        if  self.flip:
                            self.flip = False
                            self.pos[0]+=random.randint(8,10)
                            if random.randint(0,49)<24:
                                self.set_action('attackkiemchuanbi')
                            else:
                                    self.set_action('attackgan')
                                    self.game.screenshake = max(5,self.game.screenshake)
                            
                        else:
                            self.pos[0]+=random.randint(8,10)
                            if random.randint(0,49)<24:
                                self.set_action('attackkiemchuanbi')
                            else:
                                if random.randint(0,50)<24:
                                     self.danhxa = True  
                                self.set_action('attackgan')
                                self.game.screenshake = max(5,self.game.screenshake)
                                    
                                 
                         
                   
                    self.hp-=1
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
            

   
            
        
    