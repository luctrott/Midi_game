import pygame
from pyga.Pygame_Settings import Pygame_Settings as Settings
from pyga.LCDCharmap import LCDCharmap
from pyga.LCD import LCD
from pyga.Button import Button
import os
import shutil
import tkinter as tk
from tkinter import filedialog
from LogicSettings import LogicSettings
class Game:
    def __init__(self) -> None:
        pygame.init()
        
        self.surface=pygame.display.set_mode(Settings.window_size)
        self.surface_rect=self.surface.get_rect()

        pygame.display.set_caption("Midi Test")

        self.surface.fill((255,0,0))
        self.charmap=LCDCharmap()
        self.lcd=LCD(self.surface,self.charmap)
        self.lcd.lcd_rect.center=(self.surface_rect.centerx,self.surface_rect.centery+10)
        self.lcd.create_lcd()
        

        self.buttons=[]
        self.buttons_rect=pygame.rect.Rect(0,0,1,1)
        self.buttons_rect.center=(self.surface_rect.center[0],self.surface_rect.height-120)
        tmp=Button(self.surface,"Start/Pause")
        tmp.rect.center=(self.buttons_rect.centerx,self.buttons_rect.centery)
        self.buttons.append(tmp)
        tmp=Button(self.surface,"Stop")
        tmp.rect.center=(self.buttons_rect.centerx-240,self.buttons_rect.centery+60)
        self.buttons.append(tmp)
        tmp=Button(self.surface,"Forw")
        tmp.rect.center=(self.buttons_rect.centerx+120,self.buttons_rect.centery)
        self.buttons.append(tmp)
        tmp=Button(self.surface,"Back")
        tmp.rect.center=(self.buttons_rect.centerx-120,self.buttons_rect.centery)
        self.buttons.append(tmp)
        tmp=Button(self.surface,"Vol-")
        tmp.rect.center=(self.buttons_rect.centerx+240,self.buttons_rect.centery+60)
        self.buttons.append(tmp)
        tmp=Button(self.surface,"Vol+")
        tmp.rect.center=(self.buttons_rect.centerx+240,self.buttons_rect.centery-60)
        self.buttons.append(tmp)
        tmp=Button(self.surface,"Mode")
        tmp.rect.center=(self.buttons_rect.centerx-240,self.buttons_rect.centery-60)
        self.buttons.append(tmp)

        self.eject_b=Button(self.surface,"Eject")
        self.eject_b.rect.center=(self.buttons_rect.centerx-60,60)
        self.buttons.append(self.eject_b)
        self.eject_b.when_pressed=self.eject
        self.open_b=Button(self.surface,"Open")
        self.open_b.rect.center=(self.buttons_rect.centerx+60,60)
        self.open_b.when_pressed=self.open_f
        self.buttons.append(self.open_b)
        pygame.display.flip()
        self.running=True
        self.clock=pygame.time.Clock()
        self.fps=60
      
    def eject(self)->None:
        shutil.rmtree(LogicSettings.dev_dir)
        os.mkdir(LogicSettings.dev_dir)
        
        

    def open_f(self)->None:
        root=tk.Tk()
        root.withdraw()
        #Create a pygame event for mouse button up
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP,{'button':1}))
        path=filedialog.askdirectory()
        if path!="":
            temp=f"{LogicSettings.dev_dir}sda{len(os.listdir(LogicSettings.dev_dir))+1}/"
            shutil.copytree(path,temp,dirs_exist_ok=True)

        
    
    def run(self)->None:
        while self.running:
            self.clock.tick(self.fps)
            self.events()
            self.update()
            self.draw()
        pygame.quit()
        
    def events(self)->None:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.running=False
                os._exit(0)
            for i in self.buttons:
                i.check_for_press_or_release(event)

    def update(self)->None:
        for i in self.buttons:
            i.update()
        
    def draw(self)->None:
        self.surface.fill((0,0,255))
        for i in self.buttons:
            i.draw()
        self.lcd.draw()
        pygame.display.flip()
