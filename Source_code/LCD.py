import pygame
from Pygame_Settings import Settings
from Char import Char
from LCDCharmap import LCDCharmap
class LCD:
    
    def __init__(self,screen,charmap:LCDCharmap) -> None:
        self.screen=screen
        self.charmap=charmap
        self.chars=[]
        self.lcd_rect=pygame.rect.Rect(0,0,Settings.lcd_size[0],Settings.lcd_size[1])
        self.__backlight=False    
        self.cursor_pos:list=[0,0]
    
    def init(self):
        print("LCD init")
    
    def create_lcd(self):
        self.chars=[]
        for x in range(Settings.lcd_chars[0]):
            tmp=[]
            a=int(self.lcd_rect.topleft[0]+((self.lcd_rect.width/Settings.lcd_chars[0])*x+(self.lcd_rect.width/(Settings.lcd_chars[0]*2))))
            for y in range(Settings.lcd_chars[1]):
                b=int(self.lcd_rect.topleft[1]+((self.lcd_rect.height/Settings.lcd_chars[1])*y+(self.lcd_rect.height/(Settings.lcd_chars[1]*2))))
                pos=[a,b]
                char=Char(self.screen)
                char.rect.center=pos.copy()
                char._create_pixels()
                char.set_backlight(self.__backlight)
                char.clear()
                tmp.append(char)
            self.chars.append(tmp)
    
    def write_bitmap(self,bitmap:list,x:int,y:int):
        try:
            self.chars[x][y].write_bitmap(bitmap)
        except IndexError:
            print(f"IndexError: {x},{y}: {len(self.chars)}")
    
    def clear(self):
        for x in self.chars:
            for y in x:
                y.clear()
    
    def draw(self):
        if self.__backlight:
            pygame.draw.rect(self.screen,Settings.br_color_on,self.lcd_rect)
        else:
            pygame.draw.rect(self.screen,Settings.br_color_off,self.lcd_rect)

        for x in self.chars:
            for y in x:
                y.draw()

    @property
    def backlight_enable(self)->bool:
        return self.__backlight

    @backlight_enable.setter    
    def set_backlight(self,on:bool):
        for x in self.chars:
            for y in x:
                y.set_backlight(on)
        self.__backlight=on
    
    def __print(self,text:str):
        for i in text:
            self.write_bitmap(self.charmap.get_charmap_from_char(i),self.cursor_pos[0],self.cursor_pos[1])
            self.cursor_pos[0]+=1
            if self.cursor_pos[0]>=Settings.lcd_chars[0]:
                self.cursor_pos[0]=0
                self.cursor_pos[1]+=1
            if self.cursor_pos[1]>=Settings.lcd_chars[1]:
                self.cursor_pos[1]=0
                
    def create_char(self,num:int,bitmap:tuple):
        self.charmap.create_custom_char(num,bitmap) 

    def write_string(self,st):
        self.__print(st)
    
    def close(self):
        print("LCD closed")