"""
   File Name: CellRecognitionDriver.py
   Version: 1.0
   Author: Guillaume Garnier
   Date Modified: 2019-01-31
   License: GNU-GPL-3.0-or-later
   Python Version 3.5
   Description: Recursively performs analysis on folders and subfolders
"""
import os
import IdentiCyte.Globs as Globs
from IdentiCyte.CellRecognitionDriver import driver


def batch(l_dir,  # type: str
           pics_dirs,  # type: str
           window=None,  # type: Opional(MainWindow)
           userver=False,  # type: Opional(bool)
           bits=3,  # type: Opional(int)
           color='B',  # type: Opional(str)
           method='Triangle',  # type: Opional(str)
           cellSize=9000,  # type: Opional(int)
           pcThresh=90,  # type: Opional(float)
           confThresh=50,  # type: Opional(float)
           bf=True,  # type: Opional(bool)
           near=10,  # type: Opional(int)
           depth=0  # type: Optional(int)
           ):
    # type: (...) -> None
    """
    Drives the analysis

    This detects the cell categories in the library and runs both the analysis ant the output file writing.

    Parameters
    ----------
    l_dir : str
        A string of the directory path to the library
    pics_dirs : str
        A string of the directory path to the folders containing the images to be analysed
    window : MainWindow
        The main GUI window
    userver : bool
        Enables(True) or disables(False) the user verification popup window.
    bits : int
        The bit depth of the cells when analysing. there will be  2^depth levels of grey in the result. Valid values are
        between 1 and 8 inclusive.
    color : str
        The colour channel that will be inspected, ignored if analyzing grey scale images
    method : str
        The algorithm used to threshold the image into binary when detecting cells. Either 'Otsu' or 'Triangle'.
    cellSize : int
        The minimum number of pixels in a blob for it to be considered a cell and not small debris.
    pcThresh : float
        A percentage value of which proportion of principal components are used to compare a cell to the library. Valid
        values are between 0 and 100 inclusive.
    confThresh : float
        The confidence level a cell must have for it to be automatically classified. This is a percentage nd should be
        between 0 and 100 inclusive.
    bf : bool
        Indicates whether the image is bright field(True) or fluorescent(False)
    near : int
        The number of nearest neighbours in the library that will be considered when classifying a cell
    depth : int
    The current recursion depth
   """

    max_depth = 5
    driver(l_dir,  # type: str
           pics_dirs,  # type: str
           window=window,  # type: Opional(MainWindow)
           userver=userver,  # type: Opional(bool)
           bits=bits,  # type: Opional(int)
           color=color,  # type: Opional(str)
           method=method,  # type: Opional(str)
           cellSize=cellSize,  # type: Opional(int)
           pcThresh=pcThresh,  # type: Opional(float)
           confThresh=confThresh,  # type: Opional(float)
           bf=bf,  # type: Opional(bool)
           near=near  # type: Opional(int)
           )
    for item in os.listdir(pics_dirs):
        if os.path.isdir(os.path.join(pics_dirs, item)) and not item == 'Labelled' and not Globs.batchEnd:

            if depth < max_depth:
                batch(l_dir,  # type: str
                      os.path.join(os.path.join(pics_dirs, item)),  # type: str
                      window=window,  # type: Opional(MainWindow)
                      userver=userver,  # type: Opional(bool)
                      bits=bits,  # type: Opional(int)
                      color=color,  # type: Opional(str)
                      method=method,  # type: Opional(str)
                      cellSize=cellSize,  # type: Opional(int)
                      pcThresh=pcThresh,  # type: Opional(float)
                      confThresh=confThresh,  # type: Opional(float)
                      bf=bf,  # type: Opional(bool)
                      near=near,  # type: Opional(int)
                      depth=depth+1)  # type: Optional(int)

            driver(l_dir,  # type: str
                   os.path.join(os.path.join(pics_dirs, item)),  # type: str
                   window=window,  # type: Opional(MainWindow)
                   userver=userver,  # type: Opional(bool)
                   bits=bits,  # type: Opional(int)
                   color=color,  # type: Opional(str)
                   method=method,  # type: Opional(str)
                   cellSize=cellSize,  # type: Opional(int)
                   pcThresh=pcThresh,  # type: Opional(float)
                   confThresh=confThresh,  # type: Opional(float)
                   bf=bf,  # type: Opional(bool)
                   near=near  # type: Opional(int)
                   )
