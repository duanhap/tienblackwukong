import pygame
import os
base_path = os.path.dirname(__file__).removesuffix('scripts')
def get_frame(sheet, frame, width, height, scale):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((width * frame), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey((0, 0, 0))

    return image
def get_frames(path,scale):
    images=[]
    sprite_sheet_image = pygame.image.load(os.path.join(base_path+'data'+path + '.png')).convert_alpha()
    animation_steps = int (sprite_sheet_image.get_width() / sprite_sheet_image.get_height())

    for x in range(animation_steps):
        images.append(get_frame(sprite_sheet_image,x, sprite_sheet_image.get_height(), sprite_sheet_image.get_height(), scale))
    return images


    

class Animation2:
    def __init__(self,animation_list,img_dur=5,loop=True):

        self.frame =0
        self.img_duration = img_dur
        self.loop = loop
        self.doneToDoSomething = False
        self.done = False
        self.framecuoi=[1,1]
        self.animation_list = animation_list
     
    def copy(self):
        return(Animation2(self.animation_list,self.img_duration,self.loop))
    def update(self):
        if self.loop:
            self.frame =  (self.frame+1)%(self.img_duration*len(self.animation_list))
        else:
            self.frame = min(self.frame +1 ,self.img_duration *len(self.animation_list)-1)
            if self.frame >= self.img_duration*len(self.animation_list) - 1:
                self.done = True
            if self.frame >= self.img_duration*len(self.animation_list) - self.framecuoi[0] and self.frame <= self.img_duration*len(self.animation_list) - self.framecuoi[1] :
                self.doneToDoSomething = True   
    def img(self):
        return self.animation_list[int(self.frame/self.img_duration)]

