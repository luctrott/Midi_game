from LogicSettings import LogicSettings
import os

def __mkdir(path)->None:
    if not os.path.exists(path):
        os.mkdir(path)

def create_folder()->None:
    __mkdir(LogicSettings.dev_dir)
    __mkdir(LogicSettings.usb_dir)
    __mkdir(LogicSettings.onboard_dir)
if __name__ == "__main__":
    create_folder()
    print("Done")