#from main import Game
from LCDHandler import LCDHandler
from CustomChars import CustomChars

class main:
    def __init__(self,game) -> None:
        self._game=game
        self.__lcd=LCDHandler(game)
        self.__lcd.create_char(0,CustomChars.char0)
        self.__lcd.create_char(1,CustomChars.char1)
        self.__lcd.create_char(2,CustomChars.char2)
        self.__lcd.create_char(3,CustomChars.char3)
        self.__lcd.create_char(4,CustomChars.char4)
        self.__lcd.create_char(5,CustomChars.char5)
        self.__lcd.create_char(6,CustomChars.char6)
        self.__progress_bar_chars=['\x01','\x02','\x03','\x04']
        
    def close(self) -> None:
        self.__lcd.close()
        