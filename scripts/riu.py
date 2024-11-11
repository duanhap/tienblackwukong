import math
import random

import pygame

from scripts.particle import Particle
from scripts.spark import Spark
from scripts.entities import PhysicsEntity
from scripts.loithoai import Loithoai
class RiuThan(PhysicsEntity):
    def __init__(self, game, pos, size,quay= False):
        super().__init__(game, 'riuthan', pos, size)
        self.attacking = False
        self.walking = 0
        self.dan=''
        self.tontai =0
        self.flip = not quay
        self.air_time=0
     
        
    def update(self, tilemap, movement=(0, 0)):
        self.velocity[1]=15
        self.tontai+=1
        if self.tontai>300:
            for i in range(30):
                angle = random.random() * math.pi * 2
                speed = random.random() * 10
                self.game.sparks.append(Spark(self.recttuongtac().center, angle, 10 + random.random()))
                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
            self.game.sparks.append(Spark(self.rect().center, 0,15 + random.random()))
            self.game.sparks.append(Spark(self.rect().center, math.pi, 15 + random.random()))
            self.game.sfx['boom'].play()
            return True
        
        
       
       

        
            
         
            
            
           
        #elif random.random() < 0.01:
          #  self.walking = random.randint(30, 120)
        
        super().update(tilemap, movement=movement)
      
        self.attacking = True
        if movement[0] != 0:
            self.set_action('idle')
        else:
            self.set_action('idle')
        if self.flip:
            self.anim_offset=(-250,0)
   
            
        
   
        
    