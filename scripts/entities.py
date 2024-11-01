
import math
import random

import pygame

from scripts.particle import Particle
from scripts.spark import Spark

class PhysicsEntity:
    def __init__(self,game,e_type,pos,size,anim_offset=(0,0)):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size 
        self.velocity=[0,0]
        self.flip = False
        self.bidanh = False# bị đánh
        self.attacking = False
        


        # tạo khung tương tác
        if self.type =='player':
            self.rectedit=(29,70,35,50)         # (x,y,chiều rộng, chiều cao) của khung
            self.rectTuongTacEdit=(23,50,50,64)     
            self.rectAttack=(60,-55,130,175,55)
            #  (cách cạnh rectphai của đối tượng ,y,chiều rộng ,chiều cao,cách cạnh rect trái của đối tượng)  
            # khi flip thì khung attack thay đổi nên cần 5 giá trị để xác định    
        elif self.type =='phanthan':
            self.rectedit=(29,70,35,50)
            self.rectTuongTacEdit=(23,50,50,64)     
            self.rectAttack=(60,-55,130,175,55)  
        elif self.type == 'enemy':
            self.rectedit=(19,52,35,50)
            self.rectTuongTacEdit=(19,50,35,50)
            self.rectAttack=(43,45,50,75,40) 
        elif self.type == 'cungthu':
            self.rectedit=(75,133,40,50)
            self.rectTuongTacEdit=(70,45,50,130)
            self.rectAttack=(70,45,50,75,-15)
        elif self.type == 'bosschim':
            self.rectedit=(170,255,50,50)
            self.rectTuongTacEdit=(165,100,70,200)
            self.rectAttack=(70,135,125,125,60)
        elif self.type == "nguoisoi":
            self.rectedit=(130,204,40,50)#  x,y,chieudai,chieu cao , 2 giá trị đằng sau này max chỉ đc 50 không là lỗi
            self.rectTuongTacEdit=(75,140,140,110) # khung tuong tac tương tự
            self.rectAttack=(15,80,120,130,100)
        elif self.type == "nguoisoido":
            self.rectedit=(130,204,40,50)#  x,y,chieudai,chieu cao , 2 giá trị đằng sau này max chỉ đc 50 không là lỗi
            self.rectTuongTacEdit=(75,140,140,110) # khung tuong tac tương tự
            self.rectAttack=(15,80,120,130,100)    # khung tấn công thì phải thêm 1 biến 
        elif self.type == 'npcsoi':
            self.rectedit=(130,189,35,50)
            self.rectTuongTacEdit=(19,50,35,50)
            self.rectAttack=(43,45,50,75,40) 
             

        self.collision = {'up':False,'down':False,'right':False,'left':False}
        self.action=''
        self.anim_offset =anim_offset # sổ liệu để căn chỉnh khung tương tác cho mỗi animation 

       
        self.set_action('idle')
        self.frame_movement =(0,0) #dichuyen len xuong trai phai
        self.can_move = True
       
      

    #rect attack
    def rectattack(self,offset=(0,0)):
        if not self.flip:
            return pygame.Rect(self.rect().x+self.rectAttack[0] + -offset[0], self.pos[1]+self.rectAttack[1]-offset[1],self.rectAttack[2],self.rectAttack[3])  
        else:
            return pygame.Rect(self.rect().x -self.rectAttack[4] -self.rectAttack[0]-10-offset[0], self.pos[1]+self.rectAttack[1]-offset[1],self.rectAttack[2],self.rectAttack[3])  


    #rect tuong tac
    def recttuongtac(self,offset=(0,0)):
        
        return pygame.Rect(self.pos[0]+self.rectTuongTacEdit[0]-offset[0], self.pos[1]+self.rectTuongTacEdit[1]-offset[1],self.rectTuongTacEdit[2],self.rectTuongTacEdit[3])  
    

    #tao collison cho player xử lý va chạm 
    def rect(self,offset=(0,0)):
        
        return pygame.Rect(self.pos[0]+self.rectedit[0]-offset[0], self.pos[1]+self.rectedit[1]-offset[1],self.rectedit[2],self.rectedit[3])  
        
            

    #tao trang thai neu dang ở trong trạng thái nào mà lại thêm chuyển đôg mơi giống  thì không chuyển
    def set_action(self,action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type +'/'+ self.action].copy() #'player/idle'
            



    def update(self,tilemap,movement=(0,0)):
        self.collision = {'up':False,'down':False,'right':False,'left':False}

        if self.can_move:
            self.frame_movement = (movement[0]+ self.velocity[0],movement[1]+ self.velocity[1])
        else:
            self.frame_movement = (0,movement[1]+ self.velocity[1])
        #di chuyen trai phai speed
        self.pos[0]+=self.frame_movement[0]*5
        #di chuyen len
        self.pos[1]+=self.frame_movement[1]*5

        #xử lý trạm 
        entity_rect = self.rect()
        pos_rect = [entity_rect.x,entity_rect.y]
        
       # Xử lý va chạm trục X
        #xử lý trạm 
        entity_rect = self.rect()
        pos_rect = [entity_rect.x,entity_rect.y]
        
        for rect in tilemap.physics_rects_around(pos_rect,1):
            if entity_rect.colliderect(rect)  :# tránh vc nhảy sang
                if self.frame_movement[0] > 0  :  # Di chuyển sang phải
                    entity_rect.right = rect.left
                    self.collision['right'] = True
                    self.pos[0] =  entity_rect.x - self.rectedit[0]
                elif self.frame_movement[0] <  0 :  # Di chuyển sang trái
                    entity_rect.left = rect.right
                    self.collision['left'] = True
                    self.pos[0] =  entity_rect.x - self.rectedit[0]
                # Cập nhật lại vị trí theo trục X
                
                

       

        # Xử lý va chạm trục Y
        entity_rect = self.rect()
        pos_rect = [entity_rect.x,entity_rect.y]
        for rect in tilemap.physics_rects_around(pos_rect,2):
            if entity_rect.colliderect(rect):
                if self.frame_movement[1] > 0 :  # Rơi xuống (di chuyển xuống dưới)
                    entity_rect.bottom = rect.top
                    self.collision['down'] = True
                    self.pos[1] = entity_rect.y - self.rectedit[1]
                elif self.frame_movement[1] < 0  and self.frame_movement[0]==0:  # Nhảy lên (di chuyển lên trên)
                    entity_rect.top = rect.bottom
                    self.collision['up'] = True
                    self.pos[1] = entity_rect.y - self.rectedit[1]

                # Cập nhật lại vị trí theo trục Y
                

        #flip       
        if movement[0]>0:
            self.flip = False
        if movement[0]<0:
            self.flip = True


        if self.attacking:        
            self.can_move = False
            if self.animation.done:  
             self.can_move = True
             self.attacking = False
        


        # Điều chỉnh vận tốc rơi    
        self.velocity[1] = min (11,self.velocity[1]+0.2 )# rơi cành nhanh đến 1 điểm nhất định
        
        if self.collision['down'] or self.collision['up']:
            self.velocity[1]=0
            self.frame_movement=(0,0)


        self.animation.update()


    # lấy ảnh
    def render(self,surf,offset=(0,0)):# off set đẻ nhận vật luôn ở vị trí trung tâm camera
        pygame.draw.rect(surf, (0, 0, 255), self.rectattack(offset), 2)  # Viền đỏ
        pygame.draw.rect(surf, (0, 255, 0), self.recttuongtac(offset), 2)  # Viền xanh lá
        pygame.draw.rect(surf, (255, 0, 0), self.rect(offset), 2)  # Viền đỏ
        surf.blit(pygame.transform.flip(self.animation.img(),self.flip,False),(self.pos[0]-offset[0]+self.anim_offset[0],self.pos[1]-offset[1]+self.anim_offset[1]))
                                             




