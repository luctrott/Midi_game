from LCDHandler import LCDHandler
from RuntimeVariables import RuntimeVariables
class Frames:
    def __init__(self, lcd:LCDHandler):
        self.__lcd=lcd
        self.__last_volume=-1
    
    def __center_text(self,text:str,fill:str=" ",lenth:int=20)->str:
        if len(text)<lenth:
            text=fill*int((lenth-len(text))/2)+text+fill*int((lenth-len(text))/2)
        if len(text)<lenth:
            text=text+fill
        return text
        
    def _draw_frame(self, text:str=None, incrementel:bool=True)->None:
        self.__lcd.cursor_pos=(0,0)
        if text is None:
            self.__lcd.write_string("-"*20)
        else:
            self.__lcd.write_string(self.__center_text(text,fill="-"))
        if not incrementel:
            self.__lcd.cursor_pos=(0,3)
            self.__lcd.write_string("-"*20)
            self.__lcd.cursor_pos=(0,1)
            self.__lcd.write_string("|")
            self.__lcd.cursor_pos=(19,1)
            self.__lcd.write_string("|")
            self.__lcd.cursor_pos=(0,2)
            self.__lcd.write_string("|")
            self.__lcd.cursor_pos=(19,2)
            self.__lcd.write_string("|")
    
    def volume(self, volume:int)->None:
        if not RuntimeVariables.screen==10:
            if RuntimeVariables.screen>10:
                self._draw_frame(incrementel=True)  
            else:
                self._draw_frame(incrementel=False)
            self.__lcd.cursor_pos=(1,1)
            self.__lcd.write_string(self.__center_text("Volume:",lenth=18))
            
        
        if (not self.__last_volume==volume) or RuntimeVariables.screen!=10:
            if  RuntimeVariables.screen!=10:
                self.__lcd.cursor_pos=(1,2)
                self.__lcd.write_string(self.__center_text(f"{volume}%",lenth=18))
            else:
                #overwrite the old three digits only
                self.__lcd.cursor_pos=(8,2)
                self.__lcd.write_string(self.__center_text(f"{volume}%",lenth=4,fill="="))

            self.__last_volume=volume
            RuntimeVariables.screen=10
            if callable(RuntimeVariables.event_callback):
                RuntimeVariables.event_callback()
        
    def usb_plugged_in(self):
        if not RuntimeVariables.screen==11:
            if RuntimeVariables.screen>10:
                self._draw_frame(incrementel=True)  
            else:
                self._draw_frame(incrementel=False)
            self.__lcd.cursor_pos=(1,1)
            self.__lcd.write_string(self.__center_text("USB plugged in",lenth=18))
            RuntimeVariables.screen=11
            if callable(RuntimeVariables.event_callback):
                RuntimeVariables.event_callback()

    def usb_removed(self):
        if not RuntimeVariables.screen==12:
            if RuntimeVariables.screen>10:
                self._draw_frame(incrementel=True)  
            else:
                self._draw_frame(incrementel=False)
            self.__lcd.cursor_pos=(1,1)
            self.__lcd.write_string(self.__center_text("USB removed",lenth=18))
            RuntimeVariables.screen=12
            if callable(RuntimeVariables.event_callback):
                RuntimeVariables.event_callback()
    
    def usb_too_many(self):
        if not RuntimeVariables.screen==30:
            if RuntimeVariables.screen>10:
                self._draw_frame(incrementel=True)  
            else:
                self._draw_frame(incrementel=False)
            self.__lcd.cursor_pos=(1,1)
            self.__lcd.write_string(self.__center_text("Too Many ",lenth=18))
            self.__lcd.cursor_pos=(1,2)
            self.__lcd.write_string(self.__center_text("USB Devices",lenth=18))
            RuntimeVariables.screen=30
            if callable(RuntimeVariables.event_callback):
                RuntimeVariables.event_callback()
    def no_output(self):
        if not RuntimeVariables.screen==31:
            if RuntimeVariables.screen>10:
                self._draw_frame(incrementel=True)  
            else:
                self._draw_frame(incrementel=False)
            self.__lcd.cursor_pos=(1,1)
            self.__lcd.write_string(self.__center_text("No Output",lenth=18))
            RuntimeVariables.screen=31
            if callable(RuntimeVariables.event_callback):
                RuntimeVariables.event_callback()