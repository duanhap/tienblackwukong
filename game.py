import pygame
import math
import os
import random
import sys
from scripts.menu import Menu
from scripts.settings import GameState
from scripts.settings import *
from scripts.utils import load_image,load_images,Animation,draw_health_bar,draw_bar_hp,toggle_mute
from scripts.animation2 import get_frame,get_frames,Animation2
from scripts.Player import Player
from scripts.cungthu import CungThu
from scripts.bosschim import BossChim
from scripts.nguoisoi import NguoiSoi
from scripts.nguoisoido import NguoiSoiDo
from scripts.bossnguoida import BossNguoiDa
from scripts.bossanhliems import BossAnhLiems
from scripts.trubatgioi import TruBatGioi
from scripts.npcsoi import NpcSoi
from scripts.Enemy import Enemy
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle
from scripts.spark import Spark
from scripts.phanthan import PhanThan
import pygame
import pygame
from moviepy.editor import VideoFileClip



#make your game its own object
class Game:
    def __init__(self):
        pygame.init()
        self.game_state = GameState()
        self.menu = Menu(self,self.game_state)
        self.capnhatvitriplayer = True
       
        # đặt tên ứng dụng
        pygame.display.set_caption('BLACK MYTH WUKONG')
        self.screen = pygame.display.set_mode((1200,800))
        #tốc đọ khung hình
        self.clock = pygame.time.Clock() 

        #dichuyen
        self.movement =[False,False]
       
        #load_image
        self.assets={
            #background và decor
            'decor':load_images('tiles/decor',(50,50),(0,0,0)),# trả về 1 mảng ảnh png  
            'grass':load_images('tiles/grass',(50,50),(0,0,0)),
            'grass3':load_images('tiles/grass3',(50,50),(0,0,0)),
            'grass2':load_images('tiles/grass2',(50,50),(255,255,255)),
            'large_decor':load_images('tiles/large_decor',None,(0,0,0),5),
            'stone':load_images('tiles/stone',(50,50),(0,0,0)),
            'stone2':load_images('tiles/stone2',(50,50),(255,255,255)),
            'binhruou':load_image('hp3.png',(112,112),(255,255,255)),
            'amount':load_image('amount.png',(112,112),(255,255,255)),
            'noitaifull':load_image('full.png',(900,800),(255,255,255)),
            'noitaichuafull':load_image('chuafull.png',(900,800),(255,255,255)),
            'player':load_image('entities/player.png',(95,125),(255,255,255)),
            'background':load_image('background.png',(1200,800)),
            'intro':load_image('intro.png',(1200,800)),
            'introword':load_image('introword3.png',(1200,800),(0,0,0)),
            'tree':load_images('tiles/tree',None,(255,255,255),5),
            'clouds':load_images('clouds/man1',None,(0,0,0)),
            'clouds2':load_images('clouds/man2',None,(0,0,0)),
            'stonegrass':load_images('tiles/stonegrass',None,(0,0,0),2),
            'ice':load_images('tiles/ice',None,(0,0,0),2),
            'background3':load_image('background3.png',(1200,800)),
            'menu':load_image('menu.jpg',(1200,800)),
            
             #dan lam
            'background2':load_image('background22.png',(1200,800)),
            'groundforest':load_images('tiles/groundforest',(50,50),(0,0,0)),
            'caydamlay':load_images('tiles/caydamlay',None,(255,255,255),2),
            









            # nhan vật và enemy
            'enemy/idle': Animation(load_images('entities/enemy/idle',(75, 100),(0,0,0)), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run',(75,100),(0,0,0)), img_dur=4),

            #cungthu
            'cungthu/idle': Animation(load_images('entities/cungthu/idle',(200, 200),(255,255,255)), img_dur=6),
            'cungthu/run': Animation(load_images('entities/cungthu/run',(200,200),(255,255,255)), img_dur=4),
            'cungthu/attack': Animation(load_images('entities/cungthu/attack',(200,200),(255,255,255)), img_dur=9,loop=False),
            'cungthu/attackngoi': Animation(load_images('entities/cungthu/attackngoi',(200,200),(255,255,255)), img_dur=5,loop=False),
            'cungthu/attackgan': Animation(load_images('entities/cungthu/attackgan',(200,200),(255,255,255)), img_dur=7,loop=False),
            'cungthu/attackchuanbigandam': Animation(load_images('entities/cungthu/attackchuanbigandam',(200,200),(255,255,255)), img_dur=15,loop=False),
            'cungthu/attackgandam': Animation(load_images('entities/cungthu/attackgandam',(200,200),(255,255,255)), img_dur=7,loop=False),
            'cungthu/hurt': Animation(load_images('entities/cungthu/hurt',(200,200),(255,255,255)), img_dur=17,loop=False),
            'cungthu/die': Animation(load_images('entities/cungthu/die',(200,200),(255,255,255)), img_dur=12,loop=False),
            
            #bosschim
            'bosschim/idle': Animation(load_images('entities/bosschim/idle',(400, 400),(255,255,255)), img_dur=10),
            'bosschim/walk': Animation(load_images('entities/bosschim/walk',(400,400),(255,255,255)), img_dur=4),
            'bosschim/attackkiemchuanbi': Animation(load_images('entities/bosschim/attackiemchuanbi',(400,400),(255,255,255)), img_dur=19,loop=False),
            'bosschim/attackkiem': Animation(load_images('entities/bosschim/attackkiem',(400,400),(255,255,255)), img_dur=5,loop=False),
            'bosschim/attackgan': Animation(load_images('entities/bosschim/attackgan',(400,400),(255,255,255)), img_dur=9,loop=False),
            'bosschim/hurt': Animation(load_images('entities/bosschim/hurt',(400,400),(255,255,255)), img_dur=7,loop=False),
            'bosschim/die': Animation(load_images('entities/bosschim/die',(400,400),(255,255,255)), img_dur=12,loop=False),
            'bosschim/win': Animation(load_images('entities/bosschim/win',(400,400),(255,255,255)), img_dur=31,loop=True),
            'bosschim/tipcan': Animation(load_images('entities/bosschim/tipcan',(400,400),(255,255,255)), img_dur=6,loop=True),
            'bosschim/jump': Animation(load_images('entities/bosschim/jump',(400,400),(255,255,255)), img_dur=2,loop=False),

            #player
            'player/idle':Animation(load_images('entities/player/idle',(95,125),(255,255,255)),img_dur=15),
            'player/run':Animation(load_images('entities/player/run',(95,125),(255,255,255)),img_dur=10),
            'player/phanthanskill':Animation(load_images('entities/player/phanthanskill',(95,125),(255,255,255)),img_dur=12,loop=False),
            'player/jump':Animation(load_images('entities/player/jump',(95,125),(255,255,255))),
            'player/block':Animation(load_images('entities/player/block',(95,125),(255,255,255))),
            'player/hurt':Animation(load_images('entities/player/hurt',(95,125),(255,255,255)),img_dur=8,loop=False),


            'player/attack':Animation(load_images('entities/player/attack2',(610,590),(255,255,255)),img_dur=6,loop=False),
            'player/attack2':Animation(load_images('entities/player/attack1',(610,590),(255,255,255)),img_dur=6,loop=False),
            'player/attack4':Animation(load_images('entities/player/attacknoitai',(610,590),(255,255,255)),img_dur=8.5,loop=False),
            'player/attack3':Animation(load_images('entities/player/attack',(300,300),(255,255,255)),img_dur=6,loop=False),
            'particle/leaf': Animation(load_images('particles/leaf',(40,40),(0,0,0)), img_dur=30, loop=False),
            'particle/particle': Animation(load_images('particles/particle',(50,50),(0,0,0)), img_dur=12, loop=False),
            'particle/particlewukong': Animation(load_images('particles/particlewukong',(50,50),(0,0,0)), img_dur=12, loop=False),


            #new monster
            'nguoisoi/idle': Animation2(get_frames('\\images\\entities\\nguoisoi\\idle',2), img_dur=5,loop=True),
            'nguoisoi/walk': Animation2(get_frames('\\images\\entities\\nguoisoi\\walk',2), img_dur=5,loop=True),
            'nguoisoi/die': Animation2(get_frames('\\images\\entities\\nguoisoi\\dead',2), img_dur=20,loop=False),
            'nguoisoi/hurt': Animation2(get_frames('\\images\\entities\\nguoisoi\\hurt',2 ), img_dur=10,loop=False),
            'nguoisoi/jump': Animation2(get_frames('\\images\\entities\\nguoisoi\\jump',2), img_dur=5.5,loop=False),
            'nguoisoi/attackgan1': Animation2(get_frames('\\images\\entities\\nguoisoi\\attackgan1',2)+
                                                get_frames('\\images\\entities\\nguoisoi\\attackgan2',2), img_dur=5,loop=False),


            'nguoisoido/idle': Animation2(get_frames('\\images\\entities\\nguoisoido\\idle',2), img_dur=5,loop=True),
            'nguoisoido/run': Animation2(get_frames('\\images\\entities\\nguoisoido\\run',2)+
                                         get_frames('\\images\\entities\\nguoisoido\\jump',2), img_dur=5,loop=True),
            'nguoisoido/die': Animation2(get_frames('\\images\\entities\\nguoisoido\\dead',2), img_dur=20,loop=False),
            'nguoisoido/hurt': Animation2(get_frames('\\images\\entities\\nguoisoido\\hurt',2 ), img_dur=10,loop=False),
            'nguoisoido/attackgan1': Animation2(get_frames('\\images\\entities\\nguoisoido\\attackgan1',2)+
                                                get_frames('\\images\\entities\\nguoisoido\\attackgan2',2)+
                                                get_frames('\\images\\entities\\nguoisoido\\attackgan3',2), img_dur=6.9,loop=False),
            

            #boss ngươi da
            'bossnguoida/idle': Animation(load_images('entities/bossnguoida/idle',(1100,800),(255,255,255)),img_dur=10,loop=True),
            'bossnguoida/attackchocxa': Animation(load_images('entities/bossnguoida/attack',(1100,800),(255,255,255)),img_dur=7,loop=False),
            'bossnguoida/attackgan': Animation(load_images('entities/bossnguoida/attackgan',(1100,800),(255,255,255)),img_dur=6,loop=False),
            'bossnguoida/block': Animation(load_images('entities/bossnguoida/block',(1100,800),(255,255,255)),img_dur=8,loop=False),
            'bossnguoida/die': Animation(load_images('entities/bossnguoida/die',(1100,800),(255,255,255)),img_dur=6,loop=False),
            'bossnguoida/hurt': Animation(load_images('entities/bossnguoida/idle',(1100,800),(255,255,255)),img_dur=4,loop=False),
            'bossnguoida/xuathien': Animation(load_images('entities/bossnguoida/xuathien',(1100,800),(255,255,255)),img_dur=10,loop=False),
            'bossnguoida/banlazecao': Animation(load_images('entities/bossnguoida/banlazecao',(1100,800),(255,255,255))+
                                                load_images('entities/bossnguoida/banlazecao',(1100,800),(255,255,255))+
                                                load_images('entities/bossnguoida/banlazecao',(1100,800),(255,255,255)),img_dur=5,loop=False),
            'bossnguoida/banlazethap': Animation(load_images('entities/bossnguoida/banlazethap',(2000,800),(255,255,255)),img_dur=6.6,loop=False),




            #nhi lang than
            'nhilangthan/idle':Animation(load_images('entities/nhilangthan/idle',(172,198),(255,255,255)),img_dur=15),
            'nhilangthan/hurt':Animation(load_images('entities/nhilangthan/hurt',(172,198),(255,255,255)),img_dur=5,loop=False),
            'nhilangthan/ne':Animation(load_images('entities/nhilangthan/ne',(1080,360),(255,255,255)),img_dur=5,loop=False),
            'nhilangthan/block':Animation(load_images('entities/nhilangthan/block',(410,390),(255,255,255)),img_dur=5,loop=False),
            'nhilangthan/xuathien':Animation(load_images('entities/nhilangthan/xuathien',(2000,1300),(255,255,255)),img_dur=6.5,loop = False),
            'nhilangthan/walk':Animation(load_images('entities/nhilangthan/walk',(172,198),(255,255,255)),img_dur=8),
            'nhilangthan/die':Animation(load_images('entities/nhilangthan/die',(2000,1300),(255,255,255)),img_dur=8,loop = False),
            'nhilangthan/phikiem':Animation(load_images('entities/nhilangthan/phikiem',(1080,360),(255,255,255)),img_dur=8,loop = False),
            'nhilangthan/tialazemax':Animation(load_images('entities/nhilangthan/tialazeoeoeoe',(1800,1300),(255,255,255)),img_dur=6.5,loop = False),
            'nhilangthan/nemriu':Animation(load_images('entities/nhilangthan/xenuisavemom',(1800,1300),(255,255,255)),img_dur=6.5,loop = False),
            'riuthan/idle':Animation(load_images('entities/nhilangthan/riu',(800,500),(255,255,255)),img_dur=6.5,loop = False),
            'nhilangthan/luot':Animation(load_images('entities/nhilangthan/luot',(1080,360),(255,255,255)),img_dur=6,loop = False),
            'nhilangthan/chuanbilao':Animation(load_images('entities/nhilangthan/chuanbilao',(1080,360),(255,255,255)),img_dur=6,loop = False),
            'nhilangthan/laodenattack':Animation(load_images('entities/nhilangthan/laodenattack',(1080,360),(255,255,255)),img_dur=6,loop = False),
            'nhilangthan/laodenattack2':Animation(load_images('entities/nhilangthan/laodenatack2',(1080,360),(255,255,255)),img_dur=6,loop = False),
            'nhilangthan/xoay':Animation(load_images('entities/nhilangthan/attackxoay',(410,390),(255,255,255)),img_dur=8,loop = False),
            'nhilangthan/combogan':Animation(load_images('entities/nhilangthan/attackcombongan',(420,390),(255,255,255)),img_dur=7,loop = False),
            'nhilangthan/tialazegan':Animation(load_images('entities/nhilangthan/tialazegan',(1080,360),(255,255,255)),img_dur=4,loop = False),


            #trubatgioi
            'trubatgioi/idle':Animation(load_images('entities/trubatgioi/idle',(320,260),(255,255,255)),img_dur=15),
            'trubatgioi/run':Animation(load_images('entities/trubatgioi/run',(320,260),(255,255,255)),img_dur=5),
            #'trubatgioi/jump':Animation(load_images('entities/trubatgioi/jump',(95,125),(255,255,255))),
            #'trubatgioi/hurt':Animation(load_images('entities/trubatgioi/hurt',(95,125),(255,255,255)),img_dur=8,loop=False),
            'trubatgioi/attack':Animation(load_images('entities/trubatgioi/attack',(320,260),(255,255,255)),img_dur=5,loop=False),


 

            #npc
            'npcsoi/idle': Animation2(get_frames('\\images\\entities\\npcsoi\\idle',0.3), img_dur=8,loop=True),

            #loithoai
            'loithoainpc':Animation(load_images('entities/loithoai',(1200,400),(255,255,255)),img_dur=400,loop=True),
            'loithoaichim':Animation(load_images('entities/bosschim/loithoai',(1000,300),(255,255,255)),img_dur=300,loop=True),
            'loithoaibatgioi':Animation(load_images('entities/trubatgioi/loithoai',(1200,400),(255,255,255)),img_dur=160,loop=True),


            



            #phanthan
            'phanthan/idle':Animation(load_images('entities/player/idle',(95,125),(255,255,255)),img_dur=15),
            'phanthan/run':Animation(load_images('entities/player/run',(95,125),(255,255,255)),img_dur=10),
            'phanthan/jump':Animation(load_images('entities/player/jump',(95,125),(255,255,255))),
            'phanthan/hurt':Animation(load_images('entities/player/hurt',(95,125),(255,255,255)),img_dur=8,loop=False),
            'phanthan/attack':Animation(load_images('entities/player/attack',(300,300),(255,255,255)),img_dur=5,loop=False),
            'phanthan/die':Animation(load_images('entities/player/die',(200,200),(0,0,0)),img_dur=10,loop=False),




            #loại đạn 
            'gun': load_image('gun.png',(25,25),(0,0,0)),
            'projectile': load_image('projectile.png',(20,15),(0,0,0)),
            'cungten1': load_image('cungten1.png',(80,6),(0,0,0)),
            'cungten2': load_image('cungten2.png',(80,6),(255,255,255)),
            'kiem1': load_image('kiem1.png',(100,20),(255,255,255)),
            'kiem2': load_image('kiem2.png',(100,20),(255,255,255)),
            'kiemnangluong1': load_image('kimnl1.png',(100,180),(0,0,0)),
            'kiemnangluong2': load_image('kimnl2.png',(100,180),(0,0,0)),

            
            #'intro':Animation(load_images('tiles/batdau',(1200,800)),img_dur=10,loop=False)
            
            
            
        }
        #âm thanks
        self.sfx={
            'chuyencanh':pygame.mixer.Sound('data/sfx/chuyencanh.mp3'),
            'chamvukhi':pygame.mixer.Sound('data/sfx/chamvukhi.mp3'),
            'tocbien':pygame.mixer.Sound('data/sfx/tocbien.mp3'),
            'tocbienquai':pygame.mixer.Sound('data/sfx/tocbienquai.mp3'),
            'bidanh':pygame.mixer.Sound('data/sfx/bidanh.mp3'),
            'wukongvoicechieudai':pygame.mixer.Sound('data/sfx/wukongvoicechieudai.mp3'),
            'boom':pygame.mixer.Sound('data/sfx/boom.mp3'),
            'xakiem':pygame.mixer.Sound('data/sfx/xakiem.mp3'),
        }
        self.sfx['chuyencanh'].set_volume(0.01)
        self.sfx['boom'].set_volume(0.01)
        self.sfx['xakiem'].set_volume(0.1   ) 
        self.sfx['tocbien'].set_volume(0.5)
        self.sfx['tocbienquai'].set_volume(5.1)
        self.sfx['bidanh'].set_volume(7)
        self.sfx['chamvukhi'].set_volume(5.1)
        self.sfx['wukongvoicechieudai'].set_volume(1.1)

        self.clip = VideoFileClip("data/demo.mp4")
        self.show_intro_video()  # Play the intro video
        self.original_volumes = {key: sound.get_volume() for key, sound in self.sfx.items()}

        

        
        #clouds1
        self.clouds1 = Clouds(self.assets['clouds'],count = 2,scale=1.2)
        self.clouds2 = Clouds(self.assets['clouds2'],count=6,scale =4.5)
        #set level
        self.level = 0
        self.load_level(self.level)


        #clouds
        self.clouds = Clouds(self.assets['clouds'],count = 7,scale=1.2)


        #soluongphanthan
        self.anhem=4
    
    def show_intro_video(self):
        # Play the intro video
        intro_duration = self.clip.duration  # Get the duration of the video
        start_time = pygame.time.get_ticks()
        pygame.mixer.music.load('data/intro.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        while True:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - start_time) / 1000.0

            if elapsed_time >= intro_duration:
                break  # Exit after the video duration

            # Get the frame corresponding to the elapsed time
            frame = self.clip.get_frame(elapsed_time)

            # Convert the frame to a Pygame surface
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

            # Blit the frame onto the screen
            self.screen.blit(pygame.transform.scale(frame_surface, self.screen.get_size()), (0, 0))

            pygame.display.update()
            self.clock.tick(30)  # Set the frame rate

            # Handle events (e.g., for skipping the video)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.game_state.fullscreen = not self.game_state.fullscreen
                        if self.game_state.fullscreen:
                            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Chuyển sang fullscreen
                        else:
                            self.screen = pygame.display.set_mode((1200, 800))  # Trở lại cửa sổ ban đầu
                    if event.key == pygame.K_SPACE:  # Skip the video by pressing space
                        
                        return
    def show_ending_video(self):
        # Play the intro video
        intro_duration = self.clip.duration  # Get the duration of the video
        start_time = pygame.time.get_ticks()
        pygame.mixer.music.load('data/ending.mp3')
        pygame.mixer.music.set_volume(0.9)
        pygame.mixer.music.play(-1)
        while True:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - start_time) / 1000.0

            if elapsed_time >= intro_duration:
                break  

            frame = self.clip.get_frame(elapsed_time)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            self.screen.blit(pygame.transform.scale(frame_surface, self.screen.get_size()), (0, 0))

            pygame.display.update()
            self.clock.tick(30)  #30Fps

            # Handle events (e.g., for skipping the video)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.game_state.fullscreen = not self.game_state.fullscreen
                        if self.game_state.fullscreen:
                            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Chuyển sang fullscreen
                        else:
                            self.screen = pygame.display.set_mode((1200, 800))  # Trở lại cửa sổ ban đầu
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.music.stop()  # Skip the video by pressing space
                        return
                    

    def load_level(self, map_id):

        self.sfx['chuyencanh'].play()

        
        #khaibao image player va tilemap
        self.player = Player(self,(400,-1700),(95,125))
       
        self.tilemap = Tilemap(self,tile_size=50)
      
        
        self.tilemap.load(str(map_id) + '.json')
        # hịu ứng lá rơi  nhờ extract map để bik vị trí spawwn
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(50 + tree['pos'][0],50  + tree['pos'][1], 100, 130))
        for tree in self.tilemap.extract([('tree', 0)], keep=True):
            self.leaf_spawners.append(pygame.Rect(150 + tree['pos'][0],150  + tree['pos'][1], 500, 1000))  
        for tree in self.tilemap.extract([('tree', 1)], keep=True):
            self.leaf_spawners.append(pygame.Rect(150 + tree['pos'][0],150  + tree['pos'][1], 500, 1000))   

        #enemy
        self.enemies = []
        self.npc=[]
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1),('spawners', 2),
                                             ('spawners', 3),('spawners', 4),('spawners', 5),
                                             ('spawners', 6),('spawners', 7),('spawners',8),
                                             ('spawners', 9)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time =0
            if spawner['variant'] == 1:
                self.enemies.append(Enemy(self, spawner['pos'], (75, 100)))
            if spawner['variant'] == 2:
                self.enemies.append(CungThu(self, spawner['pos'], (75, 100)))
            if spawner['variant'] == 3:
                self.enemies.append(BossChim(self, spawner['pos'], (75, 100)))
            if spawner['variant'] == 4:
                self.enemies.append(NguoiSoi(self, spawner['pos'], (75, 100)))
            if spawner['variant'] == 5:
                self.enemies.append(NguoiSoiDo(self, spawner['pos'], (75, 100)))
            if spawner['variant'] == 6:
                self.npc.append(NpcSoi(self, spawner['pos'], (75, 100)))
            if spawner['variant'] == 7:
                self.enemies.append(BossNguoiDa(self, spawner['pos'], (75, 100)))
            if spawner['variant'] == 8:
                self.enemies.append(BossAnhLiems(self, spawner['pos'], (75, 100)))
            if spawner['variant'] == 9:
                self.npc.append(TruBatGioi(self, spawner['pos'], (75, 100)))
            
        self.projectiles = [] #đạn bắn
        self.particles = []
        self.sparks = []   #hiệu ứng
        self.scroll =[0,0]
        self.dead = 0
        self.phanthans=[]  #skill
        self.screenshake=0 #rung lắc
        self.transition =-30 


    # Hàm vẽ thanh máu
    


    def add_player(self):
        if self.player.flip:
            x = self.player.pos[0]-  random.randint(75,150)# Tạo khoảng cách giữa các nhân vật
        else:
            x = self.player.pos[0]+  random.randint(75,150)
        y = self.player.pos[1] -  random.randint(0,100)        
        new_player = PhanThan(self, (x, y), (95,125) )
        if len(self.phanthans) <self.anhem :
            self.player.mana-=5
            self.phanthans.append(new_player)
            self.sfx['tocbienquai'].play()
            for i in range(30):
                angle = random.random() * math.pi * 2
                speed = random.random() * 2
                self.sparks.append(Spark(new_player.rect().center, angle, 2 + random.random()))
                self.particles.append(Particle(self, 'particle', new_player.rect().center, velocity=[math.cos(angle + math.pi) * speed , math.sin(angle + math.pi) * speed ], frame=random.randint(0, 7)))

    
    def run(self):
       
        current_music = None
       
        while True:

            # Kiểm tra và phát nhạc phù hợp với level hiện tại

            # set nhạc cho mỗi map
            if self.level == 0 and current_music != 'intro':
                self.anhem=0

                pygame.mixer.music.stop()
                pygame.mixer.music.load('data/intro.mp3')
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1) # Phát nhạc lặp lại
                current_music = 'intro'
            elif self.level==1 and current_music != 'khoidau':
                self.anhem=4
                pygame.mixer.music.stop()
                pygame.mixer.music.load('data/khoidau.mp3')
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                current_music = 'khoidau'
            elif self.level==2 and current_music != 'lv2':
                self.anhem=4
                pygame.mixer.music.stop()
                pygame.mixer.music.load('data/lv2.mp3')
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play(-1)
                current_music = 'lv2'
            elif self.level==3 and current_music != 'lv3':
                self.anhem=4
                pygame.mixer.music.stop()
                pygame.mixer.music.load('data/lv3.mp3')
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play(-1)
                current_music = 'lv3'
            """
             if self.level==2 and len(self.enemies) ==0:
                self.clip = VideoFileClip("data/ending.mp4")
                self.show_ending_video()
                #restart game 
                os.execv(sys.executable, ['game'] + sys.argv)
            """
           
                
           
            #camera theo player
            if self.capnhatvitriplayer:
                self.scroll[0]+=(self.player.rect().centerx-self.screen.get_width()/2-self.scroll[0])/50
                self.scroll[1]+=(self.player.rect().centery-90-self.screen.get_height()/2-self.scroll[1])/3
            render_scroll =(int(self.scroll[0]),int(self.scroll[1]))

        
            # set BG cho mỗi map
            if self.level ==0 :
                
                if self.game_state.fullscreen:
                    info = pygame.display.Info()
                    self.assets['background'] =load_image('background.png',(info.current_w,info.current_h))
                    self.screen.blit(self.assets['background'],(0,0))
                    render_scroll=(-290,-200)
                else:
                    self.screen.blit(self.assets['intro'],(0,0))
                    render_scroll=(0,0)     
            elif self.level ==1:
                if self.game_state.fullscreen:
                    info = pygame.display.Info()
                    self.assets['background'] =load_image('background.png',(info.current_w,info.current_h))
                else:
                    self.assets['background'] =load_image('background.png',(1200,800))
                
                self.screen.blit(self.assets['background'],(0,0))
            elif self.level ==2:
                if self.game_state.fullscreen:
                    info = pygame.display.Info()
                    self.assets['background2'] =load_image('background22.png',(info.current_w,info.current_h))
                else:
                    self.assets['background2'] =load_image('background22.png',(1200,800))
            
                self.screen.blit(self.assets['background2'],(0,0))
            
            elif self.level ==3:
                if self.game_state.fullscreen:
                    info = pygame.display.Info()
                    self.assets['background3'] =load_image('background3.png',(info.current_w,info.current_h))
                else:
                    self.assets['background3'] =load_image('background3.png',(1200,800))
                
                self.screen.blit(self.assets['background3'],(0,0))


            #rung lắc
            self.screenshake = max(0,self.screenshake-1)

            
            #cloud
            if self.level !=2:
                self.clouds.update()
                self.clouds.render(self.screen,offset = render_scroll)
            else:
                self.clouds2.update()
                self.clouds2.render(self.screen,offset = render_scroll)

            
            
            if self.level ==0  and self.game_state.fullscreen:
                info = pygame.display.Info()
                self.assets['introword'] =load_image('introword3.png',(info.current_w,info.current_h),(0,0,0))
                self.screen.blit(self.assets['introword'],(0,0))
            
                

            #tilemap
            self.tilemap.render(self.screen,offset = render_scroll)

            #đạn
            # [[x, y], direction, timer,loaidan] cáu tạo projectile
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1 #timer
                img = self.assets[ projectile[3]]
                self.screen.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1])) # chia chia là lấy center 

                # check xem chạm tile map thì mất 
                if self.tilemap.solid_check(projectile[0],"dan"):
                    self.projectiles.remove(projectile)
                    if  projectile[3] =='kiemnangluong1' or projectile[3] =='kiemnangluong2':
                        if random.randint(0,100)<35:
                             self.screenshake = max(20,self.screenshake)
                        for i in range(20):
                            self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 5 + random.random()))
                    else:
                        for i in range(10):
                            self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))

                #bay lâu quá cx cút        
                elif projectile[2] > 1360:
                    self.projectiles.remove(projectile)

                # chạm người đang ko dang dash cx cút
                elif abs(self.player.dashing) < 50:
                    if  projectile[3] =='kiemnangluong1' or projectile[3] =='kiemnangluong2':
                        if self.player.recttuongtac().collidepoint(projectile[0][0]+random.randint(-5,5),projectile[0][1]+random.randint(-45,45)) :
                            if not self.player.blocking:
                                self.projectiles.remove(projectile)
                                self.player.hp-=1
                                self.sfx['bidanh'].play()
                                self.screenshake = max(20,self.screenshake)
                                for i in range(30):
                                    angle = random.random() * math.pi * 2
                                    speed = random.random() * 5
                                    self.sparks.append(Spark(self.player.rect().center, angle, 3 + random.random()))
                                    #self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed , math.sin(angle + math.pi) * speed ], frame=random.randint(0, 7)))
                            else:
                                self.player.stamina-=1.5
                                if random.randint(0,100)<25:
                                    self.screenshake = max(random.randint(16,60),self.screenshake)
                                self.sfx['chamvukhi'].play()
                                self.projectiles.remove(projectile)
                                for i in range(10):
                                    self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 5 + random.random()))
                    elif self.player.recttuongtac().collidepoint(projectile[0]) and not self.player.blocking: #cho biết điểm pos của đạn có nằm trong hình chữ nhật hay không.
                        # còn thêm colliderList nữa
                        self.projectiles.remove(projectile)
                        self.player.hp-=1
                        self.sfx['bidanh'].play()
                        self.screenshake = max(16,self.screenshake)
                        for i in range(10):
                                    self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                    elif self.player.recttuongtac().collidepoint(projectile[0]) and  self.player.blocking:
                        self.projectiles.remove(projectile)
                        self.sfx['chamvukhi'].play()
                        self.player.stamina-=1
                        for i in range(10):
                            self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))

                    
            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.screen, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)  


            #hien sô lượng anime
            if self.level!=0:
                font = pygame.font.Font(None, 50)
                text_surface = font.render(str(len(self.enemies)), True, (0,0,0))
                text_surfaceX = font.render("X", True, (0,0,0))
                self.screen.blit(text_surface, (self.screen.get_width() - 200, 50))
                self.screen.blit(text_surfaceX, (self.screen.get_width() - 150, 50))
                self.screen.blit(self.assets['amount'],(self.screen.get_width() - 140,20))  
                        
            #ênmy
            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                
                enemy.render(self.screen, offset=render_scroll)
                if kill:
                    if enemy.type=='bossChim' and enemy.mainBoss==True:
                        self.enemies.remove(enemy)
                        for enemy2 in self.enemies:
                            if enemy2.type =='bosschim' and enemy.mainBoss==False:
                                enemy2.hp=-1
                                enemy2.set_action='die'
                                
                    self.enemies.remove(enemy)
                else:
                    if enemy.type=='bosschim'and self.player.pos[0]>2800 and self.player.pos[0]<5300  and enemy.mainBoss==True:
                       
                        draw_health_bar(self.screen,self.screen.get_width() // 2 - 250,  50,enemy.hp, enemy.hp_max,(255,0,0),500,20)
                    if enemy.type=="bossnguoida" and self.player.pos[0]<-2400 and self.player.pos[0]>-4800:          
                        draw_health_bar(self.screen,self.screen.get_width() // 2 - 250,  50,enemy.hp, enemy.hp_max,(255,0,0),500,20)
                    if enemy.type=="nhilangthan" and self.player.pos[0]<3971 and self.player.pos[0]>3971:          
                        draw_health_bar(self.screen,self.screen.get_width() // 2 - 250,  50,enemy.hp, enemy.hp_max,(255,0,0),500,20)

            #phanthan
            for phanthan in self.phanthans.copy():
                kill = phanthan.update(self.tilemap, (0, 0))
                phanthan.render(self.screen, offset=render_scroll)
                if kill:
                         self.phanthans.remove(phanthan)
           
                
                    
               

            #la roi
            for rect in self.leaf_spawners:
                if random.random() * 6500000 < rect.width * rect.height: # NHÂN SỐ CÀNG TO TỶ LỆ RA CẰNG THẤP
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.screen, offset=render_scroll)
                if particle.type == 'leaf':
                    # Chuyển động nhẹ theo trục x để tạo hiệu ứng dao động gió
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.5  # Tăng nhẹ tần suất dao động
                    #cham vô vùng tấn công của anime
                    for entity in self.enemies:
                        if entity.attacking and entity.animation.doneToDoSomething and random.randint(0, 100) < 80:
                            dis_x = entity.rectattack().centerx - particle.pos[0]
                            dis_y = entity.rectattack().centery - particle.pos[1]
                            if dis_x < 60 and dis_x >= -200 and abs(dis_y) <= 150:
                                particle.pos[0] += min(30, abs(dis_x) / 1.1)  # Giảm tốc độ dịch chuyển
                                particle.pos[1] -= random.randint(-150, 150)  # Giảm độ ngẫu nhiên trục y cho mượt hơn
                                
                            # Xử lý va chạm khi đạn từ phải qua trái
                            if dis_x > -60 and dis_x <= 200 and abs(dis_y) <= 150:
                                particle.pos[0] -= min(30, abs(dis_x) / 1.1)  # Giảm tốc độ dịch chuyển
                                particle.pos[1] -= random.randint(-150, 150)  # Giảm độ ngẫu nhiên trục y
                    # người chơi tấn công
                    if self.player.attacking == True:
                        if self.player.animation.doneToDoSomething and random.randint(0, 100) < 80:
                            dis_x = self.player.rectattack().centerx - particle.pos[0]
                            dis_y = self.player.rectattack().centery - particle.pos[1]
                            if dis_x < 60 and dis_x >= -200 and abs(dis_y) <= 150:
                                particle.pos[0] += min(30, abs(dis_x) / 1.1)  # Giảm tốc độ dịch chuyển
                                particle.pos[1] -= random.randint(-150, 150)  # Giảm độ ngẫu nhiên trục y cho mượt hơn
                                
                            # Xử lý va chạm khi đạn từ phải qua trái
                            if dis_x > -60 and dis_x <= 200 and abs(dis_y) <= 150:
                                particle.pos[0] -= min(30, abs(dis_x) / 1.1)  # Giảm tốc độ dịch chuyển
                                particle.pos[1] -= random.randint(-150, 150)  # Giảm độ ngẫu nhiên trục y
                    #phanthan dánh
                    for entity in self.phanthans:
                        if entity.attacking and entity.animation.doneToDoSomething and random.randint(0, 100) < 80:
                            dis_x = entity.rectattack().centerx - particle.pos[0]
                            dis_y = entity.rectattack().centery - particle.pos[1]
                            if dis_x < 60 and dis_x >= -200 and abs(dis_y) <= 150:
                                particle.pos[0] += min(30, abs(dis_x) / 1.1)  # Giảm tốc độ dịch chuyển
                                particle.pos[1] -= random.randint(-150, 150)  # Giảm độ ngẫu nhiên trục y cho mượt hơn
                                
                            # Xử lý va chạm khi đạn từ phải qua trái
                            if dis_x > -60 and dis_x <= 200 and abs(dis_y) <= 150:
                                particle.pos[0] -= min(30, abs(dis_x) / 1.1)  # Giảm tốc độ dịch chuyển
                                particle.pos[1] -= random.randint(-150, 150)  # Giảm độ ngẫu nhiên trục y
                    # người chơi dash
                    if abs(self.player.dashing) >30  and random.randint(0, 100) < 80:
                            dis_x = self.player.recttuongtac().centerx - particle.pos[0]
                            dis_y = self.player.recttuongtac().centery - particle.pos[1]
                            if dis_x < 60 and dis_x >= -200 and abs(dis_y) <= 150:
                                particle.pos[0] += min(30, abs(dis_x) / 1.1)  # Giảm tốc độ dịch chuyển
                                particle.pos[1] -= random.randint(-150, 150)  # Giảm độ ngẫu nhiên trục y cho mượt hơn
                                
                            # Xử lý va chạm khi đạn từ phải qua trái
                            if dis_x > -60 and dis_x <= 200 and abs(dis_y) <= 150:
                                particle.pos[0] -= min(30, abs(dis_x) / 1.1)  # Giảm tốc độ dịch chuyển
                                particle.pos[1] -= random.randint(-150, 150)  # Giảm độ ngẫu nhiên trục y

                    for dan in self.projectiles:
                        if random.randint(0, 100) < 65:
                            dis_x = dan[0][0] - particle.pos[0]
                            dis_y = dan[0][1] - particle.pos[1]
                            discao = 0
                            disxa =0
                            if dan[3] =='kiemnangluong1' or dan[3] =='kiemnangluong2':
                                discao=200
                                disxa = 200
                            else:
                                discao=40
                                disxa =120
                            # Xử lý va chạm khi đạn từ trái qua phải
                           
                            if dis_x < 20 and dis_x >= -1*disxa and abs(dis_y) <= discao:
                                particle.pos[0] += min(30, abs(dis_x) / 1.1)  # Giảm tốc độ dịch chuyển
                                particle.pos[1] -= random.randint(-150, 150)  # Giảm độ ngẫu nhiên trục y cho mượt hơn
                                
                            # Xử lý va chạm khi đạn từ phải qua trái
                            if dis_x > -20 and dis_x <= disxa and abs(dis_y) <= discao:
                                particle.pos[0] -= min(30, abs(dis_x) / 1.1)  # Giảm tốc độ dịch chuyển
                                particle.pos[1] -= random.randint(-150, 150)  # Giảm độ ngẫu nhiên trục y

                if kill:
                    self.particles.remove(particle)
          

            #thanh máu
            if self.level!=0:
                draw_health_bar(self.screen, 180, self.screen.get_height() - 112 , self.player.hp, self.player.hp_max,(220, 220, 220))
                draw_health_bar(self.screen, 180, self.screen.get_height() - 112 + 25, self.player.mana, self.player.mana_max,(0, 0, 139),40,10)
                draw_health_bar(self.screen, 180, self.screen.get_height() - 112 + 40, self.player.stamina, self.player.stamina_max,(255, 255, 0),150,10)
                draw_bar_hp(self.screen, 52, self.screen.get_height() - 160 + 5, self.player.binhhp, self.player.binhhpmax,(220, 220, 220),100,100)
                self.screen.blit(self.assets['binhruou'],(50,self.screen.get_height() - 160))
                draw_bar_hp(self.screen, self.screen.get_width() - 70, self.screen.get_height() - 170, self.player.noitai, self.player.noitai_max,(255, 0, 0),10,120,False)
                self.screen.blit(self.assets['noitaichuafull'],(self.screen.get_width() - 560,self.screen.get_height() - 740))
                if self.player.noitai>=10:
                   self.screen.blit(self.assets['noitaifull'],(self.screen.get_width() - 560,self.screen.get_height() - 740))
             #npc
            for npc1 in self.npc.copy():
               
                npc1.render(self.screen, offset=render_scroll)
                npc1.update(self.tilemap, (0, 0))


             #player
            if self.player.hp>0 :
                self.player.update(self.tilemap,(self.movement[1]-self.movement[0],0))
                self.player.render(self.screen,offset = render_scroll)
            else:
                self.sfx['boom'].play()
                for i in range(4):
                    angle = random.random() * math.pi * 2.2
                    speed = random.random() *2
                   # self.sparks.append(Spark(self.player.recttuongtac().center, angle,1+random.random()))
                    self.particles.append(Particle(self, 'particlewukong', (self.player.rect().centerx+4,self.player.rect().centery-6.5), velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                    
            #CO CHE LOAD MAP
                

            if not len(self.enemies):
                self.transition+=1
                if self.transition >30:
                    self.level=min(self.level+1,len(os.listdir('data/maps'))-1)
                    self.load_level(self.level)
            if self.transition<0:
                self.transition+=1

            if self.player.air_time>130 or self.player.hp<=0:
                self.player.hp -=1
                if self.player.air_time >200 or  self.player.hp <-200 :
                    self.player.air_time+=2
                    self.transition = min(30,self.transition+1)
                if self.player.air_time > 300 or  self.player.hp <-500 :
                    self.load_level(self.level)
              
            #cloud1
            if self.level !=2:
                self.clouds1.update()
                self.clouds1.render(self.screen,(render_scroll[0]*3,3*render_scroll[1]))
         


           
            #print(self.tilemap.physics_rects_around(self.player.pos))
            for event in pygame.event.get(): #get the input,click , keosv..vv
                if event.type == pygame.QUIT: #click dau X để thoát
                    pygame.quit()

                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.game_state.paused = not self.game_state.paused
                    if event.key == pygame.K_f:
                        self.game_state.fullscreen = not self.game_state.fullscreen
                        if self.game_state.fullscreen:
                            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Chuyển sang fullscreen
                        else:
                            self.screen = pygame.display.set_mode((1200, 800))  # Trở lại cửa sổ ban đầu
                    if event.key == pygame.K_LEFT:
                        self.player.xuathienomap1=0
                        self.player.timexuathien =500
                        self.movement[0] = True
                        
                    if event.key == pygame.K_RIGHT:
                        self.player.xuathienomap1=0
                        self.player.timexuathien =500
                        self.movement[1] = True
                        
                    if event.key == pygame.K_UP:
                        self.player.jump()
                        for i in range(20):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 2 + 1
                            pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                            self.particles.append(Particle(self, 'particlewukong', self.player.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))                 
                    if event.key == pygame.K_DOWN:            
                        self.player.blocking = True                  
                    if event.key == pygame.K_c:
                        
                        self.player.tichnoitai=True
                        self.player.attack()
                        
                               
                    if event.key == pygame.K_x:         
                        self.player.skillphanthan()   
                    if event.key == pygame.K_z:
                        self.player.dash()
                    if event.key == pygame.K_m:
                        self.enemies.clear()
                    
                       
                    if event.key == pygame.K_v and self.player.binhhp>0:
                        self.player.binhhp-=1
                        self.player.stamina=10
                        if self.player.hp>7:
                            self.player.hp=10
                        else:
                            self.player.hp+=3
                        
                       
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    #if event.key == pygame.K_q:
                        #self.phanthan = False
                    if event.key == pygame.K_DOWN:
                        self.player.blocking = False
                    if event.key == pygame.K_c:
                        self.player.tichnoitai = False
                        self.player.dieukiendanhnoitai=0
                if self.game_state.paused:
                    selected = self.menu.handle_event(event)
                    if selected == "Sound":
                        self.game_state.sound_on = not self.game_state.sound_on
                        toggle_mute(self.game_state.sound_on,self.sfx,self.original_volumes)  # Dừng nhạc nếu tắt âm thanh
                    elif selected == "Fullscreen":
                        self.game_state.fullscreen = not self.game_state.fullscreen
                        if self.game_state.fullscreen:
                            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Chuyển sang fullscreen
                        else:
                            self.screen = pygame.display.set_mode((1200, 800))  # Trở lại cửa sổ ban đầu
                    elif selected == "Resume":
                        self.game_state.paused = False
                    elif selected == "Quit":
                        self.game_state.running = False
                        pygame.quit()
                

            if self.game_state.paused:
                self.menu.draw(self.screen)
                pygame.display.update()
                continue
            
                        
            # hiệu ứng chuyển map
            if self.transition:
                transition_surf = pygame.Surface(self.screen.get_size())
                pygame.draw.circle(transition_surf,(255,255,255),(self.screen.get_width()//2,self.screen.get_height()//2),(30 - abs(self.transition))*8)
                transition_surf.set_colorkey((255,255,255))
                self.screen.blit(transition_surf,(0,0))

            #rung lắc
            screenshake_offset = (random.random()*self.screenshake - self.screenshake/2,random.random()*self.screenshake - self.screenshake/2)   
            self.screen.blit(pygame.transform.scale(self.screen,self.screen.get_size()),screenshake_offset)    
            pygame.display.update()
            self.clock.tick(60) # duy trì tốc độ 60FPS
Game().run()