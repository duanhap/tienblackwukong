import math
import random

import pygame

from scripts.particle import Particle
from scripts.spark import Spark
from scripts.entities import PhysicsEntity


class Loithoai:
    def __init__(self,surf,type):
        self.type = type
        if type=='npc':
            self.animation = surf.assets['loithoainpc'].copy() #'player/idle'
        elif type=='bosschim':
            self.animation = surf.assets['loithoaichim'].copy() #'player/idle'   
    def update(self):
        self.animation.update()
    def render(self,surf,pos):
        
         #'player/idle'
        surf.blit(self.animation.img(), pos)
        
    
        
   
        
    