"""
   File Name: ExtractCells.py
   Version: 1.0
   Author: Guillaume Garnier
   Date Modified: 2018-12-13
   License: GNU-GPL-3.0-or-later
   Python Version 3.5
   Description: Extracts the cells to build a library
"""
import os
import numpy as np
from IdentiCyte.ToGreyScale import greyalize
import cv2
from IdentiCyte.CellDetection import detect
import IdentiCyte.Globs as Globs
import re


# Takes cells out of images for building the library
def ExCells(im_dir,  # type: str
            lib_dir,  # type: str
            window=None,   # type: Opional(MainWindow)
            bits=3,   # type: Opional(int)
            color='B',  # type: Opional(str)
            method='Otsu',  # type: Opional(str)
            minSize=9000,  # type: Opional(int)
            bf=True,  # type: Opional(bool)
            radius=155  # type: Opional(int)
            ):
    # type: (...) -> None
    """
    Extracts cells from images in a folder for use in the library.

    Detects cells in an image and cuts out square sections from each image with side length radius*2 + 1. These are
    output into lib_dir, where they should be sorted by hand into folders of appropriate categories.

    Parameters
    ----------
    im_dir : str
        A string of the directory path to the images to be analysed
    lib_dir : str
        A string of the directory path to the library
    window : MainWindow
        The main GUI window
    bits : int
        The bit depth of the cells when analysing. there will be  2^depth levels of grey in the result. Valid values are
        between 1 and 8 inclusive.
    color : str
        The colour channel that will be inspected, ignored if analyzing grey scale images
    method : str
        The algorithm used to threshold the image into binary when detecting cells. Either 'Otsu' or 'Triangle'.
    minSize : int
        The minimum number of pixels in a blob for it to be considered a cell and not small debris.
    bf : bool
        Indicates whether the image is bright field(True) or fluorescent(False)
    radius: int
        Defines the size of the section of image cut out for each cell. The section will be radius pixels out from the
        centroid as found in detect() in both the positive x and y directions in the image.

    Returns
    -------
    Creates many tif images with a single cell in each.
   """
    if not os.path.exists(lib_dir):
        os.mkdir(lib_dir)

    # Define constant
    imageNum = 1

    # Iterate through only images
    for file in os.listdir(im_dir):
        exp = re.compile("\.png$|\.tif$|\.jpg$|\.jpeg$|\.tiff$", re.I)
        an_image = bool(exp.search(file))
        if an_image:
            if window:
                window.printout(file)

            # Import the image and define its edges
            im_path = os.path.join(im_dir, file)
            image = cv2.imread(im_path)
            image = np.array(image)
            if len(np.shape(image)) == 3:
                bounds = np.shape(image[:, :, 0])
            else:
                bounds = np.shape(image)

            imInfo = detect(image, channel=color, method=method, minSize=minSize, bf=bf)
            cellLocs = imInfo

            # Extract and save the cells in greyscale
            cell = 1
            for pos in cellLocs:
                pos[0] = int(pos[0])
                pos[1] = int(pos[1])
                # Check if the cell is too close to the edge
                inBounds = ((pos[0]-radius) > 0 and
                            (pos[1]-radius) > 0 and
                            (pos[0]+radius+1) < bounds[0] and
                            (pos[1]+radius+1) < bounds[1])
                if inBounds:
                    extCell = image[(pos[0]-radius):(pos[0]+radius+1), (pos[1]-radius):(pos[1]+radius+1), :]
                    extCell = greyalize(extCell, bits, color)
                    name = os.path.join(lib_dir, str(imageNum)+'_'+str(cell) + '.tif')
                    cv2.imwrite(name, extCell)

                # Increment the counts so that each cell has a unique filename
                cell += 1
            imageNum += 1
        if Globs.end:
            window.printout('Cell Extraction Cancelled')
            break
    if window:
        window.printout("Done")

