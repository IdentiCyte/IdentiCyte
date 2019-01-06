"""
   File Name: main.py
   Author: Guillaume Garnier
   Date Modified: 2018-12-13
   License: GNU-GPL-3.0-or-later
   Python Version 3.5
   Description: The main document of the project. Runs everything else.
"""
from tkinter import Tk
from mttkinter import *
from IdentiCyte.MainUI import MainWindow


def main():
    root = Tk()
    my_gui = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()