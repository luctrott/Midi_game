from LogicSettings import LogicSettings
import threading
import shutil
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#Calls a function when the content of a directory changes
#https://stackoverflow.com/questions/18599339/python-watchdog-monitoring-file-for-changes

class __MyHandler(FileSystemEventHandler):
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

class FileManager:
    def __init__(self):
        self.__event_handler_dev = __MyHandler()
        self.__observer_dev = Observer()
        self.__observer_dev.schedule(self.__event_handler_dev, path=LogicSettings.dev_dir, recursive=False)
        self.__observer_dev.start()
        self.__event_handler_dev.to_call_when_added=self.__on_dev_added
        self.__event_handler_dev.to_call_when_removed=self.__on_dev_removed
    
    def __on_dev_added(self):
        print("dev added")
    
    def __on_dev_removed(self):
        print("dev removed")

    def close(self):
        self.__observer_dev.stop()
        self.__observer_dev.join()
        