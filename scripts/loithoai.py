import math
import random

import pygame

from scripts.particle import Particle
from scripts.spark import Spark
from scripts.entities import PhysicsEntity


class Loithoai:
    def __init__(self,surf):
        self.animation = surf.assets['loithoainpc'].copy() #'player/idle'
    def update(self):
        self.animation.update()
    def render(self,surf):
        
         #'player/idle'
        surf.blit(self.animation.img(), (0,400))
        
    
        
   
        
    