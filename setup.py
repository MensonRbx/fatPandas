# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 15:24:46 2023

@author: ChatGPT, mensonrbx

File creates .exe for app
"""

import os
import importlib

import pandas as pd

import src.fatPanda as FatPanda_Module


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

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.fatPandaInstance = FatPanda_Module.FatPanda()
        self.currentFile = None
        
        screen = QDesktopWidget().screenGeometry()

        # Calculate the center point of the screen
        center_x = (screen.width() - self.width()) / 2
        center_y = (screen.height() - self.height()) / 2

        # Set window properties
        self.setWindowTitle("My Window")
        self.setGeometry(int(center_x), int(center_y), 700, 650)

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
        self.scrollArea.setGeometry(self.width() - 420, 40, 380, 280)
      
        # Create a container widget for the images
        self.imageContainer = QWidget()
        self.imageLayout = QVBoxLayout(self.imageContainer)
        self.imageContainer.setGeometry(0, 0, 400, 1000)  # Set larger size than the scroll area
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
    
        print("ere0")
        
        if not self.currentFile:
            warning = QMessageBox()
            warning.setIcon(QMessageBox.Warning)
            warning.setText("No Plot Selected!")
            warning.setWindowTitle("No Plot Selected")
            warning.setStandardButtons(QMessageBox.Ok)
            warning.exec_()
        else:
            print("ere1")
            self._generatePlot()
        
        
    def _generatePlot(self):
        self.deleteCurrentImages()
        
        #currently .csv, will expand
        df = pd.read_csv(self.currentFile)
        
        self.fatPandaInstance.getPlots(
            df, 
            kind = plotTypeDict[self.plotChoice.currentText()],
            kwargs = {
                "x": "Year/Month"
            }    
        )
        
        self.addPlotImages()
            
    def addPlotImages(self):
        
        print("plotting images")
        
        path = "src\\fatPanda\\temp"
        
        for filename in set(os.listdir(path)):
            
            print(filename)
            
            if not filename.endswith('.png') or not filename.endswith(".jpg"):
                return
            pixmap = QPixmap(os.path.join(path, filename))
            label = QLabel(self.imageContainer)
            label.setPixmap(pixmap)
            label.setFixedSize(300, 300)
            label.setScaledContents(True)
            self.imageLayout.addWidget(label)
    
    def deleteCurrentImages(self):
        
        path = "src\\fatPanda\\temp"
        
        while self.imageLayout.count():
            child = self.imageLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        for filename in set(os.listdir(path)):
            continue


if __name__ == '__main__':
   app = QApplication([])
   window = MyWindow()
   window.show()
   app.exec_()
   print("Done!")
    