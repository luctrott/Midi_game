from LCDHandler import LCDHandler
from RuntimeVariables import RuntimeVariables

class ProgressBar:
    def __init__(self,lcd:LCDHandler) -> None:
        self.__lcd=lcd
        self.__progress_bar_chars=['\x00','\x01','\x02','\x03','\x04']
        self.__progress=0
        self.__progress_bar_curent_chars=[]
        self.__current_time_passed="     "
        self.__current_time_whole="     "
        self.__whole_time=-1
        self.__passed_time=-1
        
        for _ in range(10):
            self.__progress_bar_curent_chars.append(self.__progress_bar_chars[0])
        self.__display_time(self.__passed_time,self.__whole_time,False)

    @property
    def whole_time(self)->int:
        return self.__whole_time
    
    @whole_time.setter
    def whole_time(self,value:int)->None:
        self.__whole_time=value
    
    @property
    def passed_time(self)->int:
        return self.__passed_time
    
    @passed_time.setter
    def passed_time(self,value:int)->None:
        self.__passed_time=value
        self.__display_time(self.__whole_time,self.__passed_time)
    
    def __convert_to_dotted(self,seconds:int)->str:
        if seconds<0:
            return "??:??"
        elif seconds>5999:
            return "XX:XX"
        else:
            minutes=seconds//60
            seconds=seconds-(minutes*60)
            return f'{minutes:02d}:{seconds:02d}'
    
    
    def __display_time(self,whole:int,passed:int,incrmental:bool=True)->None:
        if RuntimeVariables.screen==1:
        
            th=self.__convert_to_dotted(whole)
            tp=self.__convert_to_dotted(passed)
            if any([whole<0,passed<0]):
                progess=-1
            elif any([whole==0,passed==0]):
                progess=0
            else:
                progess=int((passed/whole)*100)

            if not incrmental:
                self.__current_time_whole=th
                self.__current_time_passed=tp
                self.__lcd.cursor_pos=(0,3)
                self.__lcd.write_string(tp)
                self.__lcd.cursor_pos=(15,3)
                self.__lcd.write_string(th)
            else:
                if self.__current_time_whole!=th:
                    for num,char in enumerate(th):
                        if char!=self.__current_time_whole[num]:
                            self.__lcd.cursor_pos=(15+num,3)
                            self.__lcd.write_string(char)
                    self.__current_time_whole=th

                if self.__current_time_passed!=tp:
                    for num,char in enumerate(tp):
                        if char!=self.__current_time_passed[num]:
                            self.__lcd.cursor_pos=(num,3)
                            self.__lcd.write_string(char)
                    self.__current_time_passed=tp
            self.__draw_progress_bar(progess,incrmental)

        


    def __draw_progress_bar(self,progress:int,incremental:bool=True)->None:
        #progress: -1=-1, 0=0, 100=30
        if progress!= -1 and progress>0:
            progress=int(progress/3)

        if (progress != self.__progress or not incremental) and progress<=30:
            self.__progress=progress
            tmp=self.__progress_bar_curent_chars.copy()
            if progress == -1:

                for i in range(10):
                    tmp[i]=self.__progress_bar_chars[0]
            elif  progress == 0:
                for i in range(10):
                    tmp[i]=self.__progress_bar_chars[1]
            elif progress == 30:
                for i in range(10):
                    tmp[i]=self.__progress_bar_chars[4]
            else:
                a=int(progress/3)
                b=progress-(a*3)

                if not incremental:
                    for i in range(a):
                        tmp[i]=self.__progress_bar_chars[1]
                elif a>0:
                    tmp[a-1]=self.__progress_bar_chars[4]
                tmp[a]=self.__progress_bar_chars[b+1]
            if incremental:
                for i in range(10):
                    if tmp[i]!=self.__progress_bar_curent_chars[i]:
                        self.__progress_bar_curent_chars[i]=tmp[i]
                        self.__lcd.cursor_pos=(i+5,3)
                        self.__lcd.write_string(tmp[i])
            else:
                self.__progress_bar_curent_chars=tmp.copy()
                self.__lcd.cursor_pos=(5,3)
                self.__lcd.write_string(''.join(tmp))
    
    def force_reload(self)->None:
        self.__display_time(self.__whole_time,self.__passed_time,False)
