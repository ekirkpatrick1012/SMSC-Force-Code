# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#include <QFileDoalog>
import matplotlib, pandas, scipy
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
import sys, os
from pathlib import Path


class pathCall(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):

            

        self.fileSelect = QFileDialog()
        self.setCentralWidget(self.fileSelect)
        self.home_dir = str(Path.home())
        self.dataPath = r"C:\Users\EKirkpatrick\OneDrive - Vanderbilt\Desktop\Data"
        self.fileSelect.setDirectory(self.dataPath)
        self.tracePath = self.fileSelect.getOpenFileName(self, 'Open File')
        self.calPath = self.fileSelect.getOpenFileName(self, 'Open File')
        self.sPath = self.fileSelect.getOpenFileName(self, 'Open File')

    def button(self):
        btn = QtGui.QPushButton('Quit', self)
        btn.clicked.connect(self.quitApp)
        
    def quitApp(self):
        QtCore.QCoreApplication.instance().quit()


        

    
