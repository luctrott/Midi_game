import pygame
from Pygame_Settings import Pygame_Settings as Settings
class Pixel:
    def __init__(self,screen) -> None:
        self.screen=screen
        self.backlight=False
        self.state=False
        self.center=(0,0)
        self._rect=pygame.rect.Rect(0,0,Settings.pix_size[0],Settings.pix_size[1])
    def draw(self):
        if self.backlight:
            if self.state:
                self.__pix(Settings.pix_color_on_on)
            else:
                self.__pix(Settings.pix_color_on_off)
        else:
            if self.state:
                self.__pix(Settings.pix_color_off_on)
            else:
                self.__pix(Settings.pix_color_off_off)

    def __pix(self,color):
        self._rect.center=self.center
        #print(self._rect.center)
        pygame.draw.rect(self.screen,color,self._rect,0)
        
