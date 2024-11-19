import math
import random

import pygame

from scripts.particle import Particle
from scripts.spark import Spark
from scripts.entities import PhysicsEntity
class Player(PhysicsEntity):
    def __init__(self,game,pos,size):
        super().__init__(game,'player',pos,size)
        self.air_time =0  # thời gian ở trong không trung không tiếp đất
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
        
        self.binhhpmax=3
        self.binhhp=3
        self.noitai =0
        self.noitai_max=10
        self.attack_thu_may=1

        self.tichnoitai=False
        self.dieukiendanhnoitai=0


        self.xuathien = False
        self.timexuathien =0
        self.xuathienomap1=1
        self.duochealing = False
        self.imagehiuunng = self.game.assets['trubatgioi/healed'].copy()

    def update(self,tilemap,movement=(0,0)):
        super().update(tilemap, movement=movement)
        self.stamina= min(10,self.stamina+0.032)
        if self.game.level ==1 and self.xuathienomap1 :
            self.xuathien = True
        if self.xuathien ==True:
            self.timexuathien+=1
           # self.can_move = False
            if self.timexuathien<450 and self.timexuathien>250:
                movement = [True,False]
                self.pos[0]+=2
               
            elif self.timexuathien>450:
                self.can_move = True
                self.xuathien =False
                self.xuathienomap1=0
                movement = [False,False]
        
        #diu kien danh noi tai
        if self.tichnoitai:
            self.dieukiendanhnoitai+=10
        if self.noitai>=10 and self.dieukiendanhnoitai>120:

            self.attack_thu_may=4
            
        #va cham với enemy
        for enemycon in self.game.enemies:
            if self.recttuongtac().colliderect(enemycon.rectattack()):
                if enemycon.attacking and abs(self.dashing) <50 and enemycon.animation.doneToDoSomething :
                    if  not self.blocking:                      
                        self.game.sfx['boom'].play() 
                        if random.randint(0,100)<15:             
                            if self.flip == False:
                                self.pos[0] +=5.5
                                self.pos[1] -=10                           
                            else:
                                self.pos[0] -=5.5 
                                self.pos[1] -=10                    
                        self.hp-=0.1
                        #self.game.sfx['bidanh'].play()
                        
                    else:
                        self.game.sfx['chamvukhi'].play()
                        
                        if self.stamina<1:
                            self.hp-=0.005
                        else:
                            self.stamina-=0.01*random.randint(5,20)

                        if enemycon.type =='bosschim':
                            self.game.screenshake = max(random.randint(10,15),self.game.screenshake)
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
                            self.game.screenshake = max(8,self.game.screenshake)
                    
        if self.attacking:
                   
            if self.attack_thu_may==1:
                self.set_action('attack')
                self.game.sfx['wukongvoicechieudai'].play()
                self.animation.framecuoi[0]= self.animation.img_duration *5+1
                self.animation.framecuoi[1]= self.animation.img_duration *3+1
                self.anim_offset=(-260,-388)
                self.rectTuongTacEdit=(23,50,50,64)     
                self.rectAttack=(60,50,130,80,55)
                if self.flip and self.animation.doneToDoSomething:
                            self.velocity[0]=-1.5
                else:
                            self.velocity[0]=1.5   
                
            elif self.attack_thu_may==2:
                self.set_action('attack2')
                self.game.sfx['wukongvoicechieudai'].play()
                self.animation.framecuoi[0]= self.animation.img_duration *5+1
                self.animation.framecuoi[1]= self.animation.img_duration *3+1
                self.anim_offset=(-260,-388)
                self.rectTuongTacEdit=(23,50,50,64)     
                self.rectAttack=(60,50,130,80,55)
                if self.flip and self.animation.doneToDoSomething:
                            self.velocity[0]=-1.5
                else:
                            self.velocity[0]=1.5   
            elif self.attack_thu_may==3:
                self.set_action('attack3')
                self.game.sfx['wukongvoicechieudai'].play()
                self.animation.framecuoi[0]= self.animation.img_duration *5+1
                self.animation.framecuoi[1]= self.animation.img_duration *3+1        
                self.anim_offset=(-90,-75)
                self.rectTuongTacEdit=(23,50,50,64)     
                self.rectAttack=(60,-55,130,175,55)
            elif self.attack_thu_may==4:
                self.set_action('attack4')
                
                self.rectTuongTacEdit=(23,-230,50,64)
                self.rectAttack=(10,-350,330,470,240)
                self.noitai=0
                
                self.animation.framecuoi[0]= self.animation.img_duration *7+1
                self.animation.framecuoi[1]= self.animation.img_duration *3+1
                self.anim_offset=(-240,-400)
                if self.animation.frame>105 and self.animation.frame<125:
                    self.game.screenshake = max(20,self.game.screenshake)           
            self.can_move = False
            if self.action=='attack4':
                
                if self.tichnoitai and self.animation.frame>40 and self.animation.frame<45 :
                    self.animation.ngatchieu = True
                    self.kickhoatdung=0
                    

                else:
                    self.animation.ngatchieu = False

            if self.animation.done:
                
                
                self.rectTuongTacEdit=(23,50,50,64)
                self.attack_thu_may=max(1,(self.attack_thu_may+1)%4)
                self.anim_offset=(0,0)
                if self.noitai>7:
                    self.noitai=10
                self.noitai+=3             
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
            if self.attack_thu_may==4:
                self.stamina-=4
        
            
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
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)
        if self.duochealing and self.action!='attack4':
            
            if self.flip:
                surf.blit(pygame.transform.flip(self.imagehiuunng.img(), True, False), (self.rect().centerx +160 - self.imagehiuunng.img().get_width() - offset[0], self.rect().centery-130- offset[1]))
            else:
                surf.blit(self.imagehiuunng.img(), (self.rect().centerx-150  - offset[0], self.rect().centery-130 - offset[1]))       
            self.imagehiuunng.update()
            
        

      