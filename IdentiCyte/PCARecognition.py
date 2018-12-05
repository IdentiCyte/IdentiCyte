"""
   File Name: PCARecognition.py
   Version: 1.0
   Author: Guillaume Garnier
   Date Modified: 2018-11-21
   License: GNU-GPL-3.0-or-later
   Python Version 3.5
   Description: Performs the recognition and identifies cells
"""
import numpy as np
from tkinter import *
from IdentiCyte.CellVerUI import CellVerUI
from datetime import datetime
import os
import IdentiCyte.Globs as Globs
import cv2
from typing import List


def findThresh(arr,  # type: array[float]
               level  # type: float
               ):
    # type: (array, float) -> int
    """
    Returns the first index in an array which is greater than a specified level.

    Parameters
    ----------
    arr : array
        An array of numbers
    level : float
        A threshold to which elements in arr will be compared

    Returns
    -------
    i : int
        The first index that contains an element greater than the level. -1 if all elements in the array are less than
        level
    """
    for i in range(len(arr)):
        if arr[i] >= level:
            return i
    return -1


def PCARecognition(inputData,  # type: ndarray
                   resDict,  # type: dict{str: array[float], str:ndarray, str:List[str], str:ndarray, str:ndarray}
                   userVer,  # type: bool
                   library_dir,  # type: str
                   typeArray,  # type: list[str]
                   pcThresh=90,  # type: Opional(float)
                   confThresh=50,  # type: Opional(float)
                   near=10  # type: Opional(int)
                   ):
    # type: (...) -> (List[str], ndarray)
    """
    Recognises cells

    The cells are passed in and compared against the library.

    Parameters
    ----------
    inputData : ndarray
        An array of arrays, one array for each cell in an image. Each inner array is a flattened matrix which
        represents a cell from the image being analyzed.
    resDict : dict
        A dictionary containing the information from the LibraryInfo.pkl
    userver : bool
        Enables(True) or disables(False) the user verification popup window.
    library_dir : str
        A string of the directory path to the library
    typeArray : list
        A list of strings, each of which represents a category
    pcThresh : float
        A percentage value of which proportion of principal components are used to compare a cell to the library. Valid
        values are between 0 and 100 inclusive.
    confThresh : float
        The confidence level a cell must have for it to be automatically classified. This is a percentage nd should be
        between 0 and 100 inclusive.
    near : int
        THe number of nearest neighbours in the library that will be considered when classifying a cell

    Returns
    -------
    resultCol : list
        A list which contains strings which represent the classification of each cell in the image
    confCol : ndarray
        An array of the confidence for each cell. THe indices of the confidences correspond to the indices of the
        classifications in resultCol.
   """

    # Variables for operation.
    pcThresh = pcThresh/100

    testNum = np.shape(inputData)

    # Set up large matrices so they do not grow with each iteration
    resultCol = ["---"]*testNum[0]
    confCol = np.zeros([testNum[0], 1])

    # Determine the edge length when displaying the cells to the user
    if userVer:
        edgeLength = np.sqrt(testNum[1])

    # Read in all the relevant variables
    eigenV = resDict['eigenV']
    score = resDict['SCORE']
    latent = resDict['latent']
    meanV = resDict['meanV']
    colTypes = resDict['colTypes']
    trainNum, _ = np.shape(score)

    # Determine the number of Principal components to use
    latentCum = np.cumsum(latent)
    threshold = np.max(latentCum)*pcThresh
    pcNum = findThresh(latentCum, threshold)
    if pcNum < 1:
        pcNum = 1

    # Take the determined number of components
    eigenCells = eigenV[:, 0:pcNum]
    gallery = score[:, 0:pcNum]

    # Project the data onto the eigencells
    features = np.matmul((inputData - np.tile(meanV, (testNum[0], 1))), eigenCells)

    # Recognise the cells
    for k in range(testNum[0]):
        if Globs.end:
            break
        # If the cell is on the edge, its entry will be set to all zeros. Using a very small number to avoid possible
        # float errors
        if np.abs(np.sum(inputData[k])) > 1e-20:

            # Select the current cell
            f = features[k]

            # Determine the distance of the cell from each of the eigencells in the library
            dist = np.sum(np.power((np.tile(f, (trainNum, 1)) - gallery), 2), axis=1)
            idx = np.arange(0, len(dist), 1)  # type: list[int]

            # Sort the lists by distance, keeping track of the original positions
            dist, idx = ((list(t) for t in zip(*sorted(zip(dist, idx)))))

            # Select the closest cells from the image library to the current cell
            top = dist[0:near]

            # Build a dictionary and a lookup array to keep track of what cell types are closest to the current cell
            typeDic = {}
            revTypeDic = []
            for j in range(len(top)):
                if not colTypes[idx[j]] in typeDic:
                    typeDic[str(colTypes[idx[j]])] = len(typeDic)
                    revTypeDic.append(str(colTypes[idx[j]]))

            # Determine the confidence for each type of cell among the closest
            typeScores = np.zeros(len(typeDic))
            for i in range(len(top)):
                cellSum = (1/(i+1))*(1/top[i])  # Since python counts indices from zero, rank is index + 1
                typeScores[typeDic[colTypes[idx[i]]]] += cellSum

            # Convert scores to percentages and find the most likely type
            typeScores = np.multiply(np.divide(typeScores, np.sum(typeScores)), 100)
            conf = np.max(typeScores)
            mPos = np.argmax(typeScores)

            # Perform user verification
            if userVer and (conf < confThresh):

                # Prepare the cell to be displayed
                img = np.reshape(inputData[k],
                                 [int(np.sqrt(np.size(inputData[k]))),
                                  int(np.sqrt(np.size(inputData[k])))])

                img = np.multiply(img, 256)

                # Bring up the verification window
                wind = Toplevel()
                verification = CellVerUI(wind, img.astype(int), typeArray)
                wind.mainloop()

                # Get the result of the selection
                decision = verification.type.get()

                # Destroy the window so the next image may be displayed correctly
                wind.destroy()

                if not (decision == "Ignore"):
                    # Save the image with a unique name
                    resultCol[k] = decision
                    type_dir = os.path.abspath(os.path.join(library_dir,decision))

                    name = str(datetime.now())
                    for char in " -.:":
                        name = name.replace(char, '')

                    filename = os.path.abspath(os.path.join(type_dir, name + '.tif'))

                    cv2.imwrite(filename, img)
                else:
                    resultCol[k] = 'Ignore'
                # if the user has verified, treat the result as certain
                conf = 100
            elif (conf < confThresh):
                resultCol[k] = 'Other'
            else:  # elseif userVer and (conf < confThresh):
                # Save the most likely cell type
                resultCol[k] = revTypeDic[mPos]

        else:  # elseif np.abs(np.sum(inputData[k])) > 1e-20:
            # Handle literal edge cases
            resultCol[k] = 'Edge'
            conf = 100
        # Save the confidence
        confCol[k] = conf
    return resultCol, confCol
