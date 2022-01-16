import json 

class DataHandling:
    def __init__(self,soc_obj=None):
        self.soc=soc_obj
        
    def data_send(self,msg):
        json_data=json.dumps(msg)
        self.soc.send(json_data.encode())

    def data_recv(self):
        real_data = ''
        while True:
            try:
                real_data = real_data+self.soc.recv(1024).decode().rstrip()
                return json.loads(real_data)
            except ValueError:
                continue