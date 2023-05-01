# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 15:17:23 2023

@author: ChatGPT (lets see what this puppy can do), mensonrbx
"""

import sys

from tkinter import Tk, Button, Frame

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.quit_button = Button(self, text="Quit", command=self.quit)
        self.quit_button.pack(side="bottom")

    def quit(self):
        self.master.destroy()
        sys.exit()

root = Tk()
app = Application(master=root)

root.protocol("WM_")

root.protocol("WM_DELETE_WINDOW", app.quit)
app.mainloop()