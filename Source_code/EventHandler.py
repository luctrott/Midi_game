from RuntimeVariables import RuntimeVariables
from   Settings import Settings
import threading
import time


class EventHandler:
    def __init__(self) -> None:
        self.__thread=threading.Thread(target=self.__run,daemon=True)
        self.__closed=False
        self.__closing_event=threading.Event()
        self.__last_eventtime=0
        self.__wait=threading.Event()
        
    
    def __event_callback(self):
        self.__last_eventtime=time.time()
        self.__wait.set()
    
    def __run(self):
        while not self.__closed:
            self.__wait.wait()
            if RuntimeVariables.screen==1 or RuntimeVariables.screen>=30:
                self.__wait.clear()
            elif (time.time()-self.__last_eventtime)>=Settings.event_time:
                print("Home")
                RuntimeVariables.screen==1

    def start(self):
        RuntimeVariables.event_callback = self.__event_callback
        self.__last_eventtime=time.time()
        self.__thread.start()
    
    def close(self):
        self.__closed=True
        self.__wait.set()
        self.__thread.join()
    
        
        
        