from LogicSettings import LogicSettings
import shutil
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#Calls a function when the content of a directory changes
#https://stackoverflow.com/questions/18599339/python-watchdog-monitoring-file-for-changes

class MyHandler(FileSystemEventHandler):
        def __init__(self):
            super().__init__()
            self.to_call_when_added=None
            self.to_call_when_removed=None

        def on_created(self, event):
            if callable(self.to_call_when_added):
                self.to_call_when_added()
        
        def on_deleted(self, event):
            if callable(self.to_call_when_removed):
                self.to_call_when_removed()

class UsbManager:
    def __init__(self):
        self.__event_handler_dev = MyHandler()
        self.__observer_dev = Observer()
        self.__observer_dev.schedule(self.__event_handler_dev, path=LogicSettings.dev_dir, recursive=False)
        self.__observer_dev.start()
        self.__event_handler_dev.to_call_when_added=self.__on_dev_added
        self.__event_handler_dev.to_call_when_removed=self.__on_dev_removed
        self.__devs=[]
    
    def __on_dev_added(self):
        
        a=False
        for dev in os.listdir(LogicSettings.dev_dir):
            if len(dev)>3 <5:
                if "sd" in dev:
                    if dev not in self.__devs:
                        self.__mount(dev)
                        self.__devs.append(dev)
                        a=True

    
    def __on_dev_removed(self):
        tmp= os.listdir(LogicSettings.dev_dir)
        a=False
        for dev in self.__devs:
            if dev not in tmp:
                self.__unmount(dev)
                self.__devs.remove(dev)
                a=True
    
    def __mount(self,dev):
        print("Mounting "+dev)
        #shutil.copytree(LogicSettings.dev_dir+dev,LogicSettings.mount_dir+dev)
    
    def __unmount(self,dev):
        print("Unmounting "+dev)
        #shutil.rmtree(LogicSettings.mount_dir+dev)
    
    def close(self):
        self.__observer_dev.stop()
        self.__observer_dev.join()


if __name__ == "__main__":
    file_manager=UsbManager()
    input("Press enter to close")
    file_manager.close()