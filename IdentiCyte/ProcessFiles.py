"""
   File Name: ProcessFiles.py
   Version: 1.0
   Author: Guillaume Garnier
   Date Modified: 2019-01-07
   License: GNU-GPL-3.0-or-later
   Python Version 3.5
   Description: Collects the results from the detection and recognition of cells.
"""
import os
import numpy as np
from IdentiCyte.ToGreyScale import greyalize
from IdentiCyte.PCARecognition import PCARecognition
import IdentiCyte.Globs as Globs
from IdentiCyte.CellDetection import detect
import cv2
import pickle
import gc
import re

def ProcessFiles(l_dir,  # type: str
                 pics_dir,# type: str
                 typeArray,  # type: List[str]
                 window=None,  # type: Opional(MainWindow)
                 userVer=False,  # type: Opional(bool)
                 bits=3,  # type: Opional(int)
                 color='B',# type: Opional(str)
                 method='Triangle',# type: Opional(str)
                 minSize=9000,  # type: Opional(int)
                 pcThresh=90,  # type: Opional(float)
                 confThresh=50,  # type: Opional(float)
                 bf=True,  # type: Opional(bool)
                 near=10  # type: Opional(int)
                 ):
    # type: (...) -> (List[List[str]], List[List[float]], List[List[int]])
    """
    Reads in images and prepares them for analysis.

    All images in pics_dir are read in, the cells in them are detected and passed to PCARecognition to be recognised.

    Parameters
    ----------
    l_dir : str
        A string of the directory path to the library
    pics_dir : str
        A string of the directory path to the images to be analysed
    typeArray : list
        A list of strings, each of which represents a category
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
    minSize : int
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
        THe number of nearest neighbours in the library that will be considered when classifying a cell

    Returns
    -------
    cellTypes : list
        A list which contains a list of cell types for each analysed image. The cell types are represented as strings.
    cellConf : list
        A list of lists containing the confidence values for each cell in each image. The cells are listed in the same
        order as in cell types (ie the first element in the first list in cellTypes refers to the same cell as the first
        element in the first list of cellConf)
    locations : list
        A list of lists of pairs of co-ordinates. These co-ordinates refer to an approximate centroid for all the cells
        in the analyzes images. This has the same order as cellTypes and cellConf.
   """

    img_names = os.listdir(pics_dir)

    # Remove all non image filenames from the list
    for entry in range(len(img_names)-1, -1, -1):
        exp = re.compile("\.png$|\.tif$|\.jpg$|\.jpeg$|\.tiff$", re.I)
        an_image = bool(exp.search(img_names[entry]))
        if os.path.isdir(os.path.join(pics_dir, img_names[entry])) or not an_image:
            img_names.pop(entry)

    if not img_names:
        Globs.end = True
    imgNum = len(img_names)

    cellTypes = [[]]*imgNum
    cellConf = [[]]*imgNum

    # Import the library
    if window:
        window.printout('Loading Library')
    try:
        lib_file = os.path.join(l_dir, 'LibraryInfo.pkl')
        with open(lib_file, 'rb') as f:
            resDict = pickle.load(f)
    except:
        Globs.end = True

    if not Globs.end:
        pixels, _ = np.shape(resDict['eigenV'])
        if window and not Globs.end:
            window.printout('Library Loaded')
        elif window and Globs.end:
            window.printout('Library file not found.')

        # Determine the side length of the square which will be extracted to look at the cells
        radius = int((np.sqrt(pixels)-1)/2)

        locations = []

        # Identify the cells in every image
        for j in range(imgNum):
            gc.collect()
            if Globs.end:
                break
            # Get the dimensions of the image
            image = cv2.imread(os.path.join(pics_dir, img_names[j]))
            xMax, yMax, *_ = np.shape(image)

            if window:
                window.printout(str(j + 1) + '. ' + img_names[j])

            # Find the cells in the current image
            imInfo = detect(image,
                            channel=color,
                            method=method,
                            minSize=minSize,
                            bf=bf)

            # Create the matrix that will hold the cells
            cellData = np.zeros([len(imInfo), pixels])

            # Extract the cells from each image
            for k in range(len(imInfo)):
                if Globs.end:
                    break
                xPos = imInfo[k][0]
                yPos = imInfo[k][1]

                # Check if the cell is on the edge
                inBounds = ((xPos-radius) > 0 and (yPos-radius) > 0 and
                            (xPos+radius) < xMax and (yPos+radius) < yMax)
                if inBounds:
                    thisCell = image[int(xPos-radius):int(xPos+radius+1), int(yPos-radius):int(yPos+radius+1), :]

                    # Convert to greyscale by taking a  channel
                    thisCell = greyalize(thisCell, depth=bits, colour=color)

                    # Normalize
                    thisCell = thisCell/np.max(thisCell)

                    # Add to the matrix of cells, where each 'row' is a cell
                    thisCell = np.reshape(thisCell, [1, np.size(thisCell)])
                    cellData[k] = thisCell
            cellTypes[j], cellConf[j] = PCARecognition(cellData,
                                                       resDict,
                                                       userVer,
                                                       l_dir,
                                                       typeArray,
                                                       pcThresh,
                                                       confThresh,
                                                       near)
            locations.append(imInfo)
        return cellTypes, cellConf, locations
    else:
        if window:
            window.printout('The library has not been compiled. Either compile the library or select a folder with a '
                            'library that has been compiled.')
            Globs.end = True
            Globs.batchEnd = True
            return 0, 0, 0

