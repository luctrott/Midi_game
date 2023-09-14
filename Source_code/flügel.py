from LCDHandler import LCDHandler
from CustomChars import CustomChars
from FileManager import FileManager
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
        time.sleep(1)
        self.__progress_bar_chars=['\x01','\x02','\x03','\x04']
        self.__progress=0
        self.__progress_bar_curent_chars=[]
        self.__draw_progress_bar(1)
    
    def __draw_progress_bar(self,progress:int)->None:
        if progress != self.__progress:
            self.__progress=progress
            tmp=[]
            self.__lcd.cursor_pos=(0,1)
            for char in self.__progress_bar_chars:
                self.__lcd.write_string(char)
                

                
                    

            
    def close(self) -> None:
        self.__lcd.close()
        self.__filemanager.close()
        