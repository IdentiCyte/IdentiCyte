"""
   File Name: WriteResults.py
   Author: Guillaume Garnier
   Date Modified: 2019-01-07
   License: GNU-GPL-3.0-or-later
   Python Version 3.5
   Description: Writes the results of the analysis to the summary Excel sheet and pickle file
"""
import xlsxwriter
import numpy as np
import os
import pickle
import re


def WriteResults(stat,
                 typeArray,  # type: List[str]
                 locations,  # type: List[List[int]]
                 pics_dir,  # type: str
                 l_dir,  # type: str
                 results,  # type: List[List[str]]
                 conf,  # type: List[ndarray]
                 pcThresh,  # type: float
                 confThresh,  # type: float
                 userver,  # type: bool
                 bits,  # type: int
                 color,  # type: str
                 method,  # type: str
                 cellSize,  # type: int
                 near,  # type: int
                 bf  # type: bool
                 ):
    # type: (...) -> None
    """
    Collects all the data from the analysis and writes it to an Excel spreadsheet

    Parameters
    ----------
    stat : ndarray
        An array of arrays. Each array coresponds to an image and has a number of entries equal to the number of
        categories. The value in each index of the inner arrays corresponds to the number of cells of the type which
        lies in the same index of typeArray.
    typeArray : list
        A list of strings, each of which represents a category
    locations : list
        A list of lists. Each list corresponds to one of the images analysed and has the location of each cell in
        the corresponding image.
    pics_dir : str
        A string of the directory path to the images to be analysed
    l_dir : str
        A string of the directory path to the library
    results : list
        A list of lists. Each list corresponds to one of the images analysed and has the classifications of cells in
        the corresponding image.
    conf : list
        A list of ndarrays. Each array corresponds to one of the images analysed and has the confidences of cells in
        the corresponding image.
    pcThresh : float
        A percentage value of which proportion of principal components are used to compare a cell to the library. Valid
        values are between 0 and 100 inclusive.
    confThresh : float
        The confidence level a cell must have for it to be automatically classified. This is a percentage nd should be
        between 0 and 100 inclusive.
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
    bf : bool
        Indicates whether the image is bright field(True) or fluorescent(False)

    Returns
    -------
    Outputs a .xls file with a summary of the analysis
   """
    for j in range(len(results)):
        if type(results[j]) is np.ndarray:
            results[j] = results[j].tolist()

    for j in range(len(results)):
        for k in range(len(results[j])):
            results[j][k] = [results[j][k], ' %.1lf%%' % conf[j][k], [int(locations[j][k][0]), int(locations[j][k][1])]]

    # Make the file's name
    dataName = os.path.split(pics_dir)[-1]
    results_file = os.path.abspath(os.path.join(pics_dir, 'IdentifiedCellInfo.pkl'))

    results.append(typeArray)
    with open(results_file, 'wb') as f:
        pickle.dump(results, f)

    # Calculate the average confidence per image
    for lst in range(len(conf)):
        if len(conf[lst]):
            tmpMean = 0
            # Get the average of all non edge cells
            for perc in range(len(conf[lst])):
                if 'Edg' not in results[lst][perc]:
                    tmpMean = tmpMean + conf[lst][perc]
            if len(conf[lst]) > 0:
                tmpMean = tmpMean/len(conf[lst])
            else:
                tmpMean = 0
            try:
                conf[lst] = tmpMean[0]
            except:
                conf[lst] = tmpMean
        else:
            conf[lst] = 0

    # Find the average confidence for the folder
    conf = np.insert(conf, 0, np.mean(conf))

    # Complete the confidence column
    confStr = ['%.1lf%%' % np.mean(conf[lst]) for lst in range(len(conf))]
    confStr.insert(0, 'Confidence Per Image')

    # Calculate the total number of cells in each image
    totalNums = []
    for j in range(len(stat[0])):
        runCount = 0
        for k in range(len(stat)):
            runCount += stat[k][j]
        totalNums.append(int(runCount))

    # Find the total number of cells in the folder
    totalNums.insert(0, sum(totalNums))

    # Get the total number of each type of cell in the folder
    outStat = []
    for j in range(len(stat)):
        outStat.append(np.insert(stat[j], 0, sum(stat[j])))

    # Convert number of cells per image to a percentage
    for j in range(1, len(outStat[0])):
        if not (totalNums[j] == 0):
            for k in range(len(outStat)):
                outStat[k][j] /= totalNums[j]
                outStat[k][j] *= 100

    # Find the total number of desirable cells (All cells not in the 'Other', 'Edge' or 'Ignore' categories)
    totalNums.insert(1, int(totalNums[0] - outStat[-1][0] - outStat[-2][0]))
    totalNums.insert(0, '')
    for j in range(len(outStat)):
        outStat[j] = outStat[j].tolist()

    # Convert the output stats to strings
    for j in range(len(outStat)):
        for k in range(1, len(outStat[0])):
            outStat[j][k] = '%.1lf%%' % outStat[j][k]

    # Add the percentage of each type of cell counted
    for j in range(len(outStat)):
        if totalNums[2] > 0:
            outStat[j].insert(1, '%.1lf' % (outStat[j][0]*100/totalNums[2]))
        else:
            outStat[j].insert(1, '0')
        outStat[j].insert(0, typeArray[j])
    outStat[-1][2] = '-'
    outStat[-2][2] = '-'

    # Get the names of files
    img_names = os.listdir(pics_dir)
    for entry in range(len(img_names) - 1, -1, -1):
        exp = re.compile("\.png$|\.tif$|\.jpg$|\.jpeg$|\.tiff$", re.I)
        an_image = bool(exp.search(img_names[entry]))
        if os.path.isdir(os.path.abspath(os.path.join(pics_dir, img_names[entry]))) or not an_image:
            img_names.pop(entry)

    # Complete the first column
    img_names.insert(0, 'Percent of Identified Cells')
    img_names.insert(0, 'Cells Per Category')
    img_names.insert(0, 'Library Categories')

    # Combine all the matrices for outputting
    outStat.insert(0, img_names)
    outStat.append(totalNums)

    # Make the file's name
    file_name = os.path.abspath(os.path.join(pics_dir, dataName + '.xlsx'))

    # Write out to the excel doc
    workbook = xlsxwriter.Workbook(file_name)
    summarySheet = workbook.add_worksheet("Summary")
    detailedSheet = workbook.add_worksheet("Per Image Breakdown")

    # Define the settings summary############
    namesCol = ['Image Location',
                'Library Location',
                'User Verification',
                'Bit Depth',
                'Color Channel',
                'Thresholding Method',
                'Minimum Cell Size',
                'Confidence Percent',
                'Principal Component Percent',
                'Illumination',
                'Number of Similar Images Considered']

    yn = ['Disabled', 'Enabled']
    illum = ['Fluorescent', 'Bright Field']
    settingsCol = [pics_dir,
                   l_dir,
                   yn[userver],
                   bits,
                   color,
                   method,
                   cellSize,
                   confThresh,
                   pcThresh,
                   illum[bf],
                   near]
    row = 1
    for k in outStat:
        k.insert(3,' ')
    # Write the summary sheet and the detailed overview
    for col, data in enumerate(outStat[0:-1]):
        summarySheet.write_column(row, col, data[0:3])
        detailedSheet.write_column(row-1, col, [data[0]]+data[4:])

    #confStr.insert(2, ' ')
    summarySheet.write_column(row, len(outStat), outStat[-1][0:3])
    detailedSheet.write_column(0, len(outStat), ['Cells per Image'] + outStat[-1][4:])
    detailedSheet.write_column(0, len(outStat)+2, [confStr[0]]+confStr[2:])
    detailedSheet.write_column(0,0, ["Image Name"])

    summarySheet.write_row(0, 0, ["Dataset Name", dataName])
    summarySheet.write_row(5, 0, ['Mean Confidence of all Images'])
    summarySheet.write_row(5, 1, [confStr[1]])
    summarySheet.write_column(2, len(outStat)+1, ['Total Cells in Batch', 'Cells Identified'])
    summarySheet.write_column(9,0, namesCol)
    summarySheet.write_column(9, 1, settingsCol)
    img_names.pop(1)
    img_names[1] = 'Overall Confidence'

    workbook.close()
