# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 15:24:46 2023

@author: ChatGPT, mensonrbx

File creates .exe for app
"""

import os
import importlib

import pandas as pd

from src.fatPanda import FatPanda

from time import sleep

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog, QScrollArea, QComboBox, QDesktopWidget, QMainWindow, QWidget, QLabel, QPushButton, QSlider, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap

plotTypeDict = {
    "Bar Plot": "bar",
    "Line Plot": "line",
    "Scatter Plot": "scatter",
    "Pie Plot": "pie",
    "Histogram": "hist",
    "Box Plot": "box",
    "Area Plot": "area",
    
}

method_filetype_mapping = {
    'read_csv': ['csv'],
    'read_excel': ['xls', 'xlsx'],
    'read_json': ['json'],
    'read_html': ['html']
}

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.fatPandaInstance = FatPanda()
        self.currentFile = None
    
        # Set window properties
       # self.setWindowIcon()
        self.setWindowTitle("Fat Panda")
        self.setGeometry(100, 100, 750, 500)

        # Add plot selection
        self.plotLabel = QLabel(self)
        self.plotLabel.setText("Select Plot")
        self.plotLabel.move(27, 10)

        self.plotChoice = QComboBox(self)
        self.plotChoice.addItem('Line Plot')
        self.plotChoice.addItem('Scatter Plot')
        self.plotChoice.addItem('Bar Plot')
        self.plotChoice.move(10, 50)
 
        #Select data file
        self.selectLabel = QLabel(self)
        self.selectLabel.setText("Select Data")
        self.selectLabel.move(137, 10)
        
        self.selectData = QPushButton(self)
        self.selectData.setText("Select...")
        self.selectData.move(120, 50)
        self.selectData.size()
        self.selectData.clicked.connect(self.getDataFileToPlot)
        
        self.nameOfFileLabel = QLabel(self)
        self.nameOfFileLabel.setText("File Name")
        self.nameOfFileLabel.move(137, 80)
        
        # Create a scroll area widget
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setGeometry(self.width() - 420, 40, 400, 400)
      
        # Create a container widget for the images
        self.imageContainer = QWidget()
        self.imageLayout = QVBoxLayout(self.imageContainer)
        self.imageContainer.setGeometry(0, 0, 100, 1500)  # Set larger size than the scroll area
        self.scrollArea.setWidget(self.imageContainer)
        self.scrollArea.setWidgetResizable(True)

        # Final Plot button
        self.plotButton = QPushButton(self)
        self.plotButton.setText("Generate Plot")
        self.plotButton.move(10, self.height() - 60)
        self.plotButton.size()
        self.plotButton.clicked.connect(self.onPlotButtonClicked)
       
    def getDataFileToPlot(self):
        self.currentFile, _ = QFileDialog.getOpenFileName(self, 'Open File', '.', 'All Files (*.*)')
        
        if self.currentFile:
            name = self.currentFile.split("/")[-1]
            self.nameOfFileLabel.setText(name)
        
    def onPlotButtonClicked(self):
        
        if not self.currentFile:
            warning = QMessageBox()
            warning.setIcon(QMessageBox.Warning)
            warning.setText("No Plot Selected!")
            warning.setWindowTitle("No Plot Selected")
            warning.setStandardButtons(QMessageBox.Ok)
            warning.exec_()
        else:
            self._generatePlot()
        
        
    def _generatePlot(self):
        plotMethodName = self._getMappingMethod()
        
        assert plotMethodName, "Error at _generate plot, no appropriate plot method found"
        
        self.deleteCurrentImages()
        self.deleteImageFiles()
        
        method = getattr(pd, plotMethodName)
        
        df = method(self.currentFile)
        
        self.fatPandaInstance.getPlots(
            df, 
            kind = plotTypeDict[self.plotChoice.currentText()],
            kwargs = {
                "x": "Year/Month"
            }    
        )
        
        self.addPlotImages()
        
    def _getMappingMethod(self):
        
        for methodName, fileTypeArray in method_filetype_mapping.items():
            fileType = self.currentFile.split(".")[-1]
            print(fileType)
            if fileType in fileTypeArray: 
                return methodName
        
            
    def addPlotImages(self):
        
        print("plotting images")
        
        home_dir = os.getcwd()
        path = f"{home_dir}\\temp"
        
        for filename in set(os.listdir(path)):
            
            if not filename.endswith('.png'):
                continue

            pixmap = QPixmap(os.path.join(path, filename))
            label = QLabel(self.imageContainer)
            label.setPixmap(pixmap)
            label.setFixedSize(600, 400)
            self.imageLayout.addWidget(label)
    
    def deleteCurrentImages(self):
        while self.imageLayout.count():
            child = self.imageLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            
    def deleteImageFiles(self):
        home_dir = os.getcwd()
        path = f"{home_dir}\\temp"
        for filename in set(os.listdir(path)):
            filePath = os.path.join(path, filename)
            try:
                os.remove(filePath)
            except:
                continue

if __name__ == '__main__':
   app = QApplication([])
   window = MyWindow()
   window.show()
   app.exec_()
   print("Done!")
    