"""
   File Name: MainUI.py
   Version: 1.0
   Author: Guillaume Garnier
   Date Modified: 2018-11-21
   License: GNU-GPL-3.0-or-later
   Python Version 3.5
   Description: Handles the main GUI window and calls all the other functions.
"""

from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from mttkinter import *
import os
import IdentiCyte.ExtractCells as EC
from IdentiCyte.CellRecognitionDriver import driver
from IdentiCyte.ConstructLibrary import compileLibrary
import traceback
from threading import Thread
import IdentiCyte.Globs as Globs
from IdentiCyte.DisplayIdentified import display
from IdentiCyte.FolderBatch import batch


class MainWindow():
    """
    The main window of the program.
    """
    def __init__(self, master):
        # type: (Tk) -> None
        self.master = master
        self.userVer = BooleanVar()
        self.color = StringVar()
        self.img = StringVar()
        self.bits = IntVar()
        self.pcThresh = DoubleVar()
        self.confThresh = DoubleVar()
        self.method = StringVar()
        self.cellSize = IntVar()
        self.cellRadius = IntVar()
        self.brigthfield = BooleanVar()
        self.batch = BooleanVar()
        self.thread = Thread()
        self.dispThread = Thread()
        self.near = IntVar()
        self.version = "1.0"
        Globs.end = False

        self.bits.set(3)
        self.color.set('B')
        self.userVer.set(False)
        self.pcThresh.set(90)
        self.confThresh.set(50)
        self.method.set('Otsu')
        self.cellSize.set(9000)
        self.brigthfield.set(True)
        self.batch.set(True)
        self.cellRadius.set(155)
        self.near.set(10)

        self.select = ttk.Notebook()
        self.main_ = ttk.Frame(self.select)
        self.library_ = ttk.Frame(self.select)
        self.options_ = ttk.Frame(self.select)
        self.check_ = ttk.Frame(self.select)
        self.select.add(self.main_, text='Analysis')
        self.select.add(self.check_, text='Review')
        self.select.add(self.library_, text='Library')
        self.select.add(self.options_, text='Options')
        self.select.pack(fill=BOTH)

        # Default folders
        self.lib = StringVar()
        self.lib.set(os.path.join(os.getcwd(), 'Library'))
        self.lib.set('D:\\IdentiCyte\\Library')
        self.infile = StringVar()
        self.infile.set(os.getcwd())
        self.infile.set('D:\\IdentiCyte\\Image Samples')

        # Define some frames for positioning
        self.top = Frame(self.main_)
        self.bot = Frame(self.main_)
        self.top.pack(side=TOP)
        self.bot.pack(side=BOTTOM, fill=BOTH, expand=False)

        # Output
        self.out = Frame(master)
        self.out.pack(anchor=S, expand=True, fill=BOTH)

        # Frame for all the boxes
        self.optsFrame = Frame(self.options_)
        self.optsFrame.pack(side=TOP, anchor=N)

        # Add a pane for the chanel select radio buttons
        self.chanelLabel = LabelFrame(master, text="Channel Select")
        self.chanelLabel.pack(in_=self.optsFrame, side=LEFT)

        # Add a pane for the manual identification radio buttons
        self.userVerLabel = LabelFrame(master, text="Manual Identification")
        self.userVerLabel.pack(in_=self.main_)

        # Initialize window details - name and size
        master.title("IdentiCyte")
        master.geometry("785x500")

########Analysis Tab##########################################################
        # Create library selection
        self.anLibFrame = ttk.Frame(master)
        self.anLibFrame.pack(in_=self.top, side=TOP)
        # Label to tell the user what this field does
        self.anLabel = Label(master, text="Library Folder: ")
        self.anLabel.pack(in_=self.anLibFrame, side=LEFT)

        # Entry box to type in
        self.anLibBox = Entry(master, width=80)
        self.anLibBox.pack(in_=self.anLibFrame, side=LEFT)
        self.anLibBox["textvariable"] = self.lib

        # Brings up a window to select the input folder
        self.anchoose_lib_btn = Button(master, text="...", command=lambda: self.chooseLibDir(self.lib))
        self.anchoose_lib_btn.pack(in_=self.anLibFrame, side=RIGHT)
        #####################################################

        # Create input selection
        self.inFrame = ttk.Frame(master)
        self.inFrame.pack(in_=self.top, side=TOP)
            # Label to tell the user what this field does
        self.anlabel = Label(master, text="  Input Folder: ")
        self.anlabel.pack(in_=self.inFrame, side=LEFT)

            # Entry box to type in
        self.aninBox = Entry(master, width=80)
        self.aninBox.pack(in_=self.inFrame, side=LEFT)
        self.aninBox["textvariable"] = self.infile

            # Brings up a window to select the input folder
        self.anchoose_btn = Button(master, text="...", command=lambda: self.chooseDir(self.infile))
        self.anchoose_btn.pack(in_=self.inFrame, side=RIGHT)
        #######################################################

        # User Verification radio buttons
        self.userEVer = Radiobutton(self.userVerLabel, text="Enable", variable=self.userVer, value=True)
        self.userDVer = Radiobutton(self.userVerLabel, text="Disable", variable=self.userVer, value=False)
        self.userDVer.pack(side=TOP)
        self.userEVer.pack(side=TOP)

        # Run Recognition
        self.recognise = Button(master, text="Identify Cells", command=lambda: self.runRecognition())
        self.recognise.pack(in_=self.bot, side=TOP)
        # # Run Batch Recognition
        # self.batch_recognise = Button(master, text="Batch Identify", command=lambda: self.runBatch())
        # self.batch_recognise.pack(in_=self.bot, side=TOP)
########Review Tab##################################################################################

        # Create input selection
        self.revInFrame = ttk.Frame(master)
        self.revInFrame.pack(in_=self.check_, side=TOP)

        # Label to tell the user what this field does
        self.revInLabel = Label(master, text="  Input Image: ")
        self.revInLabel.pack(in_=self.revInFrame, side=LEFT)

        # Entry box to type in
        self.revInBox = Entry(master, width=80)
        self.revInBox.pack(in_=self.revInFrame, side=LEFT)
        self.revInBox["textvariable"] = self.img

        # Brings up a window to select the input folder
        self.revChoose_btn = Button(master, text="...", command=lambda: self.chooseImg(self.img))
        self.revChoose_btn.pack(in_=self.revInFrame, side=RIGHT)
        #####################################################

        self.dispBtn = Button(master, text="Review", command=lambda: self.check())
        self.dispBtn.pack(in_=self.check_, side=BOTTOM, anchor=S)
########Library Tab##################################################################################

        # Create input selection
        self.libInFrame = ttk.Frame(master)
        self.libInFrame.pack(in_=self.library_, side=TOP)
        # Label to tell the user what this field does
        self.libInLabel = Label(master, text="  Input Folder: ")
        self.libInLabel.pack(in_=self.libInFrame, side=LEFT)

        # Entry box to type in
        self.libInBox = Entry(master, width=80)
        self.libInBox.pack(in_=self.libInFrame, side=LEFT)
        self.libInBox["textvariable"] = self.infile

        # Brings up a window to select the input folder
        self.libChoose_btn = Button(master, text="...", command=lambda: self.chooseDir(self.infile))
        self.libChoose_btn.pack(in_=self.libInFrame, side=RIGHT)
        ########################################################
        # Trigger cell extraction
        self.show_exCells = Button(master, text="Extract Cells", command=lambda: self.exCells())
        self.show_exCells.pack(in_=self.library_, side=TOP)
        ########################################################

        # Create library selection
        self.libSelFrame = ttk.Frame(master)
        self.libSelFrame.pack(in_=self.library_, side=TOP)
        # Label to tell the user what this field does
        self.libLibLabel = Label(master, text="Library Folder: ")
        self.libLibLabel.pack(in_=self.libSelFrame, side=LEFT)

        # Entry box to type in
        self.libLibBox = Entry(master, width=80)
        self.libLibBox.pack(in_=self.libSelFrame, side=LEFT)
        self.libLibBox["textvariable"] = self.lib

        # Brings up a window to select the input folder
        self.libChoose_lib_btn = Button(master, text="...", command=lambda: self.chooseLibDir(self.lib))
        self.libChoose_lib_btn.pack(in_=self.libSelFrame, side=RIGHT)
        #################################################################

        # Trigger Library Compilation
        self.compile_btn = Button(master, text="Compile Library", command=lambda: self.compileLibrary())
        self.compile_btn.pack(in_=self.library_, side=TOP)
###########Options Tab##################################################################
        # Near Images Frame
        self.nearFrame = Frame(master)
        self.nearFrame.pack(in_=self.options_, side=BOTTOM)
        vcmd2 = (master.register(self.validateSize), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        # Near Images Threshold
        self.nearLabel = Label(master, text='Number of most similar images to consider: ')
        self.nearPercent = Label(master, text=' images')
        self.nearBox = Entry(master, validate='key', validatecommand=vcmd2, width=4)

        self.nearLabel.pack(in_=self.nearFrame, side=LEFT)
        self.nearPercent.pack(in_=self.nearFrame, side=RIGHT)
        self.nearBox.pack(in_=self.nearFrame, side=BOTTOM)
        self.nearBox["textvariable"] = self.near

        # Principal Components Frame
        self.pcFrame = Frame(master)
        self.pcFrame.pack(in_=self.options_, side=BOTTOM)
        vcmd = (master.register(self.validatePerc), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        # Confidences Threshold
        self.pcLabel = Label(master, text='Percent of Principal Components to take: ')
        self.pcPercent = Label(master, text='%')
        self.pcBox = Entry(master, validate='key', validatecommand=vcmd, width=4)

        self.pcLabel.pack(in_=self.pcFrame, side=LEFT)
        self.pcPercent.pack(in_=self.pcFrame, side=RIGHT)
        self.pcBox.pack(in_=self.pcFrame, side=BOTTOM)
        self.pcBox["textvariable"] = self.pcThresh

        # Confidences Frame
        self.confFrame = Frame(master)
        self.confFrame.pack(in_=self.options_, side=BOTTOM)

        # Confidences Threshold
        self.confLabel = Label(master, text='Confidence for definite identification: ')
        self.confPercent = Label(master, text='%')
        self.confBox = Entry(master, validate='key', validatecommand=vcmd, width=4)

        self.confLabel.pack(in_=self.confFrame, side=LEFT)
        self.confPercent.pack(in_=self.confFrame, side=RIGHT)
        self.confBox.pack(in_=self.confFrame, side=BOTTOM)
        self.confBox["textvariable"] = self.confThresh

        # Cell Size Frame
        self.sizeFrame = Frame(master)
        self.sizeFrame.pack(in_=self.options_, side=BOTTOM)

        vcmd2 = (master.register(self.validateSize), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        # Cell Size
        self.sizeLabel = Label(master, text='Minimum Cell Area: ')
        self.sizePercent = Label(master, text=' pixels')
        self.sizeBox = Entry(master, validate='key', validatecommand=vcmd2, width=8)

        self.sizeLabel.pack(in_=self.sizeFrame, side=LEFT)
        self.sizePercent.pack(in_=self.sizeFrame, side=RIGHT)
        self.sizeBox.pack(in_=self.sizeFrame, side=BOTTOM)
        self.sizeBox["textvariable"] = self.cellSize

        # Cell Radius Frame
        self.radiusFrame = Frame(master)
        self.radiusFrame.pack(in_=self.options_, side=BOTTOM)

        vcmd2 = (master.register(self.validateSize), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        # Cell Size
        self.radiusLabel = Label(master, text='Cell Radius: ')
        self.radiusPercent = Label(master, text=' pixels')
        self.radiusBox = Entry(master, validate='key', validatecommand=vcmd2, width=5)

        self.radiusLabel.pack(in_=self.radiusFrame, side=LEFT)
        self.radiusPercent.pack(in_=self.radiusFrame, side=RIGHT)
        self.radiusBox.pack(in_=self.radiusFrame, side=BOTTOM)
        self.radiusBox["textvariable"] = self.cellRadius

        # Color selecting radio buttons
        self.colorR = Radiobutton(self.chanelLabel, text="Red", variable=self.color, value='R')
        self.colorG = Radiobutton(self.chanelLabel, text="Green", variable=self.color, value='G')
        self.colorB = Radiobutton(self.chanelLabel, text="Blue", variable=self.color, value='B')
        self.colorR.pack(side=TOP)
        self.colorG.pack(side=TOP)
        self.colorB.pack(side=TOP)

        # Method selecting frame
        self.methLabel = LabelFrame(self.options_, text='Thresholding Method')
        self.methLabel.pack(in_=self.optsFrame, side=RIGHT)
        # Method selecting radio buttons
        self.methO = Radiobutton(self.methLabel, text="Otsu", variable=self.method, value='Otsu')
        self.methT = Radiobutton(self.methLabel, text="Triangle", variable=self.method, value='Triangle')

        self.methO.pack(side=TOP)
        self.methT.pack(side=TOP)

        # Illumination Selecting Frame
        self.illumLabel = LabelFrame(self.options_, text='Illumination Method')
        self.illumLabel.pack(in_=self.optsFrame, side=RIGHT)
        # Method selecting radio buttons
        self.illumBF = Radiobutton(self.illumLabel, text="Brightfield", variable=self.brigthfield, value=True)
        self.illumFl = Radiobutton(self.illumLabel, text="Fluorescence", variable=self.brigthfield, value=False)

        self.illumBF.pack(side=TOP)
        self.illumFl.pack(side=TOP)

        # Batch Selecting Frame
        self.batchLabel = LabelFrame(self.options_, text='Recursive Batch')
        self.batchLabel.pack(in_=self.optsFrame, side=RIGHT)
        # Method selecting radio buttons
        self.batchY = Radiobutton(self.batchLabel, text="Yes", variable=self.batch, value=True)
        self.batchN = Radiobutton(self.batchLabel, text="No", variable=self.batch, value=False)

        self.batchY.pack(side=TOP)
        self.batchN.pack(side=TOP)

        # Dropdown Menu
        self.bitFrame = Frame(master)
        self.bitFrame.pack(in_=self.options_, side=BOTTOM)
        self.bitLabel = Label(self.bitFrame, text="Bit Depth: ")
        self.bitLabel.pack(in_=self.bitFrame, side=LEFT)
        self.types = OptionMenu(master, self.bits, 1, 2, 3, 4, 5, 6, 7, 8)
        self.types.pack(in_=self.bitFrame, side=RIGHT)
########Not in a tab#############################################################################

        # Cancel button
        self.cancel_button = Button(master, text="Cancel", command=lambda: self.cancel())
        self.cancel_button.pack(in_=self.out, side=RIGHT, anchor=SE)

        # Create output box
        self.boxFrame = Frame(master)
        self.boxFrame.pack(in_=self.out, anchor=S, expand=True, fill=BOTH)
        self.scroll = Scrollbar(self.master)
        self.scroll.pack(in_=self.boxFrame, side=RIGHT, fill=Y)
        self.outbox = Text(master, state=DISABLED, yscrollcommand=self.scroll.set, height=14)
        self.outbox.pack(in_=self.boxFrame, anchor=S, expand=True, fill=BOTH)
        self.scroll.config(command=self.outbox.yview)
########End Window##############################################################################
        self.printout("Welcome to IdentiCyte version " + self.version)
    # Choose the input
    def chooseDir(self, var):
        # type: (StringVar) -> None
        """
        Brings up a window select for a directory
        Parameters
        ----------
        var : StringVar
            A string variable containing a directory path.

        Returns
        -------
        Modifies var
        """
        prevdir = var.get()
        var.set(
            filedialog.askdirectory(initialdir=os.path.dirname(os.path.abspath(self.infile.get())),
                                    title='Select the Folder with Images to be Analysed',
                                    mustexist=False))
        if var.get() == '':
            var.set(prevdir)
        var.set(os.path.abspath(var.get()))

    def chooseImg(self, var):
        # type: (StringVar) -> None
        """
        Brings up a window select for an image
        Parameters
        ----------
        var : StringVar
            A string variable containing a directory path to the image.

        Returns
        -------
        Modifies var
        """
        previmg = var.get()
        var.set(
            filedialog.askopenfilename(initialdir=self.infile.get(),
                                       title='Select an Analysed Image',
                                       filetypes=(("Supported images", "*.jpg *.jpeg *.png *.tif *.tiff"),
                                                  ("JPEG images", "*.jpg *.jpeg"),
                                                  ("PNG images", "*.png"),
                                                  ("TIFF images", "*.tif *.tiff"))))
        if var.get() == '':
            var.set(previmg)
        var.set(os.path.abspath(var.get()))

    def chooseLibDir(self, var):
        # type: (StringVar) -> None
        """
        Brings up a window select for a library directory
        Parameters
        ----------
        var : StringVar
            A string variable containing a directory path.

        Returns
        -------
        Modifies var
        """
        prevdir = var.get()
        var.set(filedialog.askdirectory(initialdir=os.path.dirname(os.path.abspath(self.lib.get())),
                                        title='Select Library Folder', mustexist=False))
        if var.get() == '':
            var.set(prevdir)
        var.set(os.path.abspath(var.get()))

    # Extract the Cells from images
    def exCells(self):
        # type: () -> None
        """
        Extracts the cells from an image to be used as examples in the library.
        """
        Globs.end = False
        pic_dir = self.infile.get()
        lib_dir = self.lib.get()
        if not os.path.exists(pic_dir):
            Globs.end = True
            self.printout('Please select an input folder.')
        if not os.path.exists(lib_dir):
            Globs.end = True
            self.printout('Please select a library folder.')
        try:
            if (not self.thread.isAlive()) and (not Globs.end):
                self.printout('Extracting Cells')
                self.thread = Thread(target=EC.ExCells,
                                     args=(pic_dir,
                                           lib_dir,
                                           self,
                                           self.bits.get(),
                                           self.color.get(),
                                           self.method.get(),
                                           self.cellSize.get(),
                                           self.brigthfield.get(),
                                           self.cellRadius.get()))
                self.thread.start()
        except:
            self.printout(traceback.format_exc())

    def runRecognition(self):
        # type: () -> None
        """
        Runs the analysis on a specified folder
        """
        Globs.end = False
        Globs.batchEnd = False
        if (not self.thread.isAlive()) and (not Globs.end):
            lib_dir = self.lib.get()
            pcs = self.pcThresh.get()
            confLev = self.confThresh.get()
            pic_dir = self.infile.get()
            verification = self.userVer.get()
            depth = self.bits.get()
            col = self.color.get()
            meth=self.method.get()
            cellSize=self.cellSize.get()
            bf = self.brigthfield.get()
            near = self.near.get()
            if not os.path.exists(pic_dir):
                Globs.end = True
                self.printout('Please select an input folder.')
            if not os.path.exists(lib_dir):
                Globs.end = True
                self.printout('Please select a library folder.')
            if not Globs.end:
                self.printout('Getting Pictures from: ' + str(self.infile.get()))
                if self.batch.get():
                    self.thread = Thread(target=batch,
                                         args=(lib_dir,
                                               pic_dir,
                                               self,
                                               verification,
                                               depth,
                                               col,
                                               meth,
                                               cellSize,
                                               pcs,
                                               confLev,
                                               bf,
                                               near))
                else:
                    self.thread = Thread(target=driver,
                                         args=(lib_dir,
                                               pic_dir,
                                               self,
                                               verification,
                                               depth,
                                               col,
                                               meth,
                                               cellSize,
                                               pcs,
                                               confLev,
                                               bf,
                                               near))
                self.thread.start()
        else:
            self.printout('The program is currently busy.')

    # def runBatch(self):
    #     # type: () -> None
    #     """
    #     Runs the analysis on a specified folder
    #     """
    #     Globs.end = False
    #     Globs.batchEnd = False
    #     if (not self.thread.isAlive()) and (not Globs.end):
    #         lib_dir = self.lib.get()
    #         pcs = self.pcThresh.get()
    #         confLev = self.confThresh.get()
    #         pic_dir = self.infile.get()
    #         verification = self.userVer.get()
    #         depth = self.bits.get()
    #         col = self.color.get()
    #         meth=self.method.get()
    #         cellSize=self.cellSize.get()
    #         bf = self.brigthfield.get()
    #         near = self.near.get()
    #         if not os.path.exists(pic_dir):
    #             Globs.end = True
    #             self.printout('Please select an input folder.')
    #         if not os.path.exists(lib_dir):
    #             Globs.end = True
    #             self.printout('Please select a library folder.')
    #         if not Globs.end:
    #             self.printout('Getting Pictures from: ' + str(self.infile.get()))
    #             self.thread = Thread(target=batch,
    #                                  args=(lib_dir,
    #                                        pic_dir,
    #                                        self,
    #                                        verification,
    #                                        depth,
    #                                        col,
    #                                        meth,
    #                                        cellSize,
    #                                        pcs,
    #                                        confLev,
    #                                        bf,
    #                                        near))
    #             self.thread.start()
    #     else:
    #         self.printout('The program is currently busy.')

    # Displays text in the window's output box
    def printout(self, string):
        # type: () -> None
        """
        Prints a string to the text box in the main window.
        Parameters
        ----------
        string : str
            A string to be printed

        Returns
        -------
        Prints to the textbox
        """
        self.outbox.config(state=NORMAL)
        self.outbox.insert('end', string + '\n')
        self.outbox.see('end')
        self.outbox.update()
        self.outbox.config(state=DISABLED)

    def compileLibrary(self):
        # type: () -> None
        """
        Compiles the library file from the images in the library directory.
        """
        Globs.end = False
        lib_dir = self.lib.get()
        if not os.path.exists(lib_dir):
            Globs.end = True
            self.printout('Please select a library folder.')
        try:
            if not Globs.end:
                self.printout('Loading Library From: ' + self.lib.get())
                compileLibrary(lib_dir, self)
                self.printout('Done')
        except:
            self.printout(traceback.format_exc())

    # Ensure entries into percentage fields are valid
    def validatePerc(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        # type: (...) -> None
        """
        Validate a percentage in an input box.

        As in the tkinter man page.

        Parameters
        ----------
        action : str
            Type of action to be undertaken. 0 for delete, 1 for insert, or -1 for focus
        index : str
            index of the char string to be inserted, if any. Otherwise it is -1
        value_if_allowed : str
            The value of the entry if the edit is allowed.
        prior_value : str
            The value of entry prior to editing
        text : str
            The text stringbeing inserted or deleted, if any
        validation_type : str
            The type of validation currently set
        trigger_type : str
            The type of validation that triggered the callback
        widget_name : str
            The name of the entry widget.
        Returns
        -------
        Boolean
        """
        if action == '1':
            if text in '0123456789.':
                try:
                    num = float(value_if_allowed)
                    if ((num > 0) and (num <= 100)):
                        return True
                    else:
                        return False
                except:
                    return False
            else:
                return False
        else:
            return True

    # Ensure entries in numerical fields are valid
    def validateSize(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
        # type: (...) -> None
        """
        Validate an integer in an input box.

        As in the tkinter man page.

        Parameters
        ----------
        action : str
            Type of action to be undertaken. 0 for delete, 1 for insert, or -1 for focus
        index : str
            index of the char string to be inserted, if any. Otherwise it is -1
        value_if_allowed : str
            The value of the entry if the edit is allowed.
        prior_value : str
            The value of entry prior to editing
        text : str
            The text stringbeing inserted or deleted, if any
        validation_type : str
            The type of validation currently set
        trigger_type : str
            The type of validation that triggered the callback
        widget_name : str
            The name of the entry widget.
        Returns
        -------
        Boolean
        """
        if action == '1':
            if text in '0123456789':
                try:
                    num = int(value_if_allowed)
                    if num > 0:
                        return True
                    else:
                        return False
                except:
                    return False
            else:
                return False
        else:
            return True

    def cancel(self):
        # type: (...) -> None
        """
        Terminate execution as soon as possible.
        """
        Globs.end = True
        Globs.batchEnd = True

    # Review Classified Cells
    def check(self):
        # type: () -> None
        """
        Brings up the review window to check a batch of analyzed images.
        """
        Globs.end = False
        pic_dir = self.img.get()
        if not os.path.exists(pic_dir):
            Globs.end = True
            self.printout('Please select an input image.')
        if not self.dispThread.isAlive() and not Globs.end:
            self.dispThread = Thread(target=display,
                                     args=(pic_dir,
                                           self))
            self.dispThread.start()