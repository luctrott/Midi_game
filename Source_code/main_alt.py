import pygame
import time
from LCDCharmap import LCDCharmap
from Settings import Settings
from Char import Char
from LCD import LCD
from flügel import main
from threading import Thread
import os
from Button import Button
import shutil
import tkinter as tk
from tkinter import filedialog


class Game:
    def __init__(self) -> None:
        pygame.init()
        
        self.surface=pygame.display.set_mode(Settings.window_size)
        self.surface_rect=self.surface.get_rect()

        pygame.display.set_caption("Button Test")

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
      
    def eject(self):
        shutil.rmtree("dev")
        os.mkdir("dev")
        
        

    def open_f(self):
        root=tk.Tk()
        root.withdraw()
        #Create a pygame event for mouse button up
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP,{'button':1}))
        path=filedialog.askdirectory()
        if path!="":
            #shutil.copytree(src, dst, symlinks=False, ignore=None, copy_function=copy2, ignore_dangling_symlinks=False, dirs_exist_ok=False
            shutil.copytree(path,f"dev/{path.split('/')[-1]}",dirs_exist_ok=True)

        
    
    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.events()
            self.update()
            self.draw()
        pygame.quit()
    def events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.running=False
                os._exit(0)
            for i in self.buttons:
                i.check_for_press_or_release(event)
    def update(self):
        for i in self.buttons:
            i.update()
        
    def draw(self):
        self.surface.fill((0,0,255))
        for i in self.buttons:
            i.draw()
        self.lcd.draw()
        pygame.display.flip()
class Main:
    def __init__(self) -> None:
        self.game=Game()
        self.game.lcd.set_backlight(True)
        print("game done")
        self.main=main(self.game)
        print("main done")
        self.thread=Thread(target=self.run_logic)
        self.thread.start()
        print("init done")
        self.game.run()
    def run_logic(self):
        self.main.init()
        print(self.game.buttons[3].when_held)
        while self.game.running:
            time.sleep(1)

if __name__ == "__main__":    
    a=Main()
