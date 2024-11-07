import math
import random

import pygame
from scripts.tilemap import Tilemap
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



        self.chieudaikhungatack=100
        self.vitridaukhungattacknotflip=530
        
    def update(self, tilemap, movement=(0, 0)):
        disx1 = self.rect().centerx -self.game.player.rect().centerx
        disy1 = self.rect().centery -self.game.player.recttuongtac().centery
        # check chạm tường thì bị nảy lại
                      
                        
        
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
                            self.targets = [self.game.player.recttuongtac()] + [clone.recttuongtac() for clone in self.game.phanthans]
                            
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
                            
                            elif (abs(dis[0])<400 and abs(dis[0])>=50 ):
                                if abs(dis[1])<100:
                                    if self.hp>10:
                                        if (self.flip and dis[0] < 0):
                                                self.attacking = True
                                                self.set_action('attackgan')
                                                
                                            
                                        if (not self.flip and dis[0] > 0):
                                            self.attacking = True
                                            self.set_action('attackgan')
                                   
                                elif abs(dis[1])<1500:
                                    if (self.flip and dis[0] < 0):
                                            self.attacking = True
                                            self.set_action('banlazecao')
                                            
                                        
                                    if (not self.flip and dis[0] > 0):
                                        self.attacking = True
                                        self.set_action('banlazecao')
                                    
                                
                            elif (abs(dis[0])<=1000 and abs(dis[0])>=50 and abs(dis[1])<1200):
                                if self.hp>200:
                                     
                                    if (self.flip and dis[0] < 0):
                                            self.attacking = True
                                            self.set_action('attackchocxa')
                                            
                                        
                                    if (not self.flip and dis[0] > 0):
                                        self.attacking = True
                                        self.set_action('attackchocxa')
                                else:
                                    if (self.flip and dis[0] < 0):
                                            self.attacking = True
                                            self.set_action('banlazethap')
                                            
                                        
                                    if (not self.flip and dis[0] > 0):
                                        self.attacking = True
                                        self.set_action('banlazethap')
                                     
                                    
                            
                                 
                            
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
                                    if abs(disy1)<100:
                                        self.set_action('attackgan')
                                    else:
                                        self.set_action('banlazecao')
                                else:
                                    self.attacking = True
                                    if abs(disy1)<100:
                                        self.set_action('attackgan')
                                    elif abs(disx1)<250:
                                        self.set_action('banlazecao')

                            else:
                                if self.flip:
                                    self.attacking = True
                                    if abs(disy1)<100:
                                        self.set_action('attackgan')
                                    elif abs(disx1)<250:
                                        self.set_action('banlazecao')
                                else:
                                    self.flip = False
                                    self.attacking = True
                                    if abs(disy1)<100:
                                        self.set_action('attackgan')
                                    elif abs(disx1)<250:
                                        self.set_action('banlazecao')

                            
                              
                       
                    if self.action =='attackchocxa':
                                self.animation.framecuoi[0]= self.animation.img_duration *14+1
                                self.animation.framecuoi[1]= self.animation.img_duration *3+1
                                self.rectAttack=(380,250,100,400,100)


                                self.bidanh= False
                                self.blocking = False
                                
                                if self.animation.done:
                                    self.attacking = False 
                                    self.can_move= True
                    if self.action =='banlazethap':
                                self.animation.framecuoi[0]= self.animation.img_duration *22+1
                                self.animation.framecuoi[1]= self.animation.img_duration *21.86+1
                                
                                self.rectAttack=(self.vitridaukhungattacknotflip,550,self.chieudaikhungatack,100,830) 
                                #800
                                #-170
                                
                                if self.chieudaikhungatack<=130:
                                    self.chieudaikhungatack +=0.5
                                    if not self.flip:
                                        self.vitridaukhungattacknotflip-=0.5
                                    else:
                                        self.vitridaukhungattacknotflip=-170
                                elif self.chieudaikhungatack<=800:
                                    self.chieudaikhungatack +=15
                                    if not self.flip:
                                        self.vitridaukhungattacknotflip-=15
                                    else:
                                        self.vitridaukhungattacknotflip=-170

                                self.bidanh= False
                                self.blocking = False
                                
                                if self.animation.done:
                                    self.attacking = False 
                                    self.can_move= True
                                    self.chieudaikhungatack=100
                                    self.vitridaukhungattacknotflip=530
                    if self.action =='banlazecao':
                                """
                                keys_to_remove = []

                                # Lặp qua các phần tử trong tilemap
                                for rect in tilemap.physics_rects_around([self.rectattack().centerx,self.rectattack().centery],1):
                                
                                    if self.rectattack().colliderect(rect):
                                        tile_loc = f"{int(rect.x // 50)};{int(rect.y // 50)}"
                                        keys_to_remove.append(tile_loc)
                                        print(tile_loc)  # Thêm key vào danh sách cần xóa

                                # Xóa các phần tử đã chọn khỏi tilemap
                                for loc in keys_to_remove:
                                    tilemap.remove(loc)
                                """                   
                                if self.flip == False:        
                                    self.pos[0] -=random.randint(-4,4)              
                                else:
                                    self.pos[0] +=random.randint(-4,4)
                                self.animation.framecuoi[0]= self.animation.img_duration *48+1
                                self.animation.framecuoi[1]= self.animation.img_duration *3+1
                                self.rectAttack=(0,210,450,80,450) 
                                self.bidanh= False
                                self.blocking = False
                                
                                if self.animation.done:
                                    self.attacking = False 
                                    self.can_move= True
                                    if self.flip and self.animation.doneToDoSomething:
                                        self.velocity[0]=-1.5
                                    else:
                                        self.velocity[0]=1.5
                                                    
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
                                                    if self.action !='banlazethap':
                                                        self.set_action('hurt')
                                                    else:
                                                        self.bidanh= True
                    for phanthan in self.game.phanthans:
                        if phanthan.animation.doneToDoSomething:
                                if self.recttuongtac().colliderect(phanthan.rectattack()):
                                                 
                                        if not self.blocking:
                                                       
                                                if self.hp <=0:
                                                    self.set_action('die')
                                                else:
                                                    self.hp-=0.02
                                                    if self.action !='banlazethap':
                                                        self.set_action('hurt')
                                                    else:
                                                        self.bidanh= True
                    if self.bidanh or self.attacking or self.blocking:                        
                        if self.collision['right']:     
                            self.pos[0]-=20
                        elif  self.collision['left']  :                           
                            self.pos[0]+=20               
                           
                

                    
                   

                                                     
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
                self.pos[0] -=random.randint(1,5)
                

            if self.attacking:
               self.attacking = False
            self.can_move = False
            if self.animation.done:
                if random.randint(0,10)<2 and self.hp>10:
                    self.blocking = True
                    self.set_action('block')
                else:
                    if self.game.player.flip:
                        if self.flip:
                            self.flip = False
                            self.attacking = True
                            if abs(disy1)<100:
                                
                                if self.hp<10:
                                    self.set_action('banlazethap')
                                else:
                                    self.set_action('attackgan')   
                            elif abs(disx1)<250:
                                self.set_action('banlazecao')
                        else:
                            self.attacking = True
                            if abs(disy1)<100:
                                if self.hp<10:
                                    self.set_action('banlazethap')
                                else:
                                    self.set_action('attackgan')
                            elif abs(disx1)<250:
                                self.set_action('banlazecao')

                    else:
                        if self.flip:
                            self.attacking = True
                            if abs(disy1)<100:
                                if self.hp<10:
                                    self.set_action('banlazethap')
                                else:
                                    self.set_action('attackgan')
                            elif abs(disx1)<250:
                                self.set_action('banlazecao')
                        else:
                            self.flip = False
                            self.attacking = True
                            if abs(disy1)<100:
                                if self.hp<10:
                                    self.set_action('banlazethap')
                                else:
                                    
                                    self.set_action('attackgan')
                            elif abs(disx1)<250:
                                self.set_action('banlazecao')

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
        if self.action == 'banlazethap':
            
            self.anim_offset=(-480,0)
            
          
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
        
        
    