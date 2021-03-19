# Graphical interface for multi-signal visualization and interaction with ELEMYO sensors
# 2020-06-15 by ELEMYO (https://github.com/ELEMYO/ELEMYO GUI)
# 
# Changelog:
#    2021-03-19 - initial release

# Code is placed under the MIT license
# Copyright (c) 2021 ELEMYO
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ===============================================

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt 
import sys
import serial
import pyqtgraph as pg
import numpy as np
import time
import serial.tools.list_ports

# Main window
class GUI(QtWidgets.QMainWindow):
    # Initialize constructor
    def __init__(self):
          super(GUI, self).__init__()
          self.initUI()
    # Custom constructor
    def initUI(self): 
        # Values
        COM='' #Example: COM='COM6'
        baudRate = 115200 #Serial frequency
        self.cycleNumber = 0; #Number of data reading cycle
        self.l = 0 #Current point
        self.dt = 0.0012 #Updating time in seconds
        self.fs = 1 / self.dt #Updating frequency in Hz
        self.dataWidth = 30000 #Maximum count of data points
        self.Time = [0]*self.dataWidth #Time array
        self.Data1 = [0]*self.dataWidth #Data array
        self.Data2 = [0]*self.dataWidth #Data array
        self.Data3 = [0]*self.dataWidth #Data array
        self.Data4 = [0]*self.dataWidth #Data array
        self.timeWidth = 10 #Time width of plot
        self.msg_end = np.array([0])
        self.setWindowTitle("EMG/ECG/EEG - Terminal Multiple (4) | ELEMYO" + "    ( COM Port not found )")
        self.setWindowIcon(QtGui.QIcon('img/icon.png'))
        # Menu panel
        startAction = QtGui.QAction(QtGui.QIcon('img/start.png'), 'Start (Enter)', self)
        startAction.setShortcut('Return')
        startAction.triggered.connect(self.start)
        stopAction = QtGui.QAction(QtGui.QIcon('img/pause.png'), 'Stop (Space)', self)
        stopAction.setShortcut('Space')
        stopAction.triggered.connect(self.stop)
        refreshAction = QtGui.QAction(QtGui.QIcon('img/refresh.png'), 'Refresh (R)', self)
        refreshAction.setShortcut('r')
        refreshAction.triggered.connect(self.refresh)
        exitAction = QtGui.QAction(QtGui.QIcon('img/out.png'), 'Exit (Esc)', self)
        exitAction.setShortcut('Esc')
        exitAction.triggered.connect(self.close)
        # Toolbar
        toolbar = self.addToolBar('Tool')
        toolbar.addAction(startAction)
        toolbar.addAction(stopAction)
        toolbar.addAction(refreshAction)
        toolbar.addAction(exitAction)
        # Plot widget for graphic 1
        self.pw1 = pg.PlotWidget(background = (21 , 21, 21, 255))
        self.pw1.showGrid(x = True, y = True, alpha = 0.7) 
        self.plot1 = self.pw1.plot()
        self.plot1.setPen(color=(100,255,255), width=1)
        # Plot widget for graphic 2
        self.pw2 = pg.PlotWidget(background = (13 , 13, 13, 255))
        self.pw2.showGrid(x = True, y = True, alpha = 0.7) 
        self.plot2 = self.pw2.plot()
        self.plot2.setPen(color=(100,255,255), width=1)
        # Plot widget for graphic 3
        self.pw3 = pg.PlotWidget(background = (21 , 21, 21, 255))
        self.pw3.showGrid(x = True, y = True, alpha = 0.7) 
        self.plot3 = self.pw3.plot()
        self.plot3.setPen(color=(100,255,255), width=1)
        # Plot widget for graphic 4
        self.pw4 = pg.PlotWidget(background = (13 , 13, 13, 255))
        self.pw4.showGrid(x = True, y = True, alpha = 0.7) 
        self.plot4 = self.pw4.plot()
        self.plot4.setPen(color=(100,255,255), width=1)
        # Plot widget for graphic 5
        self.pw5 = pg.PlotWidget(background = (21 , 21, 21, 255))
        self.pw5.showGrid(x = True, y = True, alpha = 0.7) 
        self.plot5 = self.pw5.plot()
        self.plot5.setPen(color=(100,255,255), width=1)
        # Plot widget for graphic 6
        self.pw6 = pg.PlotWidget(background = (13 , 13, 13, 255))
        self.pw6.showGrid(x = True, y = True, alpha = 0.7) 
        self.plot6 = self.pw6.plot()
        self.plot6.setPen(color=(100,255,255), width=1)
        # Plot widget for graphic 7
        self.pw7 = pg.PlotWidget(background = (21 , 21, 21, 255))
        self.pw7.showGrid(x = True, y = True, alpha = 0.7) 
        self.plot7 = self.pw7.plot()
        self.plot7.setPen(color=(100,255,255), width=1)
        # Plot widget for graphic 8
        self.pw8 = pg.PlotWidget(background = (13 , 13, 13, 255))
        self.pw8.showGrid(x = True, y = True, alpha = 0.7) 
        self.plot8 = self.pw8.plot()
        self.plot8.setPen(color=(100,255,255), width=1)
        # Plot widget for graphic 9
        self.pw9 = pg.PlotWidget(background = (21 , 21, 21, 255))
        self.pw9.showGrid(x = True, y = True, alpha = 0.7) 
        self.plot9 = self.pw9.plot()
        self.plot9.setPen(color=(100,255,255), width=1)
        
        # Styles
        centralStyle = "color: rgb(255, 255, 255); background-color: rgb(13, 13, 13);"
        # Settings zone     
        self.l11 = QtWidgets.QLabel("")
        self.l11.setStyleSheet("font-size: 25px; background-color: rgb(21,21,21);")
        self.l13 = QtWidgets.QLabel("")
        self.l13.setStyleSheet("font-size: 25px; background-color: rgb(21,21,21);")
        self.l15 = QtWidgets.QLabel("")
        self.l15.setStyleSheet("font-size: 25px; background-color: rgb(21,21,21);")
        self.l17 = QtWidgets.QLabel("")
        self.l17.setStyleSheet("font-size: 25px; background-color: rgb(21,21,21);")
        self.l19 = QtWidgets.QLabel("")
        self.l19.setStyleSheet("font-size: 25px; background-color: rgb(21,21,21);")
        self.l1 = QtWidgets.QLabel(" 1 ")
        self.l1.setStyleSheet("font-size: 25px; background-color: rgb(153,0,0); border-radius: 14px;")
        self.l2 = QtWidgets.QLabel(" 2")
        self.l2.setStyleSheet("font-size: 25px; background-color: rgb(229, 104, 19); border-radius: 14px;") 
        self.l3 = QtWidgets.QLabel(" 3 ")
        self.l3.setStyleSheet("font-size: 25px; background-color: rgb(221, 180, 10); border-radius: 14px;")
        self.l4 = QtWidgets.QLabel(" 4 ")
        self.l4.setStyleSheet("font-size: 25px; background-color: rgb(30, 180, 30); border-radius: 14px;")
        # Main widget
        centralWidget = QtWidgets.QWidget()
        centralWidget.setStyleSheet(centralStyle)
        # Layout
        vbox = QtWidgets.QVBoxLayout()
        
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.l11, 0, 1)
        layout.addWidget(self.l1, 0, 1, Qt.AlignVCenter)
        layout.addWidget(self.l2, 1, 1, Qt.AlignVCenter)
        layout.addWidget(self.l13, 2, 1)
        layout.addWidget(self.l3, 2, 1, Qt.AlignVCenter)
        layout.addWidget(self.l4, 3, 1, Qt.AlignVCenter)
        
        layout.addWidget(self.pw1, 0, 2)
        layout.addWidget(self.pw2, 1, 2)
        layout.addWidget(self.pw3, 2, 2)
        layout.addWidget(self.pw4, 3, 2)
        layout.setColumnStretch(2, 2)
        
        vbox.addLayout(layout)
        centralWidget.setLayout(vbox)
        self.setCentralWidget(centralWidget)  
        self.showMaximized()
        self.show()
        # Serial monitor
        self.monitor = SerialMonitor(COM, baudRate)
        self.monitor.bufferUpdated.connect(self.updateListening, QtCore.Qt.QueuedConnection)
    # Start working
    def start(self):
        self.monitor.running = True
        self.monitor.start()
    # Pause
    def stop(self):
        self.monitor.running = False    
    # Refresh
    def refresh(self):
        if self.cycleNumber<=20:
            self.cycleNumber = 0;
        self.l = 0 #Current point
        self.msg_end = 0        
        self.imgTranslateNum = -self.imgTranslateNum
    # Update
    def updateListening(self, msg):
        # Update variables
        if (self.cycleNumber == 0):
            self.setWindowTitle("EMG/ECG/EEG - Terminal Multiple (4) | ELEMYO " + 
                                "    ( " + self.monitor.COM + " , " + str(self.monitor.baudRate) + " baud )")
        # Parsing data from serial buffer
        msg = msg.decode(errors='ignore')
        self.cycleNumber += 1
        if len(msg) >= 2:
            msg_end_n = msg.rfind("\r", 1)
            msg_begin = self.msg_end
            self.msg_end = msg[msg_end_n:len(msg)]
            if(self.l > 2):
                msg = msg_begin + msg[0:msg_end_n]
            for st in msg.split('\r\n'):
                s = st.split(' ')
                if (len(s) == 4) :
                     if ( self.l == self.dataWidth):
                         self.l = 0
                     self.Data1[self.l] = int(s[0])
                     self.Data2[self.l] = int(s[1])
                     self.Data3[self.l] = int(s[2])
                     self.Data4[self.l] = int(s[3])
                     self.Time[self.l] = self.Time[self.l - 1] + self.dt
                     self.l = self.l + 1
        # Shift the boundaries of the graph
        timeCount = self.Time[self.l - 1] // self.timeWidth
        # Update plot
        if (self.l > 3):
            # Signal plots
            self.pw1.setXRange(self.timeWidth * timeCount, self.timeWidth * ( timeCount + 1))
            self.pw2.setXRange(self.timeWidth * timeCount, self.timeWidth * ( timeCount + 1))
            self.pw3.setXRange(self.timeWidth * timeCount, self.timeWidth * ( timeCount + 1))
            self.pw4.setXRange(self.timeWidth * timeCount, self.timeWidth * ( timeCount + 1))  
            self.plot1.setData(y=self.Data1[0: self.l-1], x = self.Time[0: self.l-1])
            self.plot2.setData(y=self.Data2[0: self.l-1], x = self.Time[0: self.l-1])
            self.plot3.setData(y=self.Data3[0: self.l-1], x = self.Time[0: self.l-1])
            self.plot4.setData(y=self.Data4[0: self.l-1], x = self.Time[0: self.l-1])
                    
    # Exit event
    def closeEvent(self, event):
        self.monitor.ser.close()
        event.accept()

# Serial monitor class
class SerialMonitor(QtCore.QThread):
    bufferUpdated = QtCore.pyqtSignal(bytes)
    # Custom constructor
    def __init__(self, COM, baudRate):
        QtCore.QThread.__init__(self)
        self.running = False
        self.COM = COM
        self.baudRate = baudRate
        self.baudRate = baudRate
        self.checkPort = 1

    # Listening port
    def run(self):
        while self.running is True:
            while self.COM == '': 
                ports = serial.tools.list_ports.comports(include_links=False)
                for port in ports :
                    self.COM = port.device
                if self.COM != '':
                    time.sleep(0.5)
                    self.ser = serial.Serial(self.COM, self.baudRate)
                    self.checkPort = 0
            while self.checkPort:
                ports = serial.tools.list_ports.comports(include_links=False)
                for port in ports :
                    if self.COM == port.device:
                        time.sleep(0.5)
                        self.ser = serial.Serial(self.COM, self.baudRate)
                        self.checkPort = 0
                   
            # Waiting for data
            while (self.ser.inWaiting() == 0):
                pass
            # Reading data
            msg = self.ser.read( self.ser.inWaiting() )
            if msg:
                #Parsing data
                self.bufferUpdated.emit(msg)
                time.sleep(0.05)
                
# Starting program       
if __name__ == '__main__':
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    window = GUI()
    window.show()
    window.start()
    sys.exit(app.exec_())