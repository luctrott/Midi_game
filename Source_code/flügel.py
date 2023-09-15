from LCDHandler import LCDHandler
from CustomChars import CustomChars
from FileManager import FileManager
from ProgressBar import ProgressBar

import time

class main:
    def __init__(self,game) -> None:
        self._game=game
        self.__filemanager=FileManager()
        self.__lcd=LCDHandler(game)
        self.__lcd.create_char(0,CustomChars.char0)
        self.__lcd.create_char(1,CustomChars.char1)
        self.__lcd.create_char(2,CustomChars.char2)
        self.__lcd.create_char(3,CustomChars.char3)
        self.__lcd.create_char(4,CustomChars.char4)
        self.__lcd.create_char(5,CustomChars.char5)
        self.__lcd.create_char(6,CustomChars.char6)
        self.__proggres_bar=ProgressBar(self.__lcd)
        self.__closed=False
        self.__proggres_bar.force_reload()
        self.__draw_frame(incrementel=False)
    
    def __center_text(self,text:str,fill:str=" ",lenth:int=20)->str:
        if len(text)<lenth:
            text=fill*int((lenth-len(text))/2)+text+fill*int((lenth-len(text))/2)
        if len(text)<lenth:
            text=text+fill
        return text
        
    def __draw_frame(self, text:str=None, incrementel:bool=True)->None:
        self.__lcd.cursor_pos=(0,0)
        if text is None:
            self.__lcd.write_string("-"*20)
        else:
            self.__lcd.write_string(self.__center_text(text,fill="-"))
        if not incrementel:
            self.__lcd.cursor_pos=(0,3)
            self.__lcd.write_string("-"*20)
            self.__lcd.cursor_pos=(0,1)
            self.__lcd.write_string("|")
            self.__lcd.cursor_pos=(19,1)
            self.__lcd.write_string("|")
            self.__lcd.cursor_pos=(0,2)
            self.__lcd.write_string("|")
            self.__lcd.cursor_pos=(19,2)
            self.__lcd.write_string("|")

    def close(self) -> None:
        self.__lcd.close()
        self.__filemanager.close()
        self.__closed=True
    
    def run_logic(self)->None:

        while self.__closed==False:
            time.sleep(1)
    