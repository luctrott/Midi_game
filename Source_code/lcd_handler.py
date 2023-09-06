from main import Game
import threading

class Lcd_handler:
    def __init__(self,game:Game)->None:
        self.__lcd=game.lcd
        self.__thread=threading.Thread(target=self.__run,daemon=True)
        self.__closed=False
        self.__work=threading.Event()
        self.__work.set()
        self.__tasks=[]
    
    def __run(self) ->None:
        while not self.__closed:
            self.__work.wait()
