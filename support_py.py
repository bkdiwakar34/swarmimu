
from PyQt5 import QtWidgets

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import *

import numpy as np
from PyQt5.QtCore import QSize, Qt,QTimer
from reading_imu_data  import SerialPort
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar)
from PyQt5.QtWidgets import QWidget,QGridLayout,QStatusBar,QMessageBox,QVBoxLayout,QAction
from matplotlib.figure import Figure
from threading import Thread
import sys

def initialize_graphs(self):
    dynamic_canvas1 = FigureCanvasQTAgg(Figure(figsize=(5,3)))
    
    self._ax1,self._ay1,self._az1,self._gx1,self._gy1,self._gz1 = dynamic_canvas1.figure.subplots(nrows=6,sharex=True)
    layout1= QGridLayout()
    layout1.addWidget(dynamic_canvas1)
    layout1.addWidget(NavigationToolbar(dynamic_canvas1, self))
    self.ui.tab_2.setLayout(layout1)
    dynamic_canvas2 = FigureCanvasQTAgg(Figure(figsize=(5,3)))
    self._ax2,self._ay2,self._az2,self._gx2,self._gy2,self._gz2 = dynamic_canvas2.figure.subplots(nrows=6,sharex=True)
    dynamic_canvas3 = FigureCanvasQTAgg(Figure(figsize=(5,3)))
    self._ax3,self._ay3,self._az3,self._gx3,self._gy3,self._gz3 = dynamic_canvas3.figure.subplots(nrows=6,sharex=True)
    dynamic_canvas4 = FigureCanvasQTAgg(Figure(figsize=(5,3)))
    self._ax4,self._ay4,self._az4,self._gx4,self._gy4,self._gz4 = dynamic_canvas4.figure.subplots(nrows=6,sharex=True)
    dynamic_canvas5 = FigureCanvasQTAgg(Figure(figsize=(5,3)))
    self._ax5,self._ay5,self._az5,self._gx5,self._gy5,self._gz5 = dynamic_canvas5.figure.subplots(nrows=6,sharex=True)
    dynamic_canvas6 = FigureCanvasQTAgg(Figure(figsize=(5,3)))
    self._ax6,self._ay6,self._az6,self._gx6,self._gy6,self._gz6 = dynamic_canvas6.figure.subplots(nrows=6,sharex=True)
    dynamic_canvas7 = FigureCanvasQTAgg(Figure(figsize=(5,3)))
    self._ax7,self._ay7,self._az7,self._gx7,self._gy7,self._gz7 = dynamic_canvas7.figure.subplots(nrows=6,sharex=True)
    dynamic_canvas8 = FigureCanvasQTAgg(Figure(figsize=(5,3)))
    self._ax8,self._ay8,self._az8,self._gx8,self._gy8,self._gz8 = dynamic_canvas8.figure.subplots(nrows=6,sharex=True)
    
    self.t=np.linspace(0,9,1000)
    self._line1, = self._ax1.plot(self.t,self.t,color='orange')
    self._line2, = self._ay1.plot(self.t,self.t,color='green')
    self._line3, = self._az1.plot(self.t,self.t,color='red')
    self._line4, = self._gx1.plot(self.t,self.t,color='blue')
    self._line5, = self._gy1.plot(self.t,self.t,color='brown')
    self._line6, = self._gz1.plot(self.t,self.t,color='yellow')
    self._line11, = self._ax2.plot(self.t,self.t,color='orange')
    self._line12, = self._ay2.plot(self.t,self.t,color='green')
    self._line13, = self._az2.plot(self.t,self.t,color='red')
    self._line14, = self._gx2.plot(self.t,self.t,color='blue')
    self._line15, = self._gy2.plot(self.t,self.t,color='brown')
    self._line16, = self._gz2.plot(self.t,self.t,color='yellow')
    self._line21, = self._ax3.plot(self.t,self.t,color='orange')
    self._line22, = self._ay3.plot(self.t,self.t,color='green')
    self._line23, = self._az3.plot(self.t,self.t,color='red')
    self._line24, = self._gx3.plot(self.t,self.t,color='blue')
    self._line25, = self._gy3.plot(self.t,self.t,color='brown')
    self._line26, = self._gz3.plot(self.t,self.t,color='yellow')
    self._line31, = self._ax4.plot(self.t,self.t,color='orange')
    self._line32, = self._ay4.plot(self.t,self.t,color='green')
    self._line33, = self._az4.plot(self.t,self.t,color='red')
    self._line34, = self._gx4.plot(self.t,self.t,color='blue')
    self._line35, = self._gy4.plot(self.t,self.t,color='brown')
    self._line36, = self._gz4.plot(self.t,self.t,color='yellow')
    self._line41, = self._ax5.plot(self.t,self.t,color='orange')
    self._line42, = self._ay5.plot(self.t,self.t,color='green')
    self._line43, = self._az5.plot(self.t,self.t,color='red')
    self._line44, = self._gx5.plot(self.t,self.t,color='blue')
    self._line45, = self._gy5.plot(self.t,self.t,color='brown')
    self._line46, = self._gz5.plot(self.t,self.t,color='yellow')
    self._line51, = self._ax6.plot(self.t,self.t,color='orange')
    self._line52, = self._ay6.plot(self.t,self.t,color='green')
    self._line53, = self._az6.plot(self.t,self.t,color='red')
    self._line54, = self._gx6.plot(self.t,self.t,color='blue')
    self._line55, = self._gy6.plot(self.t,self.t,color='brown')
    self._line56, = self._gz6.plot(self.t,self.t,color='yellow')
    self._line61, = self._ax7.plot(self.t,self.t,color='orange')
    self._line62, = self._ay7.plot(self.t,self.t,color='green')
    self._line63, = self._az7.plot(self.t,self.t,color='red')
    self._line64, = self._gx7.plot(self.t,self.t,color='blue')
    self._line65, = self._gy7.plot(self.t,self.t,color='brown')
    self._line66, = self._gz7.plot(self.t,self.t,color='yellow')
    self._line71, = self._ax8.plot(self.t,self.t,color='orange')
    self._line72, = self._ay8.plot(self.t,self.t,color='green')
    self._line73, = self._az8.plot(self.t,self.t,color='red')
    self._line74, = self._gx8.plot(self.t,self.t,color='blue')
    self._line75, = self._gy8.plot(self.t,self.t,color='brown')
    self._line76, = self._gz8.plot(self.t,self.t,color='yellow')
    
    # Set up a Line2D.
    
    self.setaxislimits(self._ax1,self._ay1,self._az1,self._gx1,self._gy1,self._gz1)
    self.setaxislimits(self._ax2,self._ay2,self._az2,self._gx2,self._gy2,self._gz2)
    self.setaxislimits(self._ax3,self._ay3,self._az3,self._gx3,self._gy3,self._gz3)
    self.setaxislimits(self._ax4,self._ay4,self._az4,self._gx4,self._gy4,self._gz4)
    self.setaxislimits(self._ax5,self._ay5,self._az5,self._gx5,self._gy5,self._gz5)
    self.setaxislimits(self._ax6,self._ay6,self._az6,self._gx6,self._gy6,self._gz6)
    self.setaxislimits(self._ax7,self._ay7,self._az7,self._gx7,self._gy7,self._gz7)
    self.setaxislimits(self._ax8,self._ay8,self._az8,self._gx8,self._gy8,self._gz8)
    
    layout2= QGridLayout()
    layout2.addWidget(dynamic_canvas2)
    layout2.addWidget(NavigationToolbar(dynamic_canvas2, self))
    layout3= QGridLayout()
    layout3.addWidget(dynamic_canvas3)
    layout3.addWidget(NavigationToolbar(dynamic_canvas3, self))
    layout4= QGridLayout()
    layout4.addWidget(dynamic_canvas4)
    layout4.addWidget(NavigationToolbar(dynamic_canvas4, self))
    layout5= QGridLayout()
    layout5.addWidget(dynamic_canvas5)
    layout5.addWidget(NavigationToolbar(dynamic_canvas5, self))
    layout6= QGridLayout()
    layout6.addWidget(dynamic_canvas6)
    layout6.addWidget(NavigationToolbar(dynamic_canvas6, self))
    layout7= QGridLayout()
    layout7.addWidget(dynamic_canvas7)
    layout7.addWidget(NavigationToolbar(dynamic_canvas7, self))
    layout8= QGridLayout()
    layout8.addWidget(dynamic_canvas8)
    layout8.addWidget(NavigationToolbar(dynamic_canvas8, self))
    
    self.ui.tab_3.setLayout(layout2)
    self.ui.tab_4.setLayout(layout3)
    self.ui.tab_5.setLayout(layout4)
    self.ui.tab_6.setLayout(layout5)
    self.ui.tab_7.setLayout(layout6)
    self.ui.tab_8.setLayout(layout7)
    self.ui.tab_9.setLayout(layout8)