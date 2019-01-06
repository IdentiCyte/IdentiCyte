"""
   File Name: CellStatistics.py
   Version: 1.0
   Author: Guillaume Garnier
   Date Modified: 2018-12-13
   License: GNU-GPL-3.0-or-later
   Python Version 3.5
   Description: Counts the number of each type of cell in the batch of images
"""
import numpy as np

def CellStats(cellData, # type: List[List[str]]
              typeArray  # type: List[str]
              ):
    # type: (List[List[str]], List[str]) -> List[List[float]]
    """
    Compiles the data from the analysis.

    Parameters
    ----------
    cellData : list
        A list which contains a list of cell types for each analysed image. The cell types are represented as strings.
    typeArray : list
        A list of strings, each of which represents a category
    Returns
    -------
    cellTypeCount: list
        An array of arrays. Each array coresponds to an image and has a number of entries equal to the number of
        categories. The value in each index of the inner arrays corresponds to the number of cells of the type which
        lies in the same index of typeArray.
    """
    depth = len(cellData)
    catNum = len(typeArray)
    # Create an array with 1 more entry than the number of types, for unclassified cells
    cellTypeCount = np.zeros([catNum, depth])
    # Count each type of cell
    for i in range(len(cellData)):
        for j in cellData[i]:
            for k in typeArray:
                if k in str(j):
                    j = k
                    break
            if j in typeArray:
                cellTypeCount[typeArray.index(j), i] += 1
            else:
                # Generally for 'Other', 'Ignored' and 'Edge' cells
                cellTypeCount[-1, i] += 1
    return cellTypeCount
