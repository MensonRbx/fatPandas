# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 15:24:46 2023

@author: ChatGPT, mensonrbx

File creates .exe for app
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QComboBox, QDesktopWidget, QMainWindow, QWidget, QLabel, QPushButton, QSlider, QVBoxLayout

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        screen = QDesktopWidget().screenGeometry()

        # Calculate the center point of the screen
        center_x = (screen.width() - self.width()) / 2
        center_y = (screen.height() - self.height()) / 2

        # Set window properties
        self.setWindowTitle("My Window")
        self.setGeometry(int(center_x), int(center_y), 400, 300)

        # Add a label
        self.label = QLabel(self)
        self.label.setText("Select Plot")
        self.label.move(27, 10)

        #Add plot combo box
        self.plotChoice = QComboBox(self)
        self.plotChoice.addItem('Line Plot')
        self.plotChoice.addItem('Scatter Plot')
        self.plotChoice.addItem('Bar Plot')
        self.plotChoice.move(10, 50)

        # Add plot button
        self.plotButton = QPushButton(self)
        self.plotButton.setText("Generate Plot")
        self.plotButton.move(10, 250)
        self.plotButton.size()
        self.plotButton.clicked.connect(self.generate_plot)
        
    def generate_plot(self):
        selected_plot_type = self.plotChoice.currentText()
        
        if selected_plot_type == 'Line Plot':
            print('Generating line plot...')
        elif selected_plot_type == 'Scatter Plot':
            print('Generating scatter plot...')
        elif selected_plot_type == 'Bar Plot':
            print('Generating bar plot...')

if __name__ == '__main__':
   app = QApplication([])
   window = MyWindow()
   window.show()
   app.exec_()
    