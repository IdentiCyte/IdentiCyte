"""
   File Name: CellVerUI.py
   Version: 1.0
   Author: Guillaume Garnier
   Date Modified: 2018-11-21
   License: GNU-GPL-3.0-or-later
   Python Version 3.5
   Description: Defines the window through which a cell can be manually identified.
"""

from tkinter import *
from PIL import ImageTk, Image


class CellVerUI:
    """
    The UI window that pops up for user verification.

    Parameters
    ----------
    window : MainWindow
        The main GUI window
    image : ndarray
        An image of the cell to be verified.
    typeArray : list
        A list of strings, each of which represents a category

    Returns
    -------
    None, but self.type is referenced to determine what the user classified the cell as.
    """
    def __init__(self, window, image, typeArray):
        self.master = window
        self.im = Image.fromarray(image)

        # Options for the window
        window.attributes('-topmost', 1)
        window.attributes('-topmost', 0)
        window.title("Manual Identification")

        # Define the types of cell
        self.cellTypes = typeArray

        self.type = StringVar()
        self.type.set(self.cellTypes[0])

        # Define some frames for positioning
        self.top = Frame(window)
        self.bot = Frame(window)
        self.top.pack(side=TOP)
        self.bot.pack(side=BOTTOM, fill=BOTH, expand=False)

        # Label at the top
        self.label = Label(window, text="What type of cell is this?")
        self.label.pack(in_=self.top, side=TOP)

        # Display the current cell
        self.image = ImageTk.PhotoImage(self.im)
        self.imLab = Label(window, image=self.image)
        self.imLab.image = self.image
        self.imLab.pack(in_=self.top, side=BOTTOM)

        # Dropdown Menu
        self.types = OptionMenu(window, self.type, *self.cellTypes)
        self.types.pack(in_=self.bot, side=LEFT)

        # Ignore button
        self.ignore = Button(window, text="Ignore", command=lambda: self.ignored())
        self.ignore.pack(in_=self.bot, side=RIGHT)

        # When the cell type has been selected
        self.ok = Button(window, text="Select", command=lambda: self.master.quit())
        self.ok.pack(in_=self.bot, side=RIGHT)

        # When the window is closed with the x in the corner
        self.master.protocol("WM_DELETE_WINDOW", lambda: self.ignored())

    # Handle closing
    def ignored(self):
        self.type.set("Ignore")
        self.master.quit()
