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
        self.__progress_bar_chars=['\x00','\x01','\x02','\x03','\x04']
        self.__progress=0
        self.__progress_bar_curent_chars=[]
        for _ in range(10):
            self.__progress_bar_curent_chars.append(self.__progress_bar_chars[0])
        self.__draw_progress_bar(-1,False)
    
    def __draw_progress_bar(self,progress:int,incremental:bool=True)->None:
        #progress: -1=-1, 0=0, 100=30
        if progress!= -1 and progress>0:
            progress=round(progress/3)

        if progress != self.__progress or not incremental:
            self.__progress=progress
            tmp=self.__progress_bar_curent_chars.copy()
            if progress == -1:

                for i in range(10):
                    tmp[i]=self.__progress_bar_chars[0]
            elif  progress == 0:
                for i in range(10):
                    tmp[i]=self.__progress_bar_chars[1]
            elif progress == 30:
                for i in range(10):
                    tmp[i]=self.__progress_bar_chars[4]
            else:
                a=int(progress/3)
                b=progress-(a*3)

                if not incremental:
                    for i in range(a):
                        tmp[i]=self.__progress_bar_chars[1]
                elif a>0:
                    tmp[a-1]=self.__progress_bar_chars[4]
                tmp[a]=self.__progress_bar_chars[b+1]
            if incremental:
                for i in range(10):
                    if tmp[i]!=self.__progress_bar_curent_chars[i]:
                        self.__progress_bar_curent_chars[i]=tmp[i]
                        self.__lcd.cursor_pos=(i+5,3)
                        self.__lcd.write_string(tmp[i])
            else:
                self.__progress_bar_curent_chars=tmp.copy()
                self.__lcd.cursor_pos=(5,3)
                self.__lcd.write_string(''.join(tmp))

    def close(self) -> None:
        self.__lcd.close()
        self.__filemanager.close()
    
    def run_logic(self)->None:
        c=-1
        while self._game.running:
            self.__draw_progress_bar(c)
            time.sleep(2)
            c+=1
        self.close()