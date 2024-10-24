import math
import random

import pygame

from scripts.particle import Particle
from scripts.spark import Spark
from scripts.entities import PhysicsEntity
class Enemy(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)
        self.attacking = False
        self.walking = 0
        self.dan='projectile'
        
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
                if (abs(dis[1]) < 79):
                    # đang quay trái bắn trái nếu gặp
                    if (self.flip and dis[0] < 0):
                        self.game.projectiles.append([[self.rect().centerx - 45, self.rect().centery-15], -5, 0,'projectile'])
                        for i in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5 + math.pi, 2 + random.random()))
                    if (not self.flip and dis[0] > 0):
                        self.game.projectiles.append([[self.rect().centerx + 45, self.rect().centery-15], 5, 0,'projectile'])
                        for i in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5, 2 + random.random()))
           
        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)
        
        super().update(tilemap, movement=movement)
        if movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')
            
        if abs(self.game.player.dashing) >= 50:
            if self.rect().colliderect(self.game.player.rect()):
                for i in range(30):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 5
                    self.game.sparks.append(Spark(self.rect().center, angle, 2 + random.random()))
                    #self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                self.game.sparks.append(Spark(self.rect().center, 0, 5+ random.random()))
                self.game.sparks.append(Spark(self.rect().center, math.pi, 5 + random.random()))
             
                return True
    #lắp súng
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)
        
        if self.flip:
            surf.blit(pygame.transform.flip(self.game.assets['gun'], True, False), (self.rect().centerx - 20 - self.game.assets['gun'].get_width() - offset[0], self.rect().centery-20 - offset[1]))
        else:
            surf.blit(self.game.assets['gun'], (self.rect().centerx + 20 - offset[0], self.rect().centery-20 - offset[1]))
            
        
    