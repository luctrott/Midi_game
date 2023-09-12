from UsbManager import UsbManager
from LogicSettings import LogicSettings
from RuntimeVariables import RuntimeVariables
import os
import random

class FileManager(UsbManager):
    def __init__(self):
        super().__init__()
        self.__internal_files = self.__load_all_mid(LogicSettings.onboard_dir)
        self.__files_to_use = []
        self.__current_file = None
        self.tasks_on_dev_added=[]
        self.tasks_on_dev_removed=[]
        self._mode=0
    
    @property
    def mode(self)->int:
        return self._mode
    
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
    def __update(self)->None:
        self.__get_files()
        self.__shuffle(self.__files_to_use,start_with_current=True)
        self.__current_file=self.__files_to_use[0]

      




    @mode.setter
    def mode(self,value:int)->None:
        self._mode=value
    
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
        for task in self.tasks_on_dev_added:
            if callable(task):
                task()
            else:
                print("Error: A task on_added is not callable")
    
    def _on_dev_removed(self)->None:
        super()._on_dev_removed()
        self.__usb_files = self.__load_all_mid(LogicSettings.usb_dir)
        for task in self.tasks_on_dev_removed:
            if callable(task):
                task()
            else:
                print("Error: A task on_removed is not callable")

