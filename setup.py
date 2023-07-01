# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 15:24:46 2023

@author: ChatGPT (have to give it some credit), mensonrbx

File creates .exe for app
"""

import os
import pandas as pd

from src.fatPanda import FatPanda
from PyQt5.QtWidgets import QApplication, QFrame, QMessageBox, QFileDialog, QLineEdit, QScrollArea, QComboBox, QDesktopWidget, QMainWindow, QWidget, QLabel, QPushButton, QSlider, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap

plotTypeDict = {
    "Bar Plot": "bar",
    "Line Plot": "line",
    "Pie Plot": "pie",
    "Scatter Plot": "scatter",
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
        self.plotChoice.addItem("Pie Plot")
        self.plotChoice.move(10, 50)
        self.plotChoice.currentIndexChanged.connect(self.showPlotChoiceParameters)
        
        #bar
        self.barPlotOptions = QFrame(self)
        self.barPlotBox = QVBoxLayout(self.barPlotOptions)
        
        self.barTitle = QLabel()
        self.barTitle.setText("Bar Plot Options:")
        
        self.barXLabel = QLineEdit()
        self.barXLabel.setPlaceholderText("Name of x axis column...")
        
        self.barPlotBox.addWidget(self.barTitle)
        self.barPlotBox.addWidget(self.barXLabel)
        
        self.barPlotOptions.setVisible(False)
        self.barPlotOptions.setGeometry(20, 200, 200, 100)
        
        self.barPlotOptions.setStyleSheet("background-color: pink;")
        
        #line
        self.linePlotOptions = QFrame(self)
        self.linePlotBox = QVBoxLayout(self.linePlotOptions)
        
        self.lineTitle = QLabel()
        self.lineTitle.setText("Line Plot Options:")
        
        self.lineXLabel = QLineEdit()
        self.lineXLabel.setPlaceholderText("Name of x axis column...")
        
        self.linePlotBox.addWidget(self.lineTitle)
        self.linePlotBox.addWidget(self.lineXLabel)
        
        self.linePlotOptions.setVisible(True)
        self.linePlotOptions.setGeometry(20, 200, 200, 100)
    
        self.linePlotOptions.setStyleSheet("background-color: lightblue;")
        
        #scatter
        self.scatterPlotOptions = QFrame(self)
        self.scatterPlotBox = QVBoxLayout(self.scatterPlotOptions)
        
        self.scatterTitle = QLabel()
        self.scatterTitle.setText("Scatter Plot Options:")
        
        self.scatterCorrelation = QLineEdit()
        self.scatterCorrelation.setPlaceholderText("Minumum Correlation...")
        
        self.scatterPlotBox.addWidget(self.scatterTitle)
        self.scatterPlotBox.addWidget(self.scatterCorrelation)
        
        self.scatterPlotOptions.setVisible(False)
        self.scatterPlotOptions.setGeometry(20, 200, 200, 100)
    
        self.scatterPlotOptions.setStyleSheet("background-color: grey;")
    
        #pie plot optiona
        self.piePlotOptions = QFrame(self)
        self.piePlotBox = QVBoxLayout(self.piePlotOptions)
        
        self.pieTitle = QLabel()
        self.pieTitle.setText("Pie Plot Options:")
        
        self.pieProportion = QLineEdit()
        self.pieProportion.setPlaceholderText("Minumum Proportion...")
        
        self.piePlotBox.addWidget(self.pieTitle)
        self.piePlotBox.addWidget(self.pieProportion)
        
        self.piePlotOptions.setVisible(False)
        self.piePlotOptions.setGeometry(20, 200, 200, 100)
    
        self.piePlotOptions.setStyleSheet("background-color: magenta;")
    
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
        
    def showPlotChoiceParameters(self):
        plotType = self.plotChoice.currentText()
        
        self.barPlotOptions.setVisible(False)
        self.linePlotOptions.setVisible(False)
        self.scatterPlotOptions.setVisible(False)   
        self.piePlotOptions.setVisible(False)
        
        #horrendous, despicable, distraughtfull
        if plotType == "Bar Plot":
            self.barPlotOptions.setVisible(True)
        elif plotType == "Line Plot":
            self.linePlotOptions.setVisible(True)
        elif plotType == "Scatter Plot":
            self.scatterPlotOptions.setVisible(True)
        elif plotType == "Pie Plot":
            self.piePlotOptions.setVisible(True)

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
        
        method = getattr(pd, plotMethodName)
        dataFrame = method(self.currentFile)
        plotType = self.plotChoice.currentText()
        
        self.deleteCurrentImages()
        self.deleteImageFiles()
        

        self.fatPandaInstance.getPlots(
            dataFrame, 
            kind = plotTypeDict[plotType],
            kwargs = self._getKwargsForPlot(plotType)    
        )
        
        self.addPlotImages()
        
    def _getKwargsForPlot(self, plotType):
            
        if plotType == "Line Plot":
            return {"x": self.lineXLabel.text()}
        elif plotType == "Bar Plot":
            return {"x": self.barXLabel.text()}
        elif plotType == "Scatter Plot":
            return {"minCorrelation": float(self.scatterCorrelation.text())}    
        elif plotType == "Pie Plot":
            return {"minProportion": float(self.pieProportion.text())}
        
        
    def _getMappingMethod(self):
        
        for methodName, fileTypeArray in method_filetype_mapping.items():
            fileType = self.currentFile.split(".")[-1]
            if fileType in fileTypeArray: 
                return methodName
        
            
    def addPlotImages(self):
        
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
   window.deleteImageFiles()
    