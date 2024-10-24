import math
import random

import pygame

from scripts.particle import Particle
from scripts.spark import Spark
from scripts.entities import PhysicsEntity
class Player(PhysicsEntity):
    def __init__(self,game,pos,size):
        super().__init__(game,'player',pos,size)
        self.air_time =0# thời gian ở trong không trung không tiếp đất
        self.jumps =1
        self.dashing = 0
        self.phanthaning= False
        self.blocking = False
        self.attacking = False
        self.bidanh = False
        self.dead = False
        self.mana_max = 10
        self.mana=10
        self.stamina_max=10
        self.stamina= 10
        self.hp_max =10
        self.hp=10
        self.mana=50
        self.stamina = 50
        self.binhhpmax=3
        self.binhhp=3

    def update(self,tilemap,movement=(0,0)):
        super().update(tilemap, movement=movement)
        self.stamina= min(10,self.stamina+0.022)

        #va cham với enemy
        for enemycon in self.game.enemies:
            if self.recttuongtac().colliderect(enemycon.rectattack()):
                if enemycon.attacking and abs(self.dashing) <50 and enemycon.animation.doneToDoSomething :
                    if  not self.blocking:                      
                        self.game.sfx['boom'].play()              
                        if self.flip == False:
                            self.pos[0] +=5.5
                            self.pos[1] -=15                           
                        else:
                            self.pos[0] -=5.5 
                            self.pos[1] -=15                    
                        self.hp-=0.1
                        #self.game.sfx['bidanh'].play()
                        
                    else:
                        self.game.sfx['chamvukhi'].play()
                        
                        if self.stamina<1:
                            self.hp-=0.005
                        else:
                            self.stamina-=0.01*random.randint(5,20)

                        if enemycon.type =='bosschim':
                            self.game.screenshake = max(random.randint(25,40),self.game.screenshake)
                            if random.randint(0,100)<40:
                                dis_x = enemycon.rectattack().centerx - self.recttuongtac().centerx
                                #dis_y = enemycon.rectattack().centery - self.recttuongtac().centery

                                if dis_x >30:
                                    self.pos[0] += random.randint(10,150)  # Giảm tốc độ dịch chuyển
                                    self.pos[1] -= random.randint(20, 100)  # Giảm độ ngẫu nhiên trục y cho mượt hơn
                                    
                                # Xử lý va chạm khi đạn từ phải qua trái
                                if dis_x <-30:
                                    self.pos[0] -= random.randint(10,150)  # Giảm tốc độ dịch chuyển
                                    self.pos[1] -= random.randint(20, 100)  # Giảm độ ngẫu nhiên trục y
                        else:
                            self.game.screenshake = max(16,self.game.screenshake)
                    
        if self.attacking:
            self.set_action('attack')
            self.game.sfx['wukongvoicechieudai'].play()
            self.animation.framecuoi[0]= self.animation.img_duration *5+1
            self.animation.framecuoi[1]= self.animation.img_duration *3+1
            self.anim_offset=(-90,-75)
            self.can_move = False
            if self.animation.done:
             self.anim_offset=(0,0)
             
             self.can_move = True
             self.attacking = False

        

        if self.attacking==False:

            if self.phanthaning:
                self.can_move = False
                self.set_action('phanthanskill')
            else:            
                self.air_time += 1
                if self.collision['down']:
                    self.air_time = 0
                    self.jumps = 2
                
                if self.blocking :
                    
                    self.attacking= False
                    self.can_move = False
                    self.set_action('block')
                else:
                    self.can_move = True
                    
        if self.can_move:
            if self.air_time > 4:
                        self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')

        if self.action=='phanthanskill':
            if self.animation.done:
                self.game.add_player()
                self.phanthaning = False
                self.can_move = True
                '''
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
                self.bidanh = False
                self.can_move = True
                '''
        #dash
        if abs(self.dashing) in {60, 50}:
            for i in range(20):
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 1
                pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                self.game.particles.append(Particle(self.game, 'particlewukong', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))                 
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)   
        if abs(self.dashing) >50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 7
            self.game.sfx['tocbien'].play()
            #self.velocity[1] = 0
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1 # hãm 
            pvelocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
            self.game.particles.append(Particle(self.game, 'particlewukong', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7))) 

        #hãm phanh
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

    def render(self, surf, offset=(0, 0)):
        if abs(self.dashing) <= 50:
            super().render(surf, offset=offset)
            
    def jump(self):
        
        if self.jumps and self.stamina>1.5:
            self.velocity[1]=-4
            self.jumps -= 1
            self.air_time = 5
            self.stamina-=1.5

    def attack(self):
       if not self.attacking and   not self.blocking and self.stamina>1:  # Chỉ bắt đầu tấn công nếu không đang tấn công
            self.attacking = True
            self.stamina-=1
            
    def dash(self):
        if  abs(self.dashing)==0 and not self.attacking and  not self.blocking and self.stamina>3.5:

            if self.flip:
                self.dashing = -60
                self.stamina-=3.5
            else:
                self.dashing = 60
                self.stamina-=3.5
    def skillphanthan(self):
        if not self.phanthaning and self.mana>2 :
            self.phanthaning = True
            
            
            
        

      