"""
   File Name: DisplayIdentified.py
   Author: Guillaume Garnier
   Date Modified: 2019-02-08
   License: GNU-GPL-3.0-or-later
   Python Version 3.5
   Description: Displays the analysed images overlayed with cell classifications
"""
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np
import cv2
import pickle
import IdentiCyte.Globs as Globs
import sys


def display(img_file,  # type: str
            window=None  # type: Optional(MainWindow)
            ):
    # type: (str, Optional(MainWindow)) -> None
    """
    Displays images with classified cells.

    Displays images which have been analysed with colour coded tages overlayed on the cells

    Parameters
    ----------
    img_file : str
        The path to the first image to be reviewed. The image must be in the same directory as the pkl file that was
        generated when the analysis was run for the dataset.
    window : MainWindow
        The main GUI window
    """
    windName = 'Press Right Arrow Key to display next image, Left Arrow Key for previous, \'s\' to save and \'Esc\' to quit'
    fontSize = 36
    boxHeight = 50
    colInd = 0
    colors = [(255, 0, 0, 127),
              (0, 255, 0, 127),
              (0, 0, 255, 127),
              (255, 255, 0, 127),
              (255, 0, 255, 127),
              (0, 255, 255, 127),
              (255, 255, 255, 127),
              (127, 0, 127, 127),
              (127, 127, 0, 127),
              (0, 127, 127, 127),
              (255, 127, 0, 127),
              (255, 0, 127, 127),
              (127, 255, 0, 127),
              (0, 255, 127, 127),
              (127, 0, 255, 127),
              (0, 127, 255, 127),
              (255, 167, 26, 127),
              (127, 0, 0, 127),
              (0, 127, 0, 127),
              (0, 0, 127, 127)]

    pics_dir = os.path.split(img_file)[0]
    image_name = os.path.split(img_file)[-1]
    fontName = 'LiberationSans-Regular.ttf'
    fontName = resource_path(fontName)

    # Get the cell data
    res_file = os.path.abspath(os.path.join(pics_dir, 'IdentifiedCellInfo.pkl'))

    with open(res_file, 'rb') as f:
        results = pickle.load(f)

    typeArray = results.pop()

    colorDict = {}

    for category in typeArray:
        colorDict[category] = colors[colInd]
        colInd = (colInd + 1) % len(colors)
    if 'Other' not in colorDict:
        colorDict['Other'] = colors[colInd]
        colInd = (colInd + 1) % len(colors)
    if 'Edge' not in colorDict:
        colorDict['Edge'] = colors[colInd]
        colInd = (colInd + 1) % len(colors)

    font = ImageFont.truetype(font=fontName, size=fontSize)
    img_names = os.listdir(pics_dir)
    # Remove all non image files
    for entry in range(len(img_names)-1, -1, -1):
        an_image = img_names[entry].endswith('.tif') or img_names[entry].endswith('.png') or \
                   img_names[entry].endswith('.jpg') or img_names[entry].endswith('.jpeg')
        if os.path.isdir(os.path.join(pics_dir, img_names[entry])) or not an_image:
            img_names.pop(entry)

    imNum = img_names.index(image_name)


    while -1 < imNum < len(img_names) and not Globs.end:

        image = Image.open(os.path.join(pics_dir, img_names[imNum]))
        if len(np.shape(image)) == 2:
            image = np.asarray(image)
            a, b = np.shape(image)
            image = np.repeat(image, 3, 1)
            image = np.reshape(image, [a, b, 3])
            image = Image.fromarray(image)
        draw = ImageDraw.Draw(image, 'RGBA')

        cellTypes = results[imNum]
        for cell in range(len(results[imNum])):
            loc = cellTypes[cell][2]
            if len(cellTypes[cell][0]) < 8:
                cellLabel = cellTypes[cell][0] + '  ' + cellTypes[cell][1]
            else:
                cellLabel = cellTypes[cell][0][0:8] + '  ' + cellTypes[cell][1]
            boxWidth = 19*len(cellLabel)
            draw.rectangle(((loc[1], loc[0]), (loc[1]+boxWidth, loc[0]+boxHeight)), fill=colorDict[cellTypes[cell][0]])
            draw.text((loc[1], loc[0]), cellLabel, (0, 0, 0), font=font)

        cv2.namedWindow(windName, cv2.WINDOW_NORMAL)
        im = np.asarray(image)
        cv2.imshow(windName, im[:, :, (2, 1, 0)])

        factor = gcd(np.shape(im)[1], np.shape(im)[0])
        if np.shape(im)[0]//factor < 720:
            mul = 720 / (np.shape(im)[0]//factor)
        else:
            mul = 1
        height = int(np.round(mul*np.shape(im)[0]//factor, 0))
        width = int(np.round(mul * np.shape(im)[1] // factor, 0))
        cv2.resizeWindow(windName, width, height)
        key = cv2.waitKeyEx(0)
        if key == 27 or cv2.getWindowProperty(windName, 0) == -1:
            break
        elif key == 2424832 or key == 2490368 or key == 44:
            imNum = imNum - 1
        elif key == 115:
            if not os.path.exists(os.path.join(pics_dir, 'Labelled')):
                os.mkdir(os.path.join(pics_dir, 'Labelled'))
            cv2.imwrite(os.path.join(pics_dir, 'Labelled', img_names[imNum]), im[:, :, (2, 1, 0)])
            if window:
                window.printout('Saved ' + str(img_names[imNum]) + ' to ' + os.path.join(pics_dir, 'Labelled', img_names[imNum]))
            else:
                print('Saved ' + str(img_names[imNum]) + ' to ' + os.path.join(pics_dir, 'Labelled', img_names[imNum]))
        else:
            imNum = imNum + 1
    cv2.destroyWindow(windName)


def gcd(x, # type: int
        y  # type: int
        ):
    # type: (int) -> int
    """
    Calcualtes the gcd of 2 numbers.

    Parameters
    ----------
    x : int
    y : int

    Returns
    -------
    gcd : int
        The greatest common divisor of the two parameters
    """
    if y > x:
        tmp = x
        x = y
        y = tmp
    while(y):
        x,y = y, x%y
    return x

def resource_path(font):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, font)

    return os.path.join(os.path.dirname(__file__), 'liberation-fonts-ttf-2.00.1', font)
