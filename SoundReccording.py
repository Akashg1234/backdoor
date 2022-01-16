import sounddevice as sd
from scipy.io.wavfile import write
from datetime import datetime
from FileHandling import FileHandler as fh
import os

class Recording:
    def __init__(self,time=None,path=None,soc_obj=None) :
        self.recording_flag=False
        if time== ' ':
            self.duration=86400
        else:
            self.duration=time
        self.path=path
        self.file_handler=fh(soc_obj)

    def recording(self):
        frame_rate=44100
        myrecording=sd.rec(frames=int(self.recording_time*frame_rate),samplerate=frame_rate,channels=2)
        if self.recording_flag:
            sd.stop()
        else:
            sd.wait()
        time_stamp=datetime.now()
        file=self.path+'/Snd000p{}.wav'.format(time_stamp)
        write(file,frame_rate,myrecording)
        self.file_handler.file_send(file)
        os.remove(self.path)

    def stop_recording(self):
        self.recording_flag=True
        sd.stop()
        os.remove(self.path)
