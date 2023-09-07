from UsbManager import UsbManager
from LogicSettings import LogicSettings
from RuntimeVariables import RuntimeVariables
import os

class FileManager(UsbManager):
    def __init__(self):
        super().__init__()
        self.__internal_files = self.__load_all_mid(LogicSettings.onboard_dir)
        self.__usb_files = self.__load_all_mid(LogicSettings.usb_dir)
        self.__current_file = None
        self._on_dev_added = self.__on_dev_added
        self._on_dev_removed = self.__on_dev_removed
        self.tasks_on_dev_added=[]
        self.tasks_on_dev_removed=[]
    
    @property
    def mode(self)->int:
        return RuntimeVariables.mode
    
    @mode.setter
    def mode(self,value:int)->None:
        RuntimeVariables.mode=value
    
    
    def __load_all_mid(self,path:str)->list:
        files = []
        #Files including subfolders
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".mid"):
                    files.append(os.path.join(root, file))
        return files
    
    def __on_dev_added(self)->None:
        self.__usb_files = self.__load_all_mid(LogicSettings.usb_dir)
        for task in self.tasks_on_dev_added:
            if callable(task):
                task()
            else:
                print("Error: A task on_added is not callable")
    
    def __on_dev_removed(self)->None:
        self.__usb_files = self.__load_all_mid(LogicSettings.usb_dir)
        for task in self.tasks_on_dev_removed:
            if callable(task):
                task()
            else:
                print("Error: A task on_removed is not callable")

