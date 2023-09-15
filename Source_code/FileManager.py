from UsbManager import UsbManager
from LogicSettings import LogicSettings
from RuntimeVariables import RuntimeVariables
import os
import random

class FileManager(UsbManager):
    def __init__(self):
        
        self.__files_to_use = []
        self.__current_file = None
        self.tasks_on_dev_added=[]
        self.tasks_on_dev_removed=[]
        self.__mode=0
        self.__tracklist=[]
        self.__index=0
        self.round_completed_task=None
        self.__internal_files = ["Start"]
        super().__init__()
        self.__internal_files = self.__load_all_mid(LogicSettings.onboard_dir)
        self.__update()
    
    @property
    def mode(self)->int:
        return self.__mode
    
    @mode.setter
    #["one","all","random","all_loop","random_loop"]
    def mode(self,value:int)->None:
        self.__mode=value
        self.__update()

    def __get_files(self)->None:
        if len(self.__usb_files)>0:
            self.__files_to_use=self.__usb_files.copy()
        elif len(self.__internal_files)>0:
            self.__files_to_use=self.__internal_files.copy()
        else:
            RuntimeVariables.error_message="No files found"
            RuntimeVariables.error=True
    
    def __shuffle(self,ls:list,start_with_current:bool=False)->list:
        tmp=ls.copy()
        a=self.__current_file in tmp

        if start_with_current and a:
                tmp.remove(self.__current_file)
                random.shuffle(tmp)
                tmp.insert(0,self.__current_file)
        else:
            random.shuffle(tmp)
            if a:
                if self.__current_file == tmp[0]:
                    t=random.randint(1,len(tmp)-1)
                    tmp[0],tmp[t]=tmp[t],tmp[0]
        return tmp
    
    def __update(self)->None:
        self.__get_files()
        if self.__mode==2 or self.__mode==4:
            self.__tracklist=self.__shuffle(self.__files_to_use)
        else:
            self.__tracklist=self.__files_to_use.copy()

        self.__shuffle(self.__files_to_use,start_with_current=True)
        self.__current_file=self.__tracklist[0]
        self.__index=0
        
    def __load_all_mid(self,path:str)->list:
        files = []
        #Files including subfolders
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".mid"):
                    files.append(os.path.join(root, file))
        return files
    
    def _on_dev_added(self)->None:
        super()._on_dev_added()
        self.__usb_files = self.__load_all_mid(LogicSettings.usb_dir)
        self.__update()
        for task in self.tasks_on_dev_added:
            if callable(task):
                task()
            else:
                print("Error: A task on_added is not callable")
    
    def _on_dev_removed(self)->None:
        super()._on_dev_removed()
        self.__usb_files = self.__load_all_mid(LogicSettings.usb_dir)
        self.__update()
        for task in self.tasks_on_dev_removed:
            if callable(task):
                task()
            else:
                print("Error: A task on_removed is not callable")
    
    def next(self)->str:
        if self.__mode==2 or self.__mode==4:
            self.__index+=1
            if self.__index>=len(self.__tracklist):
                self.__index=0
                if not self.__mode>2:
                    if callable(self.round_completed_task):
                        self.round_completed_task()
                self.__tracklist=self.__shuffle(self.__files_to_use,False)
            self.__current_file=self.__tracklist[self.__index]
        else:
            self.__index+=1
            if self.__index>=len(self.__tracklist):
                self.__index=0
                if not self.__mode>2:
                    if callable(self.round_completed_task):
                        self.round_completed_task()
                self.__current_file=self.__tracklist[self.__index]
        return self.__current_file
    
    def previous(self)->str:
        if self.__mode==2 or self.__mode==4:
            self.__index-=1
            if self.__index<0:
                self.__index=len(self.__tracklist)-1
                self.__tracklist=self.__shuffle(self.__files_to_use,False)
            self.__current_file=self.__tracklist[self.__index]
        else:
            self.__index-=1
            if self.__index<0:
                self.__index=len(self.__tracklist)-1
            self.__current_file=self.__tracklist[self.__index]
        return self.__current_file
    
    def home(self)->str:
        self.__index=0
        if self.__mode==2 or self.__mode==4:
            self.__tracklist=self.__shuffle(self.__files_to_use,False)
        self.__current_file=self.__tracklist[self.__index]
        return self.__current_file
    
    def get_current_file(self)->str:
        return self.__current_file
