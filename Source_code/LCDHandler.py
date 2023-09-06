from main import Game
import threading
import functools

class LCDHandler:
    def __init__(self,game:Game)->None:
        self.__lcd=game.lcd
        self.__thread=threading.Thread(target=self.__run,daemon=True)
        self.__closed=False
        self.__work=threading.Event()
        self.__work.set()
        self.__tasks=[]
        self.__lcd.init()
        self.__backlight=self.__lcd.backlight_enable
    
    def __run(self) ->None:
        while not self.__closed:
            self.__work.wait()
            for t in self.__tasks:
                if callable(t):
                    t()
                else:
                    print("not callable task in lcd_handler")

                self.__tasks.remove(t)
            if len(self.__tasks)==0:
                self.__work.clear()


    @property
    def backlight_enable(self)->bool:
        return self.__backlight
    
    @backlight_enable.setter
    def backlight_enable(self,on:bool)->None:
        self.__tasks.append(functools.partial(self.__backlight_enable,on))
        self.__work.set()
        self.__backlight=on

    def __backlight_enable(self,on:bool)->None:
        self.__lcd.backlight_enable=on
    
    def clear(self)->None:
        self.__tasks.append(self.__lcd.clear)
        self.__work.set()
    
    def create_char(self,num:int,bitmap:tuple)->None:
        self.__tasks.append(functools.partial(self.__lcd.create_char,num,bitmap))
        self.__work.set()
    
    def __set_cursor_pos(self,x:int,y:int)->None:
        self.__lcd.cursor_pos=[x,y]
    
    @property
    def cursor_pos(self)->tuple[int,int]:
        return self.__lcd.cursor_pos
    
    @cursor_pos.setter
    def cursor_pos(self,pos:tuple[int,int])->None:
        self.__tasks.append(functools.partial(self.__set_cursor_pos,pos[0],pos[1]))
        self.__work.set()
    
    def write_string(self,text:str)->None:
        self.__tasks.append(functools.partial(self.__lcd.write_string,text))
        self.__work.set()
    

    def close(self)->None:
        self.__closed=True
        self.__work.set()
        self.__thread.join()
        self.__lcd.close()