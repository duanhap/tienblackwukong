import math
import random

import pygame

from scripts.particle import Particle
from scripts.spark import Spark
from scripts.entities import PhysicsEntity
class TruBatGioi(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'trubatgioi', pos, size)
        self.attacking = False
        self.walking = 0
        self.dan=''
        
    def update(self, tilemap, movement=(0, 0)):
        if self.walking:# xử lý đi trên vùng ok , chạm trái phải thì lật
            if tilemap.solid_check((self.rect().centerx + (-20 if self.flip else 20), self.rect().centery+25)):
                if (self.collision['right'] or self.collision['left']):
                    self.flip = not self.flip
                    
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)

            if not self.walking:
                #kc giữa pl và en
                dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
                #kc Y <16
                if (abs(dis[1]) < 200):
                    # đang quay trái bắn trái nếu gặp
                    self.attacking = True
                    self.set_action('attack')
           
        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)
        
        super().update(tilemap, movement=movement)
        if not self.attacking:
            if movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')
        if self.action=='attack':

            if self.animation.done:
                self.attacking = False
                self.can_move = True
       
    
            
        
    