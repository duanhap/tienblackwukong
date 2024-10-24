#tien ich
import pygame
import os

BASE_IMG_PATH = 'data/images/'

def load_image(path,size=None,bg=None,scale=None):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
   # img.set_colorkey((0,0,0)) # xóa nền ảnh
    img.set_colorkey(bg)
    if scale:
        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
    if size:
        img = pygame.transform.scale(img, size)
    return img
def load_images(path,size=None,bg=None,scale=None):
    images = []
    full_path = BASE_IMG_PATH + path

    for entry in sorted(os.scandir(full_path), key=lambda e: e.name):#sap xep theo name png
        # Thay vì sử dụng os.listdir, os.scandir trả về một iterator
        #  cho phép bạn dễ dàng kiểm tra xem một entry là file hay thư mục.
        if entry.is_dir():
            # Nếu là thư mục, đệ quy để tải hình ảnh bên trong thư mục con
            images.append(load_images(path + '/' + entry.name))
        elif entry.is_file():
            # Nếu là file, nạp hình ảnh
            images.append(load_image(path + '/' +  entry.name,size,bg,scale))

    return images
class Animation:
    def __init__(self,images,img_dur=5,loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.doneToDoSomething = False
        self.done = False
        self.frame = 0
        self.framecuoi=[1,1]
        

    def copy(self):
        return(Animation(self.images,self.img_duration,self.loop))    
    def update(self):
        if self.loop:
            self.frame =  (self.frame+1)%(self.img_duration*len(self.images))
        else:
            self.frame = min(self.frame +1 ,self.img_duration *len(self.images)-1)
            if self.frame >= self.img_duration*len(self.images) - 1:
                self.done = True
            if self.frame >= self.img_duration*len(self.images) - self.framecuoi[0] and self.frame <= self.img_duration*len(self.images) - self.framecuoi[1] :
                self.doneToDoSomething = True   
    def img(self):
        return self.images[int(self.frame/self.img_duration)]