from time import perf_counter as pf
from time import sleep
import socket
import pandas as pd
import numpy as np
from datetime import datetime
import time
import datetime

class HISSIR:
    def __init__(self,):

        HOST = '192.168.0.1'
        PORT = 8888

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        self.irs=s

    def send_to_ir(self,):
        self.irs.send(b'MS\r\n')     #MS format=MS status vaule of measure, status=00=All OFF,=01=HIGH,02=LOW,03=error,04=GO,08=HH,16=LL
        
    def get_ir_data(self,):
        time_now= datetime.datetime.now().strftime('%Y%m%d %H_%M_%S_%f')
        recdata=self.irs.recv(1024)
        irdata=recdata.decode()    #加上.decode就不會出現\r\n
        print('Receive=',irdata)
        result=irdata.split(',')
        command=result[0].encode('UTF-8').strip()
        status=result[1].strip()
        distance=int(result[2].strip())/1000
        # print('Type=',type(distance))
        print('All data=',command,status,distance)

        if (status=='04'):
            print('get you')
            self.catch_final_data()
        else:
            print('error data')

        return[time_now,command,status,distance] 
    
    def catch_final_data(self,for_counters=500,delay=0.001):
        Data_array=[]

        for i in range(for_counters):
            start = pf()
       
            hiss.send_to_ir()
            Data_array.append(self.get_ir_data())
            #print('here')
            
            elapsed_time = pf()-start
            try:
                sleep(delay-elapsed_time)
                print(delay-elapsed_time)
            except:
                sleep(0.0001)
        
        # Data_array.append(self.get_ir_data())
        # print('Data_aray=',Data_array)


    def nowtime(self,):
        DATE = datetime.datetime.now().strftime('%Y-%m-%d')
        return(DATE)

    def collect_data(self,for_counters=500,delay=0.001):
        Data_array=[]
        print('i am writing data')
        
        for i in range(for_counters):
            start = pf()
       
            hiss.send_to_ir()
            Data_array.append(self.get_ir_data())
            #print('here')
            
            elapsed_time = pf()-start
            try:
                sleep(delay-elapsed_time)
                print(delay-elapsed_time)
            except:
                sleep(0.0001)
            

        Data_array=pd.DataFrame(Data_array)
        Data_array.columns=['Time','Command','Status','Distance']
        
        current_date = datetime.datetime.now()
        filename = str(current_date.year)+str(current_date.month)+str(current_date.day)+str(current_date.second)

        Data_array.to_csv(str(filename+'.csv'),index = False)
    
    


if __name__ == "__main__":
    hiss = HISSIR()
    #hiss.send_to_ir()
    hiss.get_ir_data()
    hiss.catch_final_data(for_counters=500,delay=0.001)
    # Data_array1=[]
    # Data_array1.append(hiss.get_ir_data())
    # print('Data_array1=',Data_array1)




    
    #hiss.collect_data(for_counters= 500, delay =0.001)
    #hiss.collect_data()