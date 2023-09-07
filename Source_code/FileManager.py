from UsbManager import UsbManager
from LogicSettings import LogicSettings
import os

class FileManager(UsbManager):
    def __init__(self):
        super().__init__()
        self.__internal_files = self.__load_all_mid(LogicSettings.onboard_dir)
        self.__usb_files = self.__load_all_mid(LogicSettings.usb_dir)
    
    

    def __load_all_mid(self,path:str)->list:
        files = []
        #Files including subfolders
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".mid"):
                    files.append(os.path.join(root, file))
        return files