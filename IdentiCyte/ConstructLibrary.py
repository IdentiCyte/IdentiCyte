"""
   File Name: ConstructLibrary.py
   Version: 1.0
   Author: Guillaume Garnier
   Date Modified: 2018-11-21
   License: GNU-GPL-3.0-or-later
   Python Version 3.5
   Description: Compiles all the images in the library into a single pickle file for use in the analysis.
"""
from sklearn import decomposition as skde
import numpy as np
import os
import matplotlib; matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import pickle


def compileLibrary(l_dir,  # type: str
                   window=None  # type: Optional(MainWindow)
                   ):
    # type: (str, Optional(MainWindow)) -> None
    """
    Compiles the images in the library folder into a LibraryInfo.pkl with relevant information.

    The cell images are compiled in a matrix which has Principal Component Analysis applied to it. The results of this
    are saved so that these calculations do not need to be run at each execution.

    Parameters
    ----------
    l_dir : str
        The path to the library folder with images if cells categorized in folders.
    window : MainWindow
        The main GUI window
    Returns
    -------
    Libraryinfo.plk: pickle file
        A file containing a dictionary with the results from the PCA as well as the types of the cells in the library.
    """
    sub_dirs = os.listdir(l_dir)

    # Remove any files and leave  only folders
    for entry in range(len(sub_dirs)-1, -1, -1):
        if not os.path.isdir(os.path.abspath(os.path.join(l_dir, sub_dirs[entry]))):
            sub_dirs.pop(entry)

    colTypes = []
    libraryData = []

    # Prepare the data to be saved
    for category in sub_dirs:
        if window:
            window.printout(category)
        curr_dir = os.path.abspath(os.path.join(l_dir, category))

        imageList = os.listdir(curr_dir)

        # Discard all entries that are not TIFF images
        for file in range(len(imageList)-1, -1, -1):
            if not imageList[file].endswith('.tif'):
                imageList.pop(file)

        # If there are any images
        if len(imageList) > 0:
            # Look at the first image to get the size of every image. Images must be the same size
            currImage = os.path.abspath(os.path.join(curr_dir, imageList[0]))
            tst = plt.imread(currImage)
            imsize = np.size(tst)


            tmpTrainData = np.zeros([len(imageList), imsize])
            tmpColTypes = ['---'] * len(imageList)

            # Prepare the data in each image for PCA
            for img in range(len(imageList)):
                # Read in the current image
                image_path = os.path.abspath(os.path.join(curr_dir, imageList[img]))
                image = plt.imread(image_path)

                # Data needs to be in a 'row', make it so
                imline = np.reshape(image, [1, np.size(image)])

                # Save the type of cell as well
                tmpColTypes[img] = str(category)

                # Add the row to the matrix
                tmpTrainData[img, :] = imline/np.max(imline)

            # Collect all of the temporary data for future use
            colTypes.append(tmpColTypes[:])
            if libraryData == []:
                libraryData = tmpTrainData
            else:
                libraryData = np.concatenate((libraryData, tmpTrainData))

    # Collapse colTypes List
    colTypes = [item for sublist in colTypes for item in sublist]

    if not libraryData == []:
        if window:
            window.printout('Library Loaded')
            window.printout('Compiling Library. This may take several minutes and the program may become unresponsive.')

        # Perform PCA and save everything to a .mat file
        pca = skde.PCA()
        pca.fit(libraryData)
        SCORE = pca.fit_transform(libraryData)
        COEFF = np.transpose(pca.components_)
        latent = pca.explained_variance_
        meanV = np.mean(libraryData, axis=0)
        dicti = {'latent': latent, 'SCORE': SCORE, 'eigenV': COEFF,
                'colTypes': colTypes, 'meanV': meanV}
        name = 'LibraryInfo'

        if window:
            window.printout('Library Compiled')
            window.printout('Saving Library to File')

        library_file = os.path.abspath(os.path.join(l_dir, name + '.pkl'))
        with open(library_file, 'wb') as f:
            pickle.dump(dicti, f)
    else:
        if window:
            window.printout('There were no images to compile in the library.')

