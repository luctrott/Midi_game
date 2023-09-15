from LCDHandler import LCDHandler
from CustomChars import CustomChars
from FileManager import FileManager
from ProgressBar import ProgressBar
from Frames import Frames

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
        self.__frames=Frames(self.__lcd)
        self.__closed=False
        self.__proggres_bar.force_reload()
        

    def close(self) -> None:
        self.__lcd.close()
        self.__filemanager.close()
        self.__closed=True
    
    def run_logic(self)->None:

        while self.__closed==False:
            self.__frames.volume(int(input("volume: ")))
    