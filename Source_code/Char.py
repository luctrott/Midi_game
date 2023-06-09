import pygame
from Settings import Settings
from Pixel import Pixel
class Char:
    def __init__(self,screen) -> None:
        self.screen=screen
        self.rect=pygame.rect.Rect(0,0,Settings.char_size[0],Settings.char_size[1])
        self.pixels=[]
    
    def _create_pixels(self):
        self.pixels=[]
        for x in range(Settings.char_res[0]):
            a=int(self.rect.topleft[0]+((self.rect.width/Settings.char_res[0])*x+(self.rect.width/(Settings.char_res[0]*2))))
            
            for y in range(Settings.char_res[1]):
                b=int(self.rect.topleft[1]+((self.rect.height/Settings.char_res[1])*y+(self.rect.height/(Settings.char_res[1]*2))))
                pos=[a,b]
                #print(pos)
                tmp=Pixel(self.screen)
                tmp.center=pos.copy()
                tmp.state=True
                tmp.backlight=False
                self.pixels.append(tmp)
    def write_bitmap(self,bitmap:list):
                x=0
                #bitmap=[[True,True,True,True,True,True,True,True],[True,True,True,True,True,True,True,True],[True,True,True,True,True,True,True,True],[True,True,True,True,True,True,True,True],[True,True,True,True,True,True,True,True]]
               
                for a in bitmap:
                    for b in a:
                        self.pixels[x].state=b
                        x+=1
    def clear(self):
        for i in self.pixels:
            i.state=False

    def draw(self):
        for i in self.pixels:
            i.draw()
    def set_backlight(self,on:bool):
        for i in self.pixels:
            i.backlight=on
