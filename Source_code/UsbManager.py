from LogicSettings import LogicSettings
import shutil
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#https://stackoverflow.com/questions/18599339/python-watchdog-monitoring-file-for-changes

class MyHandler(FileSystemEventHandler):
        def __init__(self):
            super().__init__()
            self.to_call_when_added=None
            self.to_call_when_removed=None

        def on_created(self, event)->None:
            if callable(self.to_call_when_added):
                self.to_call_when_added()
        
        def on_deleted(self, event)->None:
            if callable(self.to_call_when_removed):
                self.to_call_when_removed()

class UsbManager:
    def __init__(self):
        self.__event_handler_dev = MyHandler()
        self.__observer_dev = Observer()
        self.__observer_dev.schedule(self.__event_handler_dev, path=LogicSettings.dev_dir, recursive=False)
        self.__observer_dev.start()
        self.__event_handler_dev.to_call_when_added=self._on_dev_added
        self.__event_handler_dev.to_call_when_removed=self._on_dev_removed
        self.__devs=[]
        self._changed=False
        self.__init()
        self._on_dev_added()
        
    
    def __init(self)->None:
        for dev in os.listdir(LogicSettings.usb_dir):
            self.__unmount(dev)
    
    def _on_dev_added(self)->None:
        
        for dev in os.listdir(LogicSettings.dev_dir):
            if len(dev)>3 <5:
                if "sd" in dev:
                    if dev not in self.__devs:
                        self.__mount(dev)
                        self.__devs.append(dev)
                        self._changed=True

    def _on_dev_removed(self)->None:
        tmp= os.listdir(LogicSettings.dev_dir)
        for dev in self.__devs:
            if dev not in tmp:
                self.__unmount(dev)
                self.__devs.remove(dev)
                self._changed=True
        
    
    def __mount(self,dev)->None:
        print("Mounting "+dev)
        if not os.path.exists(LogicSettings.usb_dir+dev):
            os.mkdir(LogicSettings.usb_dir+dev)
        else:
            print("Error: "+LogicSettings.usb_dir+dev+" already exists")
    
    def __unmount(self,dev)->None:
        print("Unmounting "+dev)
        if os.path.exists(LogicSettings.usb_dir+dev):
            shutil.rmtree(LogicSettings.usb_dir+dev)
        else:
            print("Error: "+LogicSettings.usb_dir+dev+" does not exist")
        

    @property
    def dev_count(self)->int:
        return len(self.__devs)    

    def close(self)->None:
        self.__observer_dev.stop()
        self.__observer_dev.join()
        for dev in self.__devs:
            self.__unmount(dev)


if __name__ == "__main__":
    usb_manager=UsbManager()
    input("Press enter to close")
    usb_manager.close()