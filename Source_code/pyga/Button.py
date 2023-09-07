import pygame
import time
from threading import Thread,Event
class Button:
    def __init__(self,surface,name,held_time:float=3) -> None:
        self.surface=surface
        self.rect=pygame.rect.Rect(0,0,100,100)
        self.is_pressed=False
        self.name=name
        self.held_time=held_time
        self.when_pressed=None
        self.when_held=None
        self.color=(0,0,0)
        self.held=False
        self.__pr=Event()
        self.__pr.clear()
        self.__hd=Event()
        self.__hd.clear()
        self.__pr_thread=Thread(target=self.__when_pressed)
        self.__pr_thread.start()
        self.__hd_thread=Thread(target=self.__when_held)
        self.__hd_thread.start()
        
    def draw(self)->None:
        pygame.draw.rect(self.surface,self.color,self.rect,0)
        font=pygame.font.SysFont("Arial",int(self.rect.height/4))
        text=font.render(self.name,True,(255-self.color[0],255-self.color[1],255-self.color[2]))
        text_rect=text.get_rect()
        text_rect.center=self.rect.center
        self.surface.blit(text,text_rect)

    def update(self) -> None:
        if self.is_pressed:
            if time.time()-self.__held_time>=self.held_time:
                if not self.held:
                    self.color=(0,255,0)
                    self.__hd.set()
                    self.held=True
        else:
            self.held=False
            self.__held_time=time.time()


    def check_for_press_or_release(self,event)->None:
        if event.type==pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_pressed=True
                self.__pr.set()

                self.color=(255,255,255)
 
        if event.type==pygame.MOUSEBUTTONUP:
            self.is_pressed=False
            self.held=False
            self.__held_time=time.time()
            self.color=(0,0,0)
    
    def __when_pressed(self)->None:
        while True:
            self.__pr.wait()
            self.__pr.clear()
            if callable(self.when_pressed):
                self.when_pressed()
    
    def __when_held(self)->None:
        while True:
            self.__hd.wait()
            self.__hd.clear()
            if callable(self.when_held):
                self.when_held()
