
#map
import json
import pygame

AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2, 
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone','grass2', 'stone2'}
AUTOTILE_TYPES = {'grass', 'stone','grass2', 'stone2'}


class Tilemap:
    def __init__(self,game,tile_size = 50):
        self.game= game
        self.tile_size = tile_size # kich thươc môi ô vuong trong bản đồ
        self.tilemap ={}#KIEU DICHtionary giong map trong c++
        self.offgrid_tiles =[]


    #trích xuất tile map , xem có nên giữ hay bỏ , hay thêm hịu ứng 
    # 1 cai là on grid 2 là off grid 
    def extract(self, id_pairs, keep=False):
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)
                    
        for loc in self.tilemap.copy():
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]
        
        return matches

    # check solid xem eneymy còn ở trên vùng di đc ko
    def solid_check(self, pos):
        tile_loc = str(int(pos[0] // self.tile_size)) + ';' + str(int(pos[1] // self.tile_size))
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]['type'] in PHYSICS_TILES:
                return self.tilemap[tile_loc]
            
             
    #save và load map  và tự động điền map       
    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
        f.close()
        
    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()
        
        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']

    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] == tile['type']:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile['variant'] = AUTOTILE_MAP[neighbors]



#collision
    # xét xung quang 1 vị trí xem có tilemap nào ko lưu vào tiles
    def tiles_around(self,pos):
        tiles =[]

        tile_loc = (int(pos[0]//self.tile_size),int(pos[1]//self.tile_size))#make the pixel position into a grid position 50 50 .. 1 1 , 75 125 .. 1 2
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0]+offset[0])+';' +str(tile_loc[1]+offset[1])
            if check_loc in self.tilemap:#if tồn tại
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    #nếu cái tile đó là loại chạm được thì sét khung
    def physics_rects_around(self,pos,xetVariant = 0):
        rects=[]
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                if xetVariant==2:
                    if tile['variant'] == 0 or tile['variant'] == 1 or tile['variant'] == 2 or tile['variant'] == 5  or tile['variant'] == 8:
                        rects.append(pygame.Rect(tile['pos'][0]*self.tile_size,tile['pos'][1]*self.tile_size,self.tile_size,self.tile_size))# x,y,kt,kt
                if xetVariant ==1:
                    if tile['variant'] != 0 and tile['variant'] != 1 and tile['variant'] != 2 and tile['variant'] != 5  and tile['variant'] != 8:
                       rects.append(pygame.Rect(tile['pos'][0]*self.tile_size,tile['pos'][1]*self.tile_size,self.tile_size,self.tile_size))# x,y,kt,kt
      
        return rects
   
#render
    def render(self,surf,offset=(0,0)):


        for tile in self.offgrid_tiles:
           surf.blit(self.game.assets[tile['type']][tile['variant']],(tile['pos'][0]-offset[0],tile['pos'][1]-offset[1]))

        #optimize  Chỉ vẽ những tile nằm trong phạm vi nhìn thấy của camera
        for x in range(offset[0]//self.tile_size,(offset[0]+ surf.get_width())//self.tile_size+1):
            for y in range(offset[1]//self.tile_size,(offset[1]+ surf.get_height())//self.tile_size+1):
                loc = str(x) +';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']],(tile['pos'][0]*self.tile_size-offset[0],tile['pos'][1]*self.tile_size-offset[1])) 
            
        
       
   #  vẽ hết tile sẵn có     
 #       for loc in self.tilemap:
  #          tile = self.tilemap[loc]
  #          surf.blit(self.game.assets[tile['type']][tile['variant']],(tile['pos'][0]*self.tile_size-offset[0],tile['pos'][1]*self.tile_size-offset[1])) 
       