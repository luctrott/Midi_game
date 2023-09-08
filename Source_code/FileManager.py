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
        self.tasks_on_dev_added=[]
        self.tasks_on_dev_removed=[]
        self._mode=0
    
    @property
    def mode(self)->int:
        return self._mode
    
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

