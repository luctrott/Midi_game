import threading
import shutil
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
class FileManager:
    def __init__(self):
        pass

    def __chage_watcher(self):
        #Calls a function when the content of a directory changes

        #https://stackoverflow.com/questions/18599339/python-watchdog-monitoring-file-for-changes
