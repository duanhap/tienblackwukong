import math
import random

import pygame

from scripts.particle import Particle
from scripts.spark import Spark
from scripts.riu import RiuThan
from scripts.entities import PhysicsEntity
class BossAnhLiems(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'nhilangthan', pos, size)
        self.walking = 0
        self.dan='kiem'
        self.banchua= False
        self.chuanbixong = True
        self.attacking = False
        self.hp =100
        self.hp_max = 100
        self.dead = False
        self.air_time =0
        self.chuanbixong = False
        self.targets = [] 

        self.blocking = False
        self.dangdungchieukhac = False

        self.khungAttackx =-500
        self.khungAttackxx =0
        self.kichthuocAttack=100
        
    def update(self, tilemap, movement=(0, 0)):
        #print(f'{self.action}walkinh {self.walking}  attacking {self.attacking}  bi danh: {self.bidanh} canmove: {self.can_move} dang dung chieu khac { self.dangdungchieukhac} flip {self.flip}' )
        dis_main9 = self.game.player.rect().centerx - self.rect().centerx
        if not self.dead:
            if self.walking:# xử lý đi trên vùng ok , chạm trái phải thì lật
                if tilemap.solid_check((self.rect().centerx + (-20 if self.flip else 20), self.rect().centery+25)):
                    if (self.collision['right'] or self.collision['left']) and not self.attacking and not self.bidanh and not self.blocking:
                        self.flip = not self.flip
                        
                    else:
                        movement = (movement[0] - 0.9 if self.flip else 0.9, movement[1])
                else:
                    self.flip = not self.flip
                self.walking = max(0, self.walking - 1)

                if not self.walking  and self.hp>0 and self.dead== False:
                                

                    # Cập nhật danh sách các vị trí mục tiêu
                    self.targets = [self.game.player.recttuongtac()] + [clone.recttuongtac() for clone in self.game.phanthans]
                    
                    # Tìm mục tiêu gần nhất
                    closest_target = min(self.targets, key=lambda t: math.hypot(t.centerx - self.rect().centerx, t.centery - self.rect().centery))
                    
                    # Tính khoảng cách đến mục tiêu gần nhất
                    dis_x = closest_target.centerx - self.rect().centerx
                    dis_y = closest_target.centery - self.rect().centery
                    dis = (dis_x, dis_y)
                
                    #kc giữa pl và en
                    dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
                    #kc Y <16
                    if (abs(dis[1]) < 500) and abs(dis[0])<1000:
                        # đang quay trái bắn trái nếu gặp
                        chieu = random.randint(0,7)
                        #chieu = 2
                        if chieu ==0 and not self.dangdungchieukhac:
                            if (self.flip and dis[0] < 0) and not self.dangdungchieukhac:
                                self.attacking = True
                                self.dangdungchieukhac = True
                                self.set_action('phikiem')
                                self.banchua = False                                            
                            if (not self.flip and dis[0] > 0) and not self.dangdungchieukhac:
                                self.attacking = True
                                self.dangdungchieukhac = True
                                self.set_action('phikiem')
                                self.banchua = False 
                        if chieu ==1 and not self.dangdungchieukhac:
                            if (self.flip and dis[0] < 0):
                                self.attacking = True
                                self.dangdungchieukhac = True
                                if  random.randint(0, 1) == 0:
                                    self.set_action('laodenattack')
                                else:
                                    self.set_action('laodenattack2')
                                                                    
                            if (not self.flip and dis[0] > 0):
                                self.attacking = True
                                self.dangdungchieukhac = True
                                if  random.randint(0, 1) == 0:
                                    self.set_action('laodenattack')
                                else:
                                    self.set_action('laodenattack2')
                        if chieu ==2 and  not self.dangdungchieukhac:
                            
                    
                            if (self.flip and dis[0] < 0):
                                self.attacking = True
                                self.dangdungchieukhac = True
                            
                                self.set_action('luot')
                                                                        
                            if (not self.flip and dis[0] > 0):
                                self.attacking = True
                                self.dangdungchieukhac = True
                                
                                self.set_action('luot')
                        if chieu == 3 and not self.dangdungchieukhac:       
                
                            if (self.flip and dis[0] < 0):
                                self.attacking = True
                                self.dangdungchieukhac = True
                                self.set_action('nemriu')
                                                                        
                            if (not self.flip and dis[0] > 0):
                                self.attacking = True
                                self.dangdungchieukhac = True
                                self.set_action('nemriu')
                        if chieu ==4 and  not self.dangdungchieukhac:
                            if (self.flip and dis[0] < 0):
                                self.attacking = True
                                self.dangdungchieukhac = True
                                self.set_action('tialazemax')
                                                                        
                            if (not self.flip and dis[0] > 0):
                                self.attacking = True
                                self.dangdungchieukhac = True
                                self.set_action('tialazemax')
                        if chieu ==5 and not self.dangdungchieukhac:
                            if (self.flip and dis[0] < 0):
                                self.attacking = True
                                self.dangdungchieukhac = True
                                
                                self.set_action('combogan')
                                                                    
                            if (not self.flip and dis[0] > 0):
                                self.attacking = True
                                self.dangdungchieukhac = True
                                
                                self.set_action('combogan')
                        if chieu == 6 and not self.dangdungchieukhac:
                            if (self.flip and dis[0] < 0):
                                    self.attacking = True
                                    self.dangdungchieukhac = True
                                    
                                    self.set_action('xoay')
                                
                                                                        
                            if (not self.flip and dis[0] > 0):
                                    self.attacking = True
                                    self.dangdungchieukhac = True
                                    
                                    self.set_action('xoay')
                        if chieu == 7 and not self.dangdungchieukhac:
                            if (self.flip and dis[0] < 0):
                                    self.attacking = True
                                    self.dangdungchieukhac = True
                                    
                                    self.set_action('tialazegan')
                                
                                                                        
                            if (not self.flip and dis[0] > 0):
                                    self.attacking = True
                                    self.dangdungchieukhac = True
                                    
                                    self.set_action('tialazegan')
                                
                            
                    
                
                        
                
            
            elif  random.randint(0,100)<50 :
                        self.walking = random.randint(30, 120)
                        # người chs đến gần thì dí
                        
                        
                        if   abs(dis_main9)<350 and self.action!='tialazemax' and self.action!='luot':
                                if self.flip and dis_main9>30:                          
                                    self.flip = False
                                if self.flip == False and dis_main9<-30:
                                                                         
                                    self.flip = True 
            super().update(tilemap, movement=movement)
            #hãm phanh
            if self.velocity[0] > 0:
                self.velocity[0] = max(self.velocity[0] - 0.1, 0)
            else:
                self.velocity[0] = min(self.velocity[0] + 0.1, 0)
            if self.bidanh or self.attacking or self.blocking:                        
                            if self.collision['right']:  
                                self.flip = True   
                                self.pos[0]-=100
                                
                                
                            elif  self.collision['left']  :
                                self.flip = False                            
                                self.pos[0]+=100
                                
                                    
                            
            if not self.attacking and not self.bidanh and not self.blocking:
                                            
                                            if movement[0] != 0:
                                                self.set_action('walk')
                                                self.rectTuongTacEdit=(58,77,50,80)
                                            else:
                                                self.set_action('idle')
                                                self.rectTuongTacEdit=(58,77,50,80)
            if self.action =='nemriu':
                                    self.rectTuongTacEdit=(58,0,0,80)
                                    self.bidanh = False

                                    
                                    self.rectAttack=(-500,60,0,0,1000)
                                                    
                                    self.bidanh= False
                                    self.blocking = False
                                
                                    if self.animation.done:
                                        self.game.enemies.append(RiuThan(self.game, [self.game.player.pos[0]-100,self.game.player.pos[1]-900], (75, 100),self.flip))

                                        self.attacking = False 
                                        self.can_move= True
                                        
                                        self.dangdungchieukhac = False
            if self.action == 'phikiem':
                self.rectTuongTacEdit=(58,0,0,80)
                self.bidanh = False

                self.animation.framecuoi[0]= self.animation.img_duration *7+1
                self.rectAttack=(10,-150,130,300,55) 
                self.bidanh= False
                self.blocking = False
                if self.animation.doneToDoSomething and not self.banchua:
                        if self.flip:
                                for i in range(random.randint(15,25)):
                                    self.game.projectiles.append([[self.rect().centerx - 120, self.rect().centery-random.randint(10,300)], -random.randint(9,20), 0,'kiem2'])
                                for i in range(10):
                                    self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5 + math.pi, 5 + random.random()))
                                    self.game.sparks.append(Spark((self.rect().centerx - 120, self.rect().centery-random.randint(10,150)), random.random() - 0.5 + math.pi, 5 + random.random()))

                                self.banchua = True   
                        else:
                                for i in range(random.randint(15,25)):
                                    self.game.projectiles.append([[self.rect().centerx +120, self.rect().centery-random.randint(10,300)], random.randint(9,20), 0,'kiem1'])
                                for i in range(10):
                                    self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5, 5 + random.random()))
                                    self.game.sparks.append(Spark((self.rect().centerx +120, self.rect().centery-random.randint(10,150)), random.random() - 0.5, 5 + random.random()))

                                self.banchua = True
                if self.animation.done:
                    
                    
                    self.attacking = False 
                    self.can_move= True
                    self.dangdungchieukhac = False
                    
            if self.action =='tialazemax':
                                    self.rectTuongTacEdit=(58,0,0,80)
                                    self.bidanh = False 
                                    self.animation.framecuoi[0]= self.animation.img_duration *58+1
                                    self.animation.framecuoi[1]= self.animation.img_duration *3+1
                                    self.rectAttack=(self.khungAttackx,60,self.kichthuocAttack,100,self.khungAttackxx)
                                    #1100
                                
                                        
                                    self.bidanh= False
                                    self.blocking = False
                                    if not self.flip:
                                        if self.animation.frame>= self.animation.img_duration*17+1 and self.animation.frame<=self.animation.img_duration*24:
                                            self.khungAttackx+=20 
                                        if self.animation.frame>= self.animation.img_duration*25+1 and self.animation.frame<=self.animation.img_duration*52:
                                            self.khungAttackx-=25
                                    else:
                                        if self.animation.frame>= self.animation.img_duration*17+1 and self.animation.frame<=self.animation.img_duration*24:
                                            self.khungAttackxx+=20 
                                        if self.animation.frame>= self.animation.img_duration*25+1 and self.animation.frame<=self.animation.img_duration*52:
                                            self.khungAttackxx-=25
                                    if self.animation.frame>= self.animation.img_duration*47+1 and self.animation.frame<=self.animation.img_duration*49:
                                        self.rectAttack=(-500,60,1100,80,1000)
                                    if self.animation.frame>= self.animation.img_duration*60+1 and self.animation.frame<=self.animation.img_duration*62:
                                        self.rectAttack=(-500,60,1100,80,1000)
                                    if self.animation.done:
                                        self.attacking = False 
                                        self.can_move= True
                                        self.khungAttackx=-500
                                        self.khungAttackxx=0
                                        self.dangdungchieukhac = False
                                        
        #17(+1) 24
        #24(+1) 32
            if self.action =='luot':
                self.bidanh = False
                self.animation.framecuoi[0]= self.animation.img_duration *69+1
                self.animation.framecuoi[1]= self.animation.img_duration *3+1
                
                if self.flip:
                    if self.animation.doneToDoSomething:
                      
                        self.pos[0]-=15
                        
                    else:
                        self.pos[0]-=5          
                    self.rectTuongTacEdit=(-8,-100,50,80)     
                    self.rectAttack=(-40,-25,130,175,80) 
                else:
                    if self.animation.doneToDoSomething:
                        
                        self.pos[0]+=15
                    else:
                        self.pos[0]+=5
                    self.rectTuongTacEdit=(138,-100,50,80)     
                    self.rectAttack=(-40,-25,130,175,80) 
                if self.animation.done:
                    self.rectTuongTacEdit=(58,77,50,80)
                    self.attacking = False 
                    self.can_move= True
                    self.dangdungchieukhac = False

            if self.action =='laodenattack':
                self.bidanh = False
                self.animation.framecuoi[0]= self.animation.img_duration *7+1
                self.animation.framecuoi[1]= self.animation.img_duration *2+1
                
                if self.flip:
                    if self.animation.doneToDoSomething:
                        self.pos[0]-=15                  
                    self.rectAttack=(100,55,200,100,80) 
                else:
                    if self.animation.doneToDoSomething:
                        self.pos[0]+=15    
                    self.rectAttack=(20,55,200,100,-80) 
                if self.animation.done:
                    self.rectTuongTacEdit=(58,77,50,80)
                    self.attacking = False 
                    self.can_move= True
                    self.dangdungchieukhac = False
            
            if self.action =='laodenattack2':
                self.bidanh = False
                self.animation.framecuoi[0]= self.animation.img_duration *7+1
                self.animation.framecuoi[1]= self.animation.img_duration *2+1
                
                if self.flip:
                    if self.animation.doneToDoSomething:
                        self.pos[0]-=15                  
                    self.rectAttack=(100,55,200,100,80) 
                else:
                    if self.animation.doneToDoSomething:
                        self.pos[0]+=15    
                    self.rectAttack=(20,55,200,100,-80) 
                if self.animation.done:
                    self.rectTuongTacEdit=(58,77,50,80)
                    self.attacking = False 
                    self.can_move= True
                    self.dangdungchieukhac = False
            if self.action =='xoay':
                self.animation.framecuoi[0]= self.animation.img_duration *9+1
                self.animation.framecuoi[1]= self.animation.img_duration *2+1
                if not self.flip:
                    if self.animation.frame>= self.animation.img_duration*3+1 and self.animation.frame<=self.animation.img_duration*5:
                        self.pos[0]+=5
                        self.rectAttack=(50,55,150,100,-80) 
                    if self.animation.frame>= self.animation.img_duration*7+1 and self.animation.frame<=self.animation.img_duration*9:
                        self.pos[0]-=5
                        self.rectAttack=(-200,55,150,100,-80) 
                    if self.animation.frame>= self.animation.img_duration*9+1 and self.animation.frame<=self.animation.img_duration*10:
                        self.pos[0]+=3
                        
                        self.rectAttack=(50,55,100,100,-80)
                else:
                    if self.animation.frame>= self.animation.img_duration*3+1 and self.animation.frame<=self.animation.img_duration*5:
                        self.pos[0]-=5
                        self.rectAttack=(100,55,150,100,40) 
                    if self.animation.frame>= self.animation.img_duration*7+1 and self.animation.frame<=self.animation.img_duration*9:
                        self.pos[0]+=5
                        self.rectAttack=(100,55,150,100,-200) 
                    if self.animation.frame>= self.animation.img_duration*9+1 and self.animation.frame<=self.animation.img_duration*10:
                        self.pos[0]-=3
                    
                        self.rectAttack=(100,55,100,100,10)
                
                if self.animation.done:
                    self.rectTuongTacEdit=(58,77,50,80)
                    self.attacking = False 
                    self.can_move= True
                    self.dangdungchieukhac = False
            if self.action =='combogan':
                self.bidanh = False
                self.animation.framecuoi[0]= self.animation.img_duration *20+1
                self.animation.framecuoi[1]= self.animation.img_duration *3+1
                if not self.flip:
                    if self.animation.frame>= self.animation.img_duration*4+1 and self.animation.frame<=self.animation.img_duration*6:
                        self.pos[0]+=5
                        self.rectAttack=(20,55,150,100,-80) 
                    if self.animation.frame>= self.animation.img_duration*10+1 and self.animation.frame<=self.animation.img_duration*12:
                        self.pos[0]+=5
                        self.rectAttack=(20,55,150,100,-80) 
                    if self.animation.frame>= self.animation.img_duration*17+1 and self.animation.frame<=self.animation.img_duration*22:
                        self.pos[0]+=5
                        if self.animation.frame>= self.animation.img_duration*17+1 and self.animation.frame<=self.animation.img_duration*20:
                            self.rectAttack=(100,55,0,0,20)
                        else:
                            self.rectAttack=(20,55,150,100,-80)
                else:
                    if self.animation.frame>= self.animation.img_duration*4+1 and self.animation.frame<=self.animation.img_duration*6:
                        self.pos[0]-=5
                        self.rectAttack=(100,55,150,100,20) 
                    if self.animation.frame>= self.animation.img_duration*10+1 and self.animation.frame<=self.animation.img_duration*12:
                        self.pos[0]-=5
                        self.rectAttack=(100,55,150,100,20) 
                    if self.animation.frame>= self.animation.img_duration*17+1 and self.animation.frame<=self.animation.img_duration*22:
                        self.pos[0]-=5
                        if self.animation.frame>= self.animation.img_duration*17+1 and self.animation.frame<=self.animation.img_duration*20:
                            self.rectAttack=(100,55,0,0,20)
                        else :
                            self.rectAttack=(100,55,150,100,20)
                            



            
                if self.animation.done:
                    self.rectTuongTacEdit=(58,77,50,80)
                    self.attacking = False 
                    self.can_move= True
                    self.dangdungchieukhac = False
            if self.action =='tialazegan':
                self.bidanh = False
                if self.flip:
                    self.pos[0]-=3
                else:
                    self.pos[0]+=3
                self.animation.framecuoi[0]= self.animation.img_duration *9+1
                self.animation.framecuoi[1]= self.animation.img_duration *8+1
                self.rectAttack=(300,55,150,100,150)



            
                if self.animation.done:
                    self.rectTuongTacEdit=(58,77,50,80)
                    self.attacking = False 
                    self.can_move= True
                    self.dangdungchieukhac = False
            if self.game.player.attacking:
                if self.game.player.animation.doneToDoSomething:
                    if self.recttuongtac().colliderect(self.game.player.rectattack()):
                                
                            if not self.blocking:
                                        
                                if self.hp <=0:
                                    self.set_action('die')
                                else:                            
                                    self.set_action('hurt')
                                    
                                    
            for phanthan in self.game.phanthans:
                if phanthan.animation.doneToDoSomething:
                        if self.recttuongtac().colliderect(phanthan.rectattack()):
                                            
                                if not self.blocking:
                                                
                                        if self.hp <=0:
                                            self.set_action('die')
                                        else:                 
                                            self.set_action('hurt')
        if self.action == 'hurt' :
            self.bidanh = True
            
            if self.game.player.flip == False:
                self.pos[0] +=random.randint(1,5)
                
            else:
                self.pos[0] -=random.randint(1,3)

            if self.attacking:
               self.attacking = False
               self.dangdungchieukhac = False
            self.can_move = False
            if self.animation.done:
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
    def render(self, surf, offset=(0, 0)):
        if self.action == 'phikiem' or self.action == 'laodenattack' or self.action == 'laodenattack2'or self.action =='tialazegan':
            self.anim_offset=(-460,-170)
        elif self.action =='tialazemax' or self.action =='nemriu'or self.action=='die':
            self.anim_offset=(-800,-1100) 
        elif self.action =='luot' :
            if self.flip:
                self.anim_offset=(-550,-170)   
            else:
                self.anim_offset=(-350,-170)
                  
        elif self.action == 'xoay' or self.action == 'combogan':
            self.anim_offset=(-120,-190)
        else:
            self.anim_offset=(0,0)
        
            
          
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
    
        
    