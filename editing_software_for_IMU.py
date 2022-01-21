from PyQt5 import QtWidgets

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import *

import numpy as np
import time
from PyQt5.QtCore import QSize, Qt,QTimer
from reading_imu_data  import SerialPort
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar)
from PyQt5.QtWidgets import QWidget,QGridLayout,QToolBar,QStatusBar,QMessageBox,QVBoxLayout,QAction
from matplotlib.figure import Figure
from threading import Thread
from newIMUsoftwarev1 import Ui_MainWindow
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import sys
from support_py import initialize_graphs

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal()
    progress = pyqtSignal()
    changePixmap = pyqtSignal()


class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            pass
        else:
            pass
        finally:
            self.signals.finished.emit()  # Done



class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.a = SerialPort('COM6',115200)
        self.c=0
        self.c1=0
        self.counter=0
        self.counter1=0
        self.counter2=0
        self.n=0
        initialize_graphs(self)
        
        self.a.connect1()

        self.ui.sec.setText("0")
        self.ui.min.setText("0")
        self.ui.hour.setText("0")
        self.ui.start.clicked.connect(self.count)
        # self.threadforplot()
        self.threadpool = QThreadPool()

        """tryng q therad"""

        _show_data = Worker(self.a.show_dat, args=())
        _show_data.progress.connect(self.connectnow)
        _show_data.error.connect(self.problem_fun)
        self.threadpool.start(_show_data)
        
        
        #self.show_new_window()
    def setaxislimits(self,x1,y1,z1,x2,y2,z2):
            x1.axis(xmin=0, xmax=9, ymin=-500, ymax=500)
            y1.axis(xmin=0, xmax=9, ymin=-500, ymax=500)
            z1.axis(xmin=0, xmax=9, ymin=-500, ymax=500)
            x2.axis(xmin=0, xmax=9, ymin=-5, ymax=5)
            y2.axis(xmin=0, xmax=9, ymin=-5, ymax=5)
            z2.axis(xmin=0, xmax=9, ymin=-5, ymax=5)
            
    def problem_fun(self):
        print("problem")

    def _update_canvas(self,x1,y1,z1,x2,y2,z2,line1,line2,line3,line4,line5,line6):    
        if len(x1)>999 and len(y1)>999 and len(z1)>999 and len(x2)>999 and len(y2)>999 and len(z2)>999:
            t=np.linspace(0,9,1000)
            
            newlist1=x1[self.n:self.n+1000]
            newlist2=y1[self.n:self.n+1000]
            newlist3=z1[self.n:self.n+1000]
            newlist4=x2[self.n:self.n+1000]
            newlist5=y2[self.n:self.n+1000]
            newlist6=z2[self.n:self.n+1000]
            # line1, = x1.plot(t,np.array(newlist1),color='orange')
            # line2, = y1.plot(t,newlist2,color='green')
            # line3, = z1.plot(t,newlist3,color='red')
            # line4, = x1.plot(t,newlist4,color='blue')
            # line5, = y1.plot(t,newlist5,color='brown')
            # line6, = z1.plot(t,newlist6,color='yellow')
           
            line1.set_ydata(newlist1)
            line2.set_ydata(newlist2)
            line3.set_ydata(newlist3)
            line4.set_ydata(newlist4)
            line5.set_ydata(newlist5)
            line6.set_ydata(newlist6)
           
            line1.figure.canvas.draw()
            line2.figure.canvas.draw()
            line3.figure.canvas.draw()
            line4.figure.canvas.draw()
            line5.figure.canvas.draw()
            line6.figure.canvas.draw()
            
       
    def count1(self):
        self.c1+=1
        if self.c1 % 2 == 1:
            self.start_record()
        else:
            self.stop_record()  
       
        
    def count(self):
        self.c+=1
        if self.c % 2 == 1:
            self.start_record()
        else:
            self.stop_record()

    def stop_record(self):
        print('Hi')
        self.timer1.stop()
        self.counter=0
        self.counter1=0
        self.counter2=0
        self.a.kill_switch(0)
        self.ui.start.setText('Start Recording')
        print("Recording stopped")
        
    def recurring_timer(self):
        self.counter += 1
        self.ui.sec.setText(" %d" % self.counter)
        if self.counter>=60:
            self.counter1+=1
            self.ui.min.setText(" %d" % self.counter1)
            self.counter=0
            self.ui.sec.setText(" %d" % self.counter)
            if self.counter1>=60:
                self.counter2+=1
                self.ui.hour.setText(" %d" % self.counter2)
                self.counter=0
                self.ui.sec.setText(" %d" % self.counter)
                self.counter1=0
                self.ui.min.setText(" %d" % self.counter1)

    def threadforplot(self):
        reader1 = Thread(target=self.show_new_window,args=())
        reader1.start()
    
    def start_record(self):
        self.a.kill_switch(1)
        self.timer1 = QTimer()
        self.timer1.setInterval(1000)
        self.timer1.timeout.connect(self.recurring_timer)
        self.timer1.start()
        self.ui.start.setText('Stop Recording')
        #print(len(self.a.Ax))
        #header=['time','gyrox1','gyroy1','gyroz1','accelx1','accely1','accelz1','gyrox2','gyroy2','gyroz2','accelx2','accely2','accelz2']
        #self.a.ConnectToArduino(header,r'C:\Users\Dell\Desktop\MS Bioengineering\imu_data7.csv')
        
        print("Recording started")
        
    def show_new_window(self):
        time.sleep(1)
        
        # self.timer= QTimer()  
        # self.timer.setInterval(1)
        # self.timer.timeout.connect(self.connectnow)
        # self.timer.start() 
        while True:
            time.sleep(0.1)
            # self.connectnow()
            self._update_canvas(self.a.Ax,self.a.Ay,self.a.Az,self.a.Gx,self.a.Gy,self.a.Gz,self._line1,self._line2,self._line3,self._line4,self._line5,self._line6)
            self._update_canvas(self.a.Ax1,self.a.Ay1,self.a.Az1,self.a.Gx1,self.a.Gy1,self.a.Gz1,self._line11,self._line12,self._line13,self._line14,self._line15,self._line16)

        
    @pyqtSlot(list)
    def connectnow(self, data):
        
        # self._update_canvas(self.a.Ax,self.a.Ay,self.a.Az,self.a.Gx,self.a.Gy,self.a.Gz,self._line1,self._line2,self._line3,self._line4,self._line5,self._line6)
        # self._update_canvas(self.a.Ax1,self.a.Ay1,self.a.Az1,self.a.Gx1,self.a.Gy1,self.a.Gz1,self._line11,self._line12,self._line13,self._line14,self._line15,self._line16)
        #self._update_canvas(self.a.Ax3,self.a.Ay3,self.a.Az1,self.a.Gx1,self.a.Gy1,self.a.Gz1,self._line1,self._line2,self._line3,self._line4,self._line5,self._line6)
        #self._update_canvas(self.a.Ax4,self.a.Ay1,self.a.Az1,self.a.Gx1,self.a.Gy1,self.a.Gz1,self._line1,self._line2,self._line3,self._line4,self._line5,self._line6)
        #self._update_canvas(self.a.Ax5,self.a.Ay1,self.a.Az1,self.a.Gx1,self.a.Gy1,self.a.Gz1,self._line1,self._line2,self._line3,self._line4,self._line5,self._line6)
        #self._update_canvas(self.a.Ax6,self.a.Ay1,self.a.Az1,self.a.Gx1,self.a.Gy1,self.a.Gz1,self._line1,self._line2,self._line3,self._line4,self._line5,self._line6)
        #self._update_canvas(self.a.Ax7,self.a.Ay1,self.a.Az1,self.a.Gx1,self.a.Gy1,self.a.Gz1,self._line1,self._line2,self._line3,self._line4,self._line5,self._line6)
        #self._update_canvas(self.a.Ax8,self.a.Ay1,self.a.Az1,self.a.Gx1,self.a.Gy1,self.a.Gz1,self._line1,self._line2,self._line3,self._line4,self._line5,self._line6)
        self._update_canvas(data[0], data[1], data[2], data[3], data[5], data[6],self._line1,self._line2,self._line3,self._line4,self._line5,self._line6)
        self._update_canvas(data[7], data[8], data[9], data[10], data[11], data[12],self._line11,self._line12,self._line13,self._line14,self._line15,self._line16)
        
       
       

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())