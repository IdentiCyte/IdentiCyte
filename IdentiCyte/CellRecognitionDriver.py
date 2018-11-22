"""
   File Name: CellRecognitionDriver.py
   Version: 1.0
   Author: Guillaume Garnier
   Date Modified: 2018-11-22
   License: GNU-GPL-3.0-or-later
   Python Version 3.5
   Description: Calls all the individual elements of the analysis
"""
from IdentiCyte.ProcessFiles import ProcessFiles
from IdentiCyte.CellStatistics import CellStats
from IdentiCyte.WriteResult import WriteResults
import IdentiCyte.Globs as Globs
import xlsxwriter
import numpy as np
import os
import timeit

def driver(l_dir,
           pics_dir,
           window=None,
           userver=False,
           bits=3,
           color='B',
           method='Triangle',
           cellSize=9000,
           pcThresh=90,
           confThresh=50,
           bf=True):
    """
    Drives the analysis

    This detects the cell categories in the library and runs both the analysis ant the output file writing.

    Parameters
    ----------
    l_dir : str
        A string of the directory path to the library
    pics_dir : str
        A string of the directory path to the images to be analysed
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
   """
    start = timeit.default_timer()

    file_name = os.path.join(pics_dir, os.path.split(pics_dir)[-1] + '.xlsx')

    # Check to see if the book can be opened
    try:
        workbook = xlsxwriter.Workbook(file_name)
        workbook.close()
    except:
        window.printout('There was an error. Please close any open Excel documents and try again.')
        Globs.end = True
    if not Globs.end:
        if window:
            window.printout('Starting Identification')
        else:
            print('Starting Identification')
        typeArray = []

        for item in os.listdir(l_dir):
            if os.path.isdir(os.path.join(l_dir, item)):
                typeArray.append(item)

        types, confidences, locations = ProcessFiles(l_dir=l_dir,
                                                     pics_dir=pics_dir,
                                                     typeArray=typeArray,
                                                     window=window,
                                                     userVer=userver,
                                                     bits=bits,
                                                     color=color,
                                                     method=method,
                                                     minSize=cellSize,
                                                     pcThresh=pcThresh,
                                                     confThresh=confThresh,
                                                     bf=bf)

        if not Globs.end:
            if 'Other' not in typeArray:
                typeArray.append('Other')
            else:
                othInd = typeArray.index('Other')
                inds = list(range(len(typeArray)))
                inds.pop(othInd)
                inds.append(othInd)
                typeArray = np.array(typeArray)[inds].tolist()
            typeArray.append('Edge')
            cellCount = CellStats(types, typeArray)

            if window and (not Globs.end):
                window.printout('Recognition Complete')
                window.printout('Outputting to Excel')
            elif (not window) and (not Globs.end):
                print('Recognition Complete')
                print('Outputting to Excel')
            if len(cellCount) > 0 and not Globs.end:
                WriteResults(cellCount,
                             typeArray,
                             locations,
                             pics_dir,
                             l_dir,
                             types,
                             confidences,
                             pcThresh,
                             confThresh,
                             userver,
                             bits,
                             color,
                             method,
                             cellSize,
                             bf)
            else:
                window.printout('There were no images in the Input Folder.')

        if window and (not Globs.end):
            window.printout('Done.')
        elif not window and (not Globs.end):
            print('Done.')
        elif window:
            window.printout('Identification Cancelled')
        else:
            print('Identification Cancelled')


    # This needs to be here. If it's not, the program uses unbounded memory.
    stop = timeit.default_timer()
    if not Globs.end:
        time = "Analysis completed in %.0lf seconds." % (stop - start)
        Globs.end = True
    else:
        time = "Analysis stopped after %.0lf seconds." % (stop - start)

    print(time)


