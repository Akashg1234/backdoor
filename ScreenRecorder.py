import threading,os
import numpy as np,cv2,tkinter as tk,pyautogui as gui,time as t
from datetime import datetime
from FileHandling import FileHandler as fh

class ScreenRecorder:
    def __init__(self,duration=None,path=None,soc_obj=None):
        self.root = tk.Tk()
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.flag=False
        self.path=path
        self.file_handler=fh(soc_obj)
        if duration==' ':
            self.duration=86400
        else:
            self.duration=duration
        
    def countdown(self):
        sec=0
        while True:
            if sec==self.duration:
                self.flag=True
                break
            elif self.flag:
                break
            t.sleep(1)
            sec+=1
            
    def screen_capturing(self):
        resulution = (self.width,self.height)
        fps = 240
        codec = cv2.VideoWriter_fourcc(*"XVID")
        file = self.path+"\\Es00d{}.avi".format(datetime.now())
        out = cv2.VideoWriter(file,codec,fps,resulution)
        thread = threading.Thread(target=self.countdown)
        thread.start()
        while True:
            img = gui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            out.write(frame)
            if self.flag:
                break
        self.count+=1
        thread.join()
        out.release()
        self.file_handler.file_send(file=file)
        os.remove(file)

    def stop_screen_recording(self):
        self.flag=True