from numpy.core.defchararray import array
import serial
import pandas as pd
import time
import struct
import numpy as np
import matplotlib.pyplot as plt
import keyboard
import csv
from datetime import datetime
from threading import Thread
from PyQt5.QtCore import QObject, pyqtSignal


class SerialPort(object):
    # Contains functions that enable communication between the docking station and the IMU watches
    data = pyqtSignal(list)

    def __init__(self, serialport, serialrate=115200):
        # Initialise serial payload
        self.count = 0
        self.plSz = 0
        self.payload = bytearray()
        self.sw=0
        self.sw1=True
        self.dummy=0
        self.Ax=[]
        self.Ay=[]
        self.Az=[]
        self.Gx=[]
        self.Gy=[]
        self.Gz=[]
        self.Ax1=[]
        self.Ay1=[]
        self.Az1=[]
        self.Gx1=[]
        self.Gy1=[]
        self.Gz1=[]

        # Initialise serial port
        running = False
        self.serialport = serialport
        self.ser = serial.Serial(serialport, serialrate)

        self.mydata = pd.DataFrame(columns=["ax", "ay", "az", "cx", "cy", "cz","ax1", "ay1", "az1", "cx1", "cy1", "cz1"])
        
    def serial_write(self, payload):
        # Format:
        # | 255 | 255 | no. of bytes | payload | checksum |

        header = [255, 255]
        chksum = 254

        payload_size = len(payload) + 1

        chksum += payload_size 

        self.ser.write(bytes([header[0]]))
        self.ser.write(bytes([header[1]]))
        self.ser.write(bytes([payload_size]))

        self.ser.write(bytes([payload]))

        
        self.ser.write(bytes([chksum % 256]))

    def serial_read(self):
        if (self.ser.read() == b'\xff') and (self.ser.read() == b'\xff'):
            # print("Yes")
            self.count += 1
            chksum = 255 + 255

            self.plSz = self.ser.read()[0]
            chksum += self.plSz

            self.payload = self.ser.read(self.plSz - 1)
           
            chksum += sum(self.payload)
            chksum = bytes([chksum % 256])
            _chksum = self.ser.read()

            return _chksum == chksum
        return False
    
    def show_data(self, progress_callback):
        
        self.Ax=[]
        self.Ay=[]
        self.Az=[]
        self.Gx=[]
        self.Gy=[]
        self.Gz=[]
        self.Ax1=[]
        self.Ay1=[]
        self.Az1=[]
        self.Gx1=[]
        self.Gy1=[]
        self.Gz1=[]
        
        y1=[]
        while True: 
            if self.serial_read():
                
                y=list(struct.unpack('12f',self.payload))
                if self.sw:
                    self.dummy=1
                    
                    y1.append(y)
                if not self.sw and self.dummy % 2==1:
                    self.dummy=0
                    
                    y1=np.array(y1)
                    y1=np.transpose(y1)
                    headerList=['gyrox1','gyroy1','gyroz1','accelx1','accely1','accelz1','gyrox2','gyroy2','gyroz2','accelx2','accely2','accelz2']
                    df = pd.DataFrame(y1).T
                    df.to_csv(r"C:\Users\Dell\Desktop\MS Bioengineering\imu_data6.csv",header=headerList)
                    y1=[]
               
                if not self.sw1:
                    break
                self.Ax.append(np.array(y[0]))
                self.Ay.append(np.array(y[1]))
                self.Az.append(np.array(y[2]))
                self.Gx.append(np.array(y[3]))
                self.Gy.append(np.array(y[4]))
                self.Gz.append(np.array(y[5]))
                self.Ax1.append(np.array(y[6]))
                self.Ay1.append(np.array(y[7]))
                self.Az1.append(np.array(y[8]))
                self.Gx1.append(np.array(y[9]))
                self.Gy1.append(np.array(y[10]))
                self.Gz1.append(np.array(y[11]))
                if len(self.Ax)>1000:
                    self.Ax = self.Ax[-1000:]
                    self.Ay = self.Ay[-1000:]
                    self.Az = self.Az[-1000:]
                    self.Gx = self.Gx[-1000:]
                    self.Gy = self.Gy[-1000:]
                    self.Gz = self.Gz[-1000:]
                    self.Ax1 = self.Ax1[-1000:]
                    self.Ay1 = self.Ay1[-1000:]
                    self.Az1 = self.Az1[-1000:]
                    self.Gx1 = self.Gx1[-1000:]
                    self.Gy1 = self.Gy1[-1000:]
                    self.Gz1 = self.Gz1[-1000:]
                progress_callback.emit([self.Ax, self.Ay,self.Az,self.Gx,self.Gy,self.Gz, self.Ax1, self.Ay1, self.Az1, self.Gx1, self.Gy1, self.Gz1])
                
    
            

    def kill_switch1(self, sw1):
        if sw1:
            self.sw1 = True
        if not sw1:
            self.sw1 = False              

    
    def kill_switch(self, sw):
        if sw:
            self.sw = 1
        if not sw:
            self.sw = 0
            
    # def connect1(self):
    #     if self.ser.isOpen():
    #         self.show=Thread(target=self.show_data,args=())
    #         self.show.start()  
    # def ConnectToArduino(self,header,filename=' '):
    #     if self.ser.isOpen():
        
    #         #Start reader and writer threads.

    #         reader = Thread(target=self.recordData, args=(header,filename))
    #         print('hi')
    #         reader.start()


