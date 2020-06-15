import sys
from qtpy.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit
from EA import *
from HC import *
from PSO import *
from time import time
import threading

class QTUI(QWidget):
    
    def __init__(self):
        super().__init__()
        self.__size=3
        self.__pop=40
        self.__iter=1000
        self.__pM=0.5
        self.__result = QLabel(self)
        self.__timeLabel = QLabel(self)
        self.__timeLabel.move(50, 325)
        self.__eaButton = QPushButton('EA', self)
        self.__result.setWordWrap(True)
        self.__w = 1.0
        self.__c1 = 1.0
        self.__c2 = 2.5
        self.initUI()
        
    def initUI(self):
         self.setGeometry(600, 600, 700, 400)
         self.setWindowTitle('AI GUI')
         
         self.__eaButton.resize(100, 32)
         self.__eaButton.move(50, 350)
         self.__eaButton.clicked.connect(self.EA)
         
         hcButton = QPushButton('HC', self)
         hcButton.resize(100, 32)
         hcButton.move(150, 350)
         hcButton.clicked.connect(self.HC)
         
         psoButton = QPushButton('PSO', self)
         psoButton.resize(100, 32)
         psoButton.move(250, 350)
         psoButton.clicked.connect(self.PSO)
         
         self.__result.move(150, 50)
         self.__result.resize(200, 200)
         self.__result.setText("Result will be displayed here")
         
         sizeLabel = QLabel(self)
         sizeLabel.setText("Size: ")
         sizeLabel.move(500, 55)
         
         sizeEdit = QLineEdit(self)
         sizeEdit.resize(100, 32)
         sizeEdit.move(550, 50)
         sizeEdit.textEdited[str].connect(self.changedSize)
         
         popLabel = QLabel(self)
         popLabel.setText("Population: ")
         popLabel.move(470, 100)
         
         popEdit = QLineEdit(self)
         popEdit.resize(100, 32)
         popEdit.move(550, 90)
         popEdit.textEdited[str].connect(self.changedPop)
         
         iterLabel = QLabel(self)
         iterLabel.setText("Nr of iterations: ")
         iterLabel.move(450, 135)
         
         iterEdit = QLineEdit(self)
         iterEdit.resize(100, 32)
         iterEdit.move(550, 130)
         iterEdit.textEdited[str].connect(self.changedIter)
         
         pMLabel = QLabel(self)
         pMLabel.setText("Mutation prob (0-1): ")
         pMLabel.move(430, 175)
         
         pMEdit = QLineEdit(self)
         pMEdit.resize(100, 32)
         pMEdit.move(550, 170)
         pMEdit.textEdited[str].connect(self.changedPM)
         
         wLabel = QLabel(self)
         wLabel.setText("w: ")
         wLabel.move(500, 220)
         
         wEdit = QLineEdit(self)
         wEdit.resize(100, 32)
         wEdit.move(550, 210)
         wEdit.textEdited[str].connect(self.changedW)
         
         c1Label = QLabel(self)
         c1Label.setText("c1: ")
         c1Label.move(500, 250)
         
         c1Edit = QLineEdit(self)
         c1Edit.resize(100, 32)
         c1Edit.move(550, 250)
         c1Edit.textEdited[str].connect(self.changedC1)
         
         c2Label = QLabel(self)
         c2Label.setText("c2: ")
         c2Label.move(500, 280)
         
         c2Edit = QLineEdit(self)
         c2Edit.resize(100, 32)
         c2Edit.move(550, 290)
         c2Edit.textEdited[str].connect(self.changedC2)
         
         self.__timeLabel.setText("Execution time will be displayed here")
         
         self.show()
         
    def EA(self):
        cont = EAController(self.__size)
        start = time()
        #thr = threading.Thread(target=cont.control, args=(self.__pop, self.__iter, self.__pM))
        #thr.start()
        cont.control(self.__pop, self.__iter, self.__pM)
        end = time()
        self.__result.setText(cont.getBest())
        self.__timeLabel.setText("EA finished in " + str(end-start) + "seconds\n")
        
        
        
    def HC(self):
        cont=HCController(self.__size)
        start = time()
        cont.control(self.__iter)
        end = time()
        self.__result.setText(cont.getBest())
        self.__timeLabel.setText("HC finished in " + str(end-start) + "seconds\n")
        
    def PSO(self):
        cont=PSOController(self.__size, self.__pop)
        start = time()
        res = cont.control(self.__size, self.__pop, self.__iter, self.__w, self.__c1, self.__c2)
        end = time()
        self.__result.setText(res)
        self.__timeLabel.setText("PSO finished in " + str(end-start) + "seconds\n")
        
    def changedSize(self, text):
        self.__size=int(text)
        
    def changedPop(self, text):
        self.__pop=int(text)
        
    def changedIter(self, text):
        self.__iter=int(text)
        
    def changedPM(self, text):
        self.__pM=float(text)
        
    def changedW(self, text):
        self.__w=float(text)
        
    def changedC1(self, text):
        self.__c1=float(text)
        
    def changedC2(self, text):
        self.__c2=float(text)