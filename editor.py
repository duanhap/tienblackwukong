import pygame
import sys
from scripts.utils import load_images
from scripts.tilemap import Tilemap


class Editor:
    def __init__(self):
        pygame.init()

        # đặt tên ứng dụng
        pygame.display.set_caption('editor')
        self.screen = pygame.display.set_mode((1200,800))
        #tốc đọ khung hình
        self.clock = pygame.time.Clock() 

    

        #load_image
        self.assets={
            'decor':load_images('tiles/decor',(50,50),(0,0,0)),# trả về 1 mảng ảnh png
            'grass':load_images('tiles/grass',(50,50),(0,0,0)),
            'grass3':load_images('tiles/grass3',(50,50),(0,0,0)),
            'grass2':load_images('tiles/grass2',(50,50),(255,255,255)),
            'large_decor':load_images('tiles/large_decor',None,(0,0,0),5),
            'stone':load_images('tiles/stone',(50,50),(0,0,0)),
            'stone2':load_images('tiles/stone2',(50,50),(255,255,255)),
            'stonegrass':load_images('tiles/stonegrass',None,(0,0,0),2),
            'ice':load_images('tiles/ice',None,(0,0,0),2),
            'spawners': load_images('tiles/spawners',(50,50),(0,0,0)),
            'tree':load_images('tiles/tree',None,(255,255,255),5),
            'groundforest':load_images('tiles/groundforest',(50,50),(0,0,0)),
            'caydamlay':load_images('tiles/caydamlay',None,(255,255,255),2),
        }

        #dichuyen
        self.movement =[False,False,False,False]

        self.tilemap= Tilemap(self,tile_size=50)
        
        #hien map nào
        try:
           self.tilemap.load('3.json')
        except FileNotFoundError:
            pass
            
        self.scroll =[0,0]
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0
        
        #click 
        self.clicking = False
        self.right_clicking = False
        self.shift = False

        self.ongrid = True
       

    def run(self):
        while True:
            #BG
            self.screen.fill((0,0,0))

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 5
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 5
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.screen, offset=render_scroll)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)#alpha được đặt là 100, nghĩa là hình ảnh sẽ trở nên bán trong suốt.(0->255)


            #click chuột lấy vị trí
            mpos = pygame.mouse.get_pos()#lấy tọa độ click chuột
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))
            




            # hiện tile map trc con trỏ chuột
           # self.screen.blit(current_tile_img,(tile_pos[0]*self.tilemap.tile_size-self.scroll[0],tile_pos[1]*self.tilemap.tile_size-self.scroll[1]))




            #hiện tile map trc con trỏ chuột nhưng hình dung được vị trí nó luôn
            if self.ongrid:
                self.screen.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:# chỉ hiện ra ở vị trí con trỏ và ko thể click
                self.screen.blit(current_tile_img, mpos)


            if self.clicking and self.ongrid: # thêm tile map
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}

            if self.right_clicking: # xóa tile map
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                #xóa tile ngoài grid
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    #xac dinh vùng
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)

            self.screen.blit(current_tile_img,(5,5))


            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    pygame.quit()

                    sys.exit()


                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: #chuot trai
                        self.clicking = True 
                        if not self.ongrid:
                            #click có thể đặt tile linh tinh ko theo grid
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
                    if event.button == 3: #chout phai
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                           self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:#scroll chuoej len
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list) # vòng lặp quay lại
                            self.tile_variant = 0
                        if event.button == 5:#scroll chuot xuong
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0



                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_o:
                        self.tilemap.save('3.json')
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
            pygame.display.update()
            self.clock.tick(100) # duy trì tốc độ 60FPS
Editor().run()