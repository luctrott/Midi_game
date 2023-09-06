import os
import time

import threading

from pathlib import Path
from functools import partial
from threading import Event,Thread

import mido
import pathlib
import random
import shutil
from Settings import Settings

class _lcd:
    def __init__(self,game) -> None:
        char0=(0b11111,0b10001,0b10101,0b10101,0b10001,0b10101,0b10001,0b11111)
        char1=(0b11111,0b10001,0b10001,0b10001,0b10001,0b10001,0b10001,0b11111)
        char2=(0b11111,0b11001,0b11001,0b11001,0b11001,0b11001,0b11001,0b11111)
        char3=(0b11111,0b11101,0b11101,0b11101,0b11101,0b11101,0b11101,0b11111)
        char4=(0b11111,0b11111,0b11111,0b11111,0b11111,0b11111,0b11111,0b11111)
        char5=(0b10000,0b11000,0b11100,0b11110,0b11110,0b11100,0b11000,0b10000)
        char6=(0b11011,0b11011,0b11011,0b11011,0b11011,0b11011,0b11011,0b11011)
        
        cols = 20
        rows = 4
        charmap = 'A00'
        i2c_expander = 'PCF8574'
        address = 0x27 
        port = 1
        self.lcd = game.lcd
        self.lcd.create_char(0,char0)
        self.lcd.create_char(1,char1)
        self.lcd.create_char(2,char2)
        self.lcd.create_char(3,char3)
        self.lcd.create_char(4,char4)
        self.lcd.create_char(5,char5)
        self.lcd.create_char(6,char6)

    
    def lcd_init(self):
        self._idle=Event()
        self._idle.set()
        self._queue=[]
        x=Thread(target=self._run_c_l,daemon=True)
        x.start()
    
    def _add_command(self,n):
        self._queue.append(n)
        self._idle.set()
    
    def _run_command(self):
        temp=self._queue.pop(0)
        temp()
    
    def _run_c_l(self):
        while True:
            if len(self._queue)>0:
                self._run_command()
            else:
                self._idle.clear()
                self._idle.wait(5)

    def write_string(self,n:str):
        self._add_command(partial(self.lcd.write_string,n))

    def clear(self):
        self._add_command(self.lcd.clear)
    
    def _cursor_pos(self,x:int,y:int):
        self.lcd.cursor_pos= [y,x]
    
    def cursor_pos(self,x:int,y:int):
        self._add_command(partial(self._cursor_pos,x,y))
    

class lcd_t:
    def __init__(self,game) -> None:
        self.game=game
        self.mode=0
        self.timelenth=None
        self.file=None
        self.timeback=None
        self.pause_set=None
        self.play=False
        self.pause=False
        self._progress=-1
        self.volume=60
        self._pbarnum=['\x01','\x02','\x03','\x04']
        self.lcd_progress()
        
    
    def sec_to_time(self,time:int):
        if time is None:
            return "??:??"
        else:
            minute=str(int(time/60))
            second=str(int(time%60))
            if len(minute)==1:
                minute="0"+minute
            if len(second)==1:
                second="0"+second
            temp=f"{minute}:{second}"
            if len(temp)>5:
                return "??:??"
            else:
                return temp
    def _center_text_in_line(self,text:str):
        if len(text)>20:
            text=text[0:20]
        temp=(20-len(text))
        pre=int(temp/2)
        aft=pre+(temp%2)
        return f"{' '*pre}{text}{' '*aft}"
            


    def lcd_init(self):
        self.lcd=_lcd(self.game)
        self.lcd.lcd_init()

    
    

    def lcd_pp(self):
        
        
        self.lcd.cursor_pos(0, 0)
        if self.play:
            self.lcd.write_string("\x05")
        else:
            self.lcd.write_string(" ")
        if self.pause:
            self.lcd.write_string("\x06")
        else:
            self.lcd.write_string(" ")
        
    
    def lcd_volume(self):
        
        
        self.lcd.clear()
        self.lcd.cursor_pos(0, 0)
        self.lcd.write_string("--------------------")
        self.lcd.cursor_pos(1, 0)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(2, 0)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(1, 19)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(2, 19)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(3, 0)
        self.lcd.write_string("--------------------")
        self.lcd.cursor_pos(1, 7)
        self.lcd.write_string("Volume")
        self.lcd.cursor_pos(2, 11)
        self.lcd.write_string("%")
        
    
    def print_volume_event(self,value:int):
        
        
        value=str(value)
        self.lcd.cursor_pos(2, 8)
        self.lcd.write_string("   ")
        self.lcd.cursor_pos(2, (11)-len(value))
        self.lcd.write_string(value)
        
    def lcd_mode(self):
        
        self.lcd.clear()
        self.lcd.cursor_pos(0, 0)
        self.lcd.write_string("--------------------")
        self.lcd.cursor_pos(1, 0)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(2, 0)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(1, 19)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(2, 19)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(3, 0)
        self.lcd.write_string("--------------------")
        self.lcd.cursor_pos(1, 8)
        self.lcd.write_string("Mode")
        

    
    def print_mode_event(self,value:int):
        
        
        templist=["One","All","Random","All loop","Random loop"]
        temp=templist[value]
        self.mode=value
        self.lcd.cursor_pos(2, 4)
        self.lcd.write_string("           ")
        self.lcd.cursor_pos(2, int(10-(len(temp)/2)))
        self.lcd.write_string(temp)
        
    def print_mode(self):
        
        templist=["O ","A ","R ","Al","Rl"]
        temp=templist[self.mode]
        self.lcd.cursor_pos(0, 18)
        self.lcd.write_string(temp)
        

    def lcd_usb_in(self):
        
        
        self.lcd.clear()
        self.lcd.cursor_pos(0, 0)
        self.lcd.write_string("--------------------")
        self.lcd.cursor_pos(1, 0)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(2, 0)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(1, 19)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(2, 19)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(3, 0)
        self.lcd.write_string("--------------------")
        self.lcd.cursor_pos(1, 8)
        self.lcd.write_string("USB")
        self.lcd.cursor_pos(2, 5)
        self.lcd.write_string("Plugged in")
        
    
    def lcd_usb_out(self):
        
        
        self.lcd.clear()
        self.lcd.cursor_pos(0, 0)
        self.lcd.write_string("--------------------")
        self.lcd.cursor_pos(1, 0)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(2, 0)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(1, 19)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(2, 19)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(3, 0)
        self.lcd.write_string("--------------------")
        self.lcd.cursor_pos(1, 8)
        self.lcd.write_string("USB")
        self.lcd.cursor_pos(2, 6)
        self.lcd.write_string("Removed")
        
    
    def lcd_no_out(self):
        
        
        self.lcd.clear()
        self.lcd.cursor_pos(0, 0)
        self.lcd.write_string("--------------------")
        self.lcd.cursor_pos(1, 0)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(2, 0)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(1, 19)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(2, 19)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(3, 0)
        self.lcd.write_string("--------------------")
        self.lcd.cursor_pos(1, 9)
        self.lcd.write_string("No")
        self.lcd.cursor_pos(2, 7)
        self.lcd.write_string("Output")
        
    
    def lcd_error(self):
        
        
        self.lcd.clear()
        self.lcd.cursor_pos(0, 0)
        self.lcd.write_string("--------------------")
        self.lcd.cursor_pos(1, 0)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(2, 0)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(1, 19)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(2, 19)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(3, 0)
        self.lcd.write_string("--------------------")
        self.lcd.cursor_pos(1, 7)
        self.lcd.write_string("Error!")
        self.lcd.cursor_pos(2, 5)
        self.lcd.write_string("Restarting")
        
    
    def lcd_file(self):
        
        
        self.lcd.clear()
        self.lcd.cursor_pos(0, 0)
        self.lcd.write_string("--------File--------")
        self.lcd.cursor_pos(3, 0)
        self.lcd.write_string("--------------------")
        
    
    def lcd_file_load(self):
        
        
        self.lcd.clear()
        self.lcd.cursor_pos(0, 0)
        self.lcd.write_string("----Loading file----")
        self.lcd_print_filename()
        self.lcd.cursor_pos(3, 0)
        self.lcd.write_string("--------------------")
        

    def lcd_no_out(self):
        
        
        self.lcd.clear()
        self.lcd.cursor_pos(0, 0)
        self.lcd.write_string("--------------------")
        self.lcd.cursor_pos(1, 0)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(2, 0)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(1, 19)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(2, 19)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(3, 0)
        self.lcd.write_string("--------------------")
        self.lcd.cursor_pos(1, 9)
        self.lcd.write_string("No")
        self.lcd.cursor_pos(2, 7)
        self.lcd.write_string("Output")
        

    def lcd_too_many_USB(self):
        
        
        self.lcd.clear()
        self.lcd.cursor_pos(0, 0)
        self.lcd.write_string("--------------------")
        self.lcd.cursor_pos(1, 0)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(2, 0)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(1, 19)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(2, 19)
        self.lcd.write_string("|")
        self.lcd.cursor_pos(3, 0)
        self.lcd.write_string("--------------------")
        self.lcd.cursor_pos(1, 1)
        self.lcd.write_string("Too many storage")
        self.lcd.cursor_pos(2, 1)
        self.lcd.write_string("devices connected")
        
    
    def lcd_print_time_back(self):
        self.lcd.cursor_pos(3, 0)
        self.lcd.write_string("     ")
        self.lcd.cursor_pos(3, 0)
        self.lcd.write_string(self.sec_to_time(self.timeback))
        

    def lcd_print_time_lenth(self):
        self.lcd.cursor_pos(3, 15)
        self.lcd.write_string("     ")
        self.lcd.cursor_pos(3, 15)
        self.lcd.write_string(self.sec_to_time(self.timelenth))
        
    def lcd_print_filename(self):
        
        if not callable(self.file):
            text="No File"
        elif self.file() is None:
            text="No File"
        else:
            text=str(Path(str(self.file())).stem)
    
        self.lcd.cursor_pos(1, 0)
        self.lcd.write_string(self._center_text_in_line(text[0:20]))
        self.lcd.cursor_pos(2, 0)
        self.lcd.write_string(self._center_text_in_line(text[20:40]))
        
    
    def lcd_progress(self):
        if (self.timelenth is None)or(self.timeback is None):
            self._progress=None
        
        else:
            self._progress=round((30/self.timelenth)*self.timeback)

        if self._progress is None:
            self._bar="\x00"*10
        elif self._progress==0:
            self._bar="\x01"*10
        else:
            self._bar=""
            self._bar+="\x04"*int(self._progress/3)
            temp=int(self._progress%3)
            if temp>0:
                self._bar+=self._pbarnum[temp]
            
            self._bar+= "\x01"*int(10-len(self._bar))
    def lcd_progress_print(self): 
        self.lcd.cursor_pos(3,5)
        self.lcd.write_string(" "*10)
        self.lcd.cursor_pos(3,5)
        
        self.lcd.write_string(self._bar)
            
    
    def lcd_print_volume(self):

        self.lcd.cursor_pos(0,10)
        self.lcd.write_string("   ")
        self.lcd.cursor_pos(0,10)
        temp= str(self.volume)
        if len(temp)<3:
            temp= f"{' '*(3-len(temp))}{temp}"
        
        self.lcd.write_string(temp)
        

    def lcd_standert(self):
        
        self.lcd.clear()
        self.lcd_pp()
        self.lcd.cursor_pos(0, 6)
        self.lcd.write_string("Vol:")
        self.lcd.cursor_pos(0, 13)
        self.lcd.write_string("%")
        self.lcd_print_volume()
        self.print_mode()
        self.lcd_progress_print()
        self.lcd_print_time_back()
        self.lcd_print_time_lenth()
        self.lcd_print_filename()

class usb:
    def __init__(self) -> None:
        self.ret_code=0
        self.devices=[]
        self.folder=[]
        self.unmount=[]
        self.mount=[]
        self.stop=False
        self.update=None

        self.mounted=None
        self.unmounted=None

 

    def get_devices_and_folders(self):

        self.devices= list(os.listdir("./dev/"))
        self.folder= list(os.listdir("./usb/"))
    
    def unmount_all(self):
        self.get_devices_and_folders()
        if len(self.folder)>0:
            for dev in self.folder:
                        self.unmount_device(dev)
                        print(f"unmounted {dev}")
            
    def getfoldercount(self):
        self.get_update()
        return len(self.folder)

    def get_update(self):
        self.get_devices_and_folders()
        if not self.devices==self.folder:
            self.mount=(list(set(self.devices)-set(self.folder)))
            self.unmount=(list(set(self.folder)-set(self.devices)))
            if len(self.unmount)>0:
                for dev in self.unmount:
                    self.unmount_device(dev)
                    print(f"unmounted {dev}")
                if callable(self.unmounted):
                    self.unmounted()
            if len(self.mount)>0:
                for dev in self.mount:
                    self.mount_device(dev)
                    print(f"mounted {dev}")
                if callable(self.mounted):
                    self.mounted()
            if callable(self.update):
                self.update()
    def unmount_device(self,dev:str):
        #remove folder with files
        shutil.rmtree(f"./usb/{dev}")

        
    
    def mount_device(self,dev:str):
        tmp=[0]
        while not tmp==os.listdir(f"./dev/{dev}"):
            tmp=os.listdir(f"./dev/{dev}")
            time.sleep(0.5)
        shutil.copytree(f"./dev/{dev}",f"./usb/{dev}")

    def run(self):
        while not self.stop:
            self.get_update()
            time.sleep(2)

class player:
    def __init__(self,port:str) -> None:
        self._pause=threading.Event()
        self._wait_for_stop=threading.Event()
        self.loading=None
        self.loading_done=None
        self.finnished=None
        self._pause.set()
        self.playbuisy=False
        self._portname=port
        self.factor=0.6
        self.time_is=None
        self._port=None
        self._port_is_open=False
        self.device_not_found=None
        self.update_time=None
        self.lenth_change=None
        self.playback_lenth=None
        self._midi=None
        self._stop_lenth=False
        self._stop=False
        self._file=None
        self._getlenth_is_running=False
        self._time_last=0
    
    def volume(self,n:int):
        self.factor=n/100
        
    def time_updater(self):
        while self.playbuisy:
            self._time_last=time.time()
            if callable(self.update_time):
                self.update_time()
            self._check_port()
            temp=(1-(time.time()-self._time_last))
            if temp>0:
                time.sleep(temp)
            self._pause.wait()
            
    
    def check_port(self):
        temp=self._portname in list(mido.get_output_names())
        return temp
    def _check_port(self):
        print("check port")
        temp=self._portname in list(mido.get_output_names())
        print(temp)

        if not temp:
            self._port_is_open=False
            
            self.device_not_found()
        return temp

    def open_port(self):
        print("open port")
        if self._check_port():
            print("port is open")
            if not self._port_is_open:
                print("port is not open")
                self._port= mido.open_output(self._portname)

            self._port_is_open=True

    def _getlenth(self):
        self._getlenth_is_running=True
        temp=0
        for msg in self._midi:
            if self._stop_lenth:
                break
            temp+=msg.time
        if not self._stop_lenth:
            self.playback_lenth= temp
            if callable(self.lenth_change):
                self.lenth_change()
        else:
            self._stop_lenth=False
        self._getlenth_is_running=False


    def _play_file(self):
        if self._check_port():
            self.playbuisy=True
            self.playback_lenth=None
            if callable(self.lenth_change):
                self.lenth_change()
            if callable(self.loading):
                self.loading()
            self._midi=list(mido.MidiFile(self._file,clip=True))
            x=threading.Thread(target=self._getlenth,daemon=True)
            x.start()
            y=threading.Thread(target=self.time_updater,daemon=True)
            y.start()
            self._port.reset()
            self.time_is=0
            if callable(self.loading_done):
                self.loading_done()
            rtime=time.time()
            time_since=0
            
            for msg in self._midi:
                if self._stop:
                    break
                ti=msg.time
                self.time_is+=ti
                time_since+=ti
                
                temp=msg.type
                if temp=='note_on' or temp=='note_off':
                    temp2= int(msg.velocity*self.factor)
                    if temp2<=127:
                        msg.velocity=temp2
                    else:
                        msg.velocity=127
                wait=(rtime+time_since-time.time())
                if wait>0:
                    time.sleep(wait)
                if not msg.is_meta:
                    self._port.send(msg)
                
                if not self._pause.is_set():
                    self._port.panic()
                    self._pause.wait()
                    rtime=time.time()
                    time_since=0


            if self._stop:
                self._stop=False
                self._wait_for_stop.set()
            
            self._port.reset()
            self.playbuisy=False
            self.time_is=None
            self.playback_lenth=None
            if callable(self.update_time):
                self.update_time()
            if callable(self.lenth_change):
                self.lenth_change()
            if not self._stop:
                if callable(self.finnished):
                    self.finnished()
        
    def pause(self):
        if self._pause.is_set():
            self._pause.clear()
    
    def resume(self):
        if not self._pause.is_set():
            self._pause.set()
    
    def stop(self):
        if self._getlenth_is_running:
            self._stop_lenth=True
        if self.playbuisy:
            self._wait_for_stop.clear()
            self._pause.set()
            self._stop=True
            self._wait_for_stop.wait()
    def play(self,file):
        self._file=file
        if self.playbuisy:
            self._wait_for_stop.clear()
            self._stop=True
            self._wait_for_stop.wait()
        x=threading.Thread(target=self._play_file,daemon=True)
        x.start()

class Files:
    def __init__(self) -> None:
        self.mode=0
        self._tracknum=0
        self.loopfull=None

    def _getAllMid(self,path):
        filelist2 = list(pathlib.Path(path).glob("**/*.mid",))
        filelist=[]
        for file in filelist2:
            filelist.append(file.absolute())
        return filelist

    
    def _randomnumberlist(self,numb:int):
        return list(random.sample(range(0,numb),numb))

    def _getAllMidi(self):
        temp= self._getAllMid('./usb/')
        if len(temp)>0:
            return temp
        else:
            temp= self._getAllMid('./onboard/')
            
            if len(temp)>0:
                return temp
            else:
                raise FileNotFoundError
    def getNum_index_in_radom(self,num:int):
        return self.rannum.index(num)
    
    def update(self):
        self.filelist=self._getAllMidi()
        self.rannum=self._randomnumberlist(len(self.filelist))
        if not self.mode in [2,4]:
            self._tracknum=0
        else:
            self._tracknum=self.rannum[0]
        return str((self.filelist[self._tracknum]))

    def forward(self):
        if not ((self.mode==2)or(self.mode==4)):
            if not (self._tracknum+1)>len(self.filelist)-1:
                self._tracknum+=1
            
            else:
                self._tracknum=0
                if callable(self.loopfull):
                    self.loopfull()
        else:
            temp=self.getNum_index_in_radom(self._tracknum)
            if not temp+1>len(self.rannum)-1:
                self._tracknum=self.rannum[temp+1]
            
            else:
                self.rannum=self.rannum=self._randomnumberlist(len(self.filelist))
                self._tracknum=self.rannum[0]
                if callable(self.loopfull):
                    self.loopfull()

        
        return str((self.filelist[self._tracknum]))
    
    def back(self):
        if not ((self.mode==2)or(self.mode==4)):
            if not (self._tracknum-1)<0:
                self._tracknum-=1
            
            else:
                self._tracknum=len(self.filelist)-1
        else:
            temp=self.getNum_index_in_radom(self._tracknum)
            if not temp-1<0:
                self._tracknum=self.rannum[temp-1]
            
            else:
                self.rannum=self.rannum=self._randomnumberlist(len(self.filelist))
                self._tracknum=self.rannum[0]
        
        return str((self.filelist[self._tracknum]))
    
    def current(self):
        return str((self.filelist[self._tracknum]))
    
    def randomstart(self):
        return str(random.choice(self.filelist))
    def reset(self):
        self._tracknum=0
        return str((self.filelist[self._tracknum]))



class connect:
    def __init__(self) -> None:
        self.freeze=False
        self.t0pv=None
        self.t1pv=None
        self.t2pv=None
        self.t3pv=None
        self.t4pv=None
        self.t5pv=None
        self.t6pv=None
        self.t0hv=None
        self.t1hv=None
        self.t2hv=None
        self.t3hv=None
        self.t4hv=None
        self.t5hv=None
        self.t6hv=None

    
    def t0p(self,action=0):
        if not action==0:
            if not action==self.t0pv:
                self.t0pv=action
        elif callable(self.t0pv):
            if not self.freeze:
                self.t0pv()

    
    def t1p(self,action=0):
        print("t1p")
        if not action==0:
            if not action==self.t1pv:
                self.t1pv=action
        elif callable(self.t1pv):
            if not self.freeze:
                self.t1pv()

    
    def t2p(self,action=0):
        print("t2p")
        if not action==0:
            if not action==self.t2pv:
                self.t2pv=action
        elif callable(self.t2pv):
            if not self.freeze:
                self.t2pv()

    
    def t3p(self,action=0):
        if not action==0:
            if not action==self.t3pv:
                self.t3pv=action
        elif callable(self.t3pv):
            if not self.freeze:
                self.t3pv()

    
    def t4p(self,action=0):
        if not action==0:
            if not action==self.t4pv:
                self.t4pv=action
        elif callable(self.t4pv):
            if not self.freeze:
                self.t4pv()

    
    def t5p(self,action=0):
        if not action==0:
            if not action==self.t5pv:
                self.t5pv=action
        elif callable(self.t5pv):
            if not self.freeze:
                self.t5pv()

    
    def t6p(self,action=0):
        if not action==0:
            if not action==self.t6pv:
                self.t6pv=action
        elif callable(self.t6pv):
            if not self.freeze:
                self.t6pv()
    
    def t0h(self,action=0):
        if not action==0:
            if not action==self.t0hv:
                self.t0hv=action
        elif callable(self.t0hv):
            if not self.freeze:
                self.t0hv()

    
    def t1h(self,action=0):
        if not action==0:
            if not action==self.t1hv:
                self.t1hv=action
        elif callable(self.t1hv):
            if not self.freeze:
                self.t1hv()

    
    def t2h(self,action=0):
        if not action==0:
            if not action==self.t2hv:
                self.t2hv=action
        elif callable(self.t2hv):
            if not self.freeze:
                self.t2hv()

    
    def t3h(self,action=0):
        if not action==0:
            if not action==self.t3hv:
                self.t3hv=action
        elif callable(self.t3hv):
            if not self.freeze:
                self.t3hv()

    
    def t4h(self,action=0):
        if not action==0:
            if not action==self.t4hv:
                self.t4hv=action
        elif callable(self.t4hv):
            if not self.freeze:
                self.t4hv()

    
    def t5h(self,action=0):
        if not action==0:
            if not action==self.t5hv:
                self.t5hv=action
        elif callable(self.t5hv):
            if not self.freeze:
                self.t5hv()

    
    def t6h(self,action=0):
        if not action==0:
            if not action==self.t6hv:
                self.t6hv=action
        elif callable(self.t6hv):
            if not self.freeze:
                self.t6hv()

    def block(self):
        self.freeze=True
    
    def connect(self):
        self.freeze=False

class main:
    def __init__(self,game) -> None:
        self.game=game
        self.mode=0
        self.event=0
        self.volume=60
        self.file=Files()
        self.lcd=lcd_t(self.game)
        self.lcd.lcd_init()
        #self.file.update()
        
        self.lcd.volume=self.volume
        self.lcd.lcd_standert()
        self.lcd.file=self.file.current
        self.file.loopfull=self.loop
        self.after_event=None
        self.ev=threading.Event()
        self.waiting=threading.Thread(target=self._wait,daemon=True)
        self._progressold=None
        self.play=False
        self.pause=False
    def restart(self):
        if True:
            self.freez()
            self.lcd.lcd_error()
            time.sleep(2)
            os._exit(1)
        

    def loop(self):
        if self.mode==1 or self.mode==2:
            self.play=False
            self.pause=False
            self.lcd.pause=False
            self.lcd.play=False
            if self.event==0:
                self.lcd.lcd_pp()

    
    def finished(self):
        if self.mode==0:
            self.play=False
            self.pause=False
            self.lcd.pause=False
            self.lcd.play=False
            if self.event==0:
                self.lcd.lcd_pp()
        else:
            self.file.forward()
            if self.event==0:
                self.lcd.lcd_print_filename()
            
            if self.play:
                x=threading.Thread(target=self._test,daemon=True)
                x.start()
    def _test(self):
        time.sleep(1)
        self.player.play(self.file.current())
        

    def lenth_update(self):
        self.lcd.timelenth=self.player.playback_lenth
        if self.event==0:
            self.lcd.lcd_print_time_lenth()
    
    def time_update(self,force=False):
        self.lcd.timeback=self.player.time_is
        self.lcd.lcd_progress()
        if not self._progressold==self.lcd._progress:
            self._progressold=self.lcd._progress
            if self.event==0 or force:
                self.lcd.lcd_progress_print()
        
        if self.event==0 or force:
            self.lcd.lcd_print_time_back()

        
       

    
    def loading_file(self):
        self.freez()
        self.events(10)
        
    
    def loading_file_done(self):
        self.ev_timeout=0
        self.event=0
        self.gpio_conn()
        
    
    def usb_in(self):
        self.events(3)
        self.player.stop()
        self.play=False
        self.pause=False
        self.lcd.play=False
        self.lcd.pause=False
        self.file.update()
    
    def usb_out(self):
        self.events(4)
        self.player.stop()
        self.play=False
        self.pause=False
        self.lcd.play=False
        self.lcd.pause=False
        self.file.update()

    def plus_pressed(self):
        if self.event==1:
            if (self.volume+1)<=999:
                self.volume+=1
            else:
                self.volume=999
            self.lcd.volume=self.volume
            self.player.volume(self.volume)
        self.events(1)
        self.lcd.print_volume_event(self.volume)

    def plus_held(self):
        while self.t0.is_pressed:
            if (self.volume+5)<=999:
                self.volume+=5
            else:
                self.volume=999
            self.lcd.volume=self.volume
            self.player.volume(self.volume)
            self.events(1)
            self.lcd.print_volume_event(self.volume)
            time.sleep(0.25)
    
    def minus_pressed(self):
        if self.event==1:
            if (self.volume-1)>=0:
                self.volume-=1
            else:
                self.volume=0
            self.lcd.volume=self.volume
            self.player.volume(self.volume)
        self.events(1)
        self.lcd.print_volume_event(self.volume)

    def minus_held(self):
        while self.t1.is_pressed:
            if (self.volume-5)>=0:
                self.volume-=5
            else:
                self.volume=0
            self.lcd.volume=self.volume
            self.player.volume(self.volume)
            self.events(1)
            self.lcd.print_volume_event(self.volume)
            time.sleep(0.25)



    def forward_pressed(self):
        if self.play:
            self.stop()
        if self.event==7:
            self.file.forward()
        self.events(7)
        self.lcd.lcd_print_filename()

    def forward_held(self):
        if self.play:
            self.stop()
        while self.t2.is_pressed:
            self.file.forward()
            self.events(7)
            self.lcd.lcd_print_filename()
            time.sleep(0.25)
    
    def back_pressed(self):
        if self.play:
            self.stop()
        if self.event==7:
            self.file.back()
        self.events(7)
        self.lcd.lcd_print_filename()

    def back_held(self):
        if self.play:
            self.stop()
        while self.t3.is_pressed:
            self.file.back()
            self.events(7)
            self.lcd.lcd_print_filename()
            time.sleep(0.25)

    def playpause(self):
        if not self.play:
            self.ev_timeout=0
            self.play=True
            self.lcd.play=self.play
            self.player.play(self.file.current())
        else:
            self.pause= not self.pause
            self.lcd.pause=self.pause
            if self.event==0:
                self.lcd.lcd_pp()
            if self.pause:
                self.player.pause()
            else:
                self.player.resume()
        

    
    def stop(self):
        self.pause=False
        self.lcd.pause=self.pause
        if self.play:
            self.play=False
            self.lcd.play=self.play
            self.player.stop()
        else:
            self.file._tracknum=0
            if self.event==0:
                self.lcd.lcd_print_filename()
        if self.event==0:
            self.lcd.lcd_pp()
        




    
    
    def mode_pressed(self):
        if self.event==2:
            if self.mode<4:
                self.mode+=1
            else:
                self.mode=0
        self.events(2)
        self.lcd.print_mode_event(self.mode)
        self.file.mode=self.mode
    def events(self,numb:int):
        
        if not self.event==numb:
        
            if not self.event==0:
                self.ev.set()
                while not self.event==-10:
                    time.sleep(0.1)
                self.ev.clear()
            
            if numb==1:
                self.event=numb
                
                self.lcd.lcd_volume()
                self.waiting=threading.Thread(target=self._wait,daemon=True)
                self.waiting.start()
            
            if numb==2:
                self.event=numb
                self.lcd.lcd_mode()
                self.waiting=threading.Thread(target=self._wait,daemon=True)
                self.waiting.start()
            
            if numb==3:
                self.event=numb
                self.lcd.lcd_usb_in()
                self.waiting=threading.Thread(target=self._wait,daemon=True)
                self.waiting.start()
            if numb==4:
                self.event=numb
                self.lcd.lcd_usb_out()
                self.waiting=threading.Thread(target=self._wait,daemon=True)
                self.waiting.start()
            if numb==5:
                self.event=numb
                self.lcd.lcd_no_out()
                self.waiting=threading.Thread(target=self._wait,daemon=True)
                self.waiting.start()
            if numb==6:
                self.event=numb
                self.lcd.lcd_too_many_USB()
                self.waiting=threading.Thread(target=self._wait,daemon=True)
                self.waiting.start()
            if numb==7:
                self.event=numb
                self.lcd.lcd_file()
                self.waiting=threading.Thread(target=self._wait,daemon=True)
                self.waiting.start()
            
            if numb==10:
                self.event=numb
                self.lcd.lcd_file_load()
                self.waiting=threading.Thread(target=self._wait,daemon=True)
                self.waiting.start()
                time.sleep(1)
                self.ev_timeout=120

        else:
            self.ev_timeout=4
                
                
    
    def _wait(self):
        self.ev_timeout=4
        self.ev.clear()
        while (not self.ev_timeout<=0) and (not self.ev.is_set()):
            
            self.ev.wait(1)
            self.ev_timeout-=1

        if (not self.ev.is_set()):
            self.lcd.lcd_standert()
            
            self.event=0
        else:
            self.event=-10
        self.after_event
    
    def gpio_conn(self):
        self.conn.connect()

    def gpio(self):
        self.conn=connect()
        hold=1
        for b in self.game.buttons:
            b.hold_time=hold
        print("HI")
        self.t0=self.game.buttons[5] #+
        self.t1=self.game.buttons[4] #-
        self.t2=self.game.buttons[2] #ff
        self.t3=self.game.buttons[3] #back
        self.t4=self.game.buttons[0] #startstop
        self.t5=self.game.buttons[1] #stop
        self.t6=self.game.buttons[6]#mode
        self.t0.when_pressed=self.conn.t0p#self.plus_pressed
        self.t0.when_held=self.conn.t0h #self.plus_held
        self.t1.when_pressed=self.conn.t1p #self.minus_pressed
        self.t1.when_held=self.conn.t1h#self.minus_held
        self.t2.when_pressed=self.conn.t2p
        self.t2.when_held=self.conn.t2h
        self.t3.when_pressed=self.conn.t3p
        self.t3.when_held=self.conn.t3h
        self.t4.when_pressed=self.conn.t4p
        self.t4.when_held=self.conn.t4h
        self.t5.when_pressed=self.conn.t5p
        self.t5.when_held=self.conn.t5h
        self.t6.when_pressed=self.conn.t6p#self.mode_pressed
        self.t6.when_held=self.conn.t6h
        
        self.conn.t0p(self.plus_pressed)
        self.conn.t0h(self.plus_held)
        self.conn.t1p(self.minus_pressed)
        self.conn.t1h(self.minus_held)

        self.conn.t2p(self.forward_pressed)
        self.conn.t2h(self.forward_held)
        self.conn.t3p(self.back_pressed)
        self.conn.t3h(self.back_held)
        self.conn.t4p(self.playpause)
        self.conn.t5p(self.stop)
        self.conn.t5h(self.restart)

        self.conn.t6p(self.mode_pressed)

        
        

        
        self.gpio_conn()
        print(self.t1.when_pressed)
        
    def freez(self):
        self.conn.block()

    def no_dev(self):
        self.freez()
        if self.play and not self.pause:
            self.player.pause()
            self.pause=True
            self.lcd.pause=True
        while not self.player.check_port():
            self.events(5)
            time.sleep(1)
        self.ev_timeout=0
        self.gpio_conn()
        self.player.open_port()
    
    def usb_update(self):
        self.player.stop()
        if self.usbc.getfoldercount()>1:
            self.freez()
            while self.usbc.getfoldercount()>1:
                self.events(6)
                time.sleep(1)
            self.ev_timeout=0
            self.gpio_conn()

    def init(self):
        self.gpio()
        print("gpio init done")
        self.usbc=usb()

        self.usbc.mounted=self.usb_in
        self.usbc.unmounted=self.usb_out
        self.usbc.update=self.usb_update
        print("usb init done")
        self.usbt= threading.Thread(target=self.usbc.run,daemon=True)
        print("usb thread init done")
        self.usbc.unmount_all()
        print("unmount all done")
        self.file.update()
        print("file update done")
        if self.event==0:
            self.lcd.lcd_print_filename()
        self.usbt.start()
        print("usb thread start done")
    
        self.player=player(Settings.midi_port) 
        self.player.device_not_found=self.no_dev
        self.player.loading=self.loading_file
        self.player.loading_done=self.loading_file_done
        self.player.update_time=self.time_update
        self.player.finnished=self.finished
        self.player.lenth_change=self.lenth_update
        print("player init done")
        self.player.open_port()
        print("player open port done")
    
if __name__=='__main__':
  
    x=main()
    x.init()
    while True:
       time.sleep(1)
        

    x.lcd.lcd_error()
    time.sleep(2)