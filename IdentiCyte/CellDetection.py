"""
   File Name: CellDetection.py
   Version: 1.0
   Author: Guillaume Garnier
   Date Modified: 2018-11-22
   License: GNU-GPL-3.0-or-later
   Python Version 3.5
   Description: Locates all the cells in a batch of images
"""
import cv2
from scipy.ndimage.morphology import binary_fill_holes
import numpy as np

def detect(image,
           channel='B',
           method='Otsu',
           minSize=9000,
           bf=True):
    """
    Detects cells in an image

    This will find cells in a bright field or fluorescence microscopy image. It looks for spots of at least a specified
    size that contrast the background (dark for bf, bright for fluoro).

    Parameters
    ----------
    image : ndarray
        An array containing the pixel values of the image. Can be 3 channel colour or grey scale
    channel : str
        The colour channel that will be inspected, ignored if analyzing grey scale images
    method : str
        The algorithm used to threshold the image into binary when detecting cells. Either 'Otsu' or 'Triangle'.
    minSize : int
        The minimum number of pixels in a blob for it to be considered a cell and not small debris.
    bf : bool
        Indicates whether the image is bright field(True) or fluorescent(False)

    Returns
    -------
    imInfo : list
        A list of the approximate centroid for each cell detected in an image.
    """

    imBinar = process(image,
                      channel,
                      method,
                      bf)
    imInfo = analyze(imBinar, minSize)
    return imInfo


def process(image,
            channel='B',
            method='Otsu',
            bf=True):
    """
    Separates cells from the background of the image.

    The image is binarized, using the specified method. The cells in this binary image are then segmented out from
    the background.
    Parameters
    ----------
    image : ndarray
        An array containing the pixel values of the image. Can be 3 channel colour or grey scale
    channel : str
        The colour channel that will be inspected, ignored if analyzing grey scale images
    method : str
        The algorithm used to threshold the image into binary when detecting cells. Either 'Otsu' or 'Triangle'.
    bf : bool
        Indicates whether the image is bright field(True) or fluorescent(False)

    Returns
    -------
    outim : ndarray
        An array of the same size as the input image. The elements along the edge have a value -1, the background
        of the image is 1 and each detected cell has a unique positive integer value.
    """
    # Select the correct color channel
    if channel is 'R':
        select = 2
    elif channel is 'G':
        select = 1
    else:
        select = 0

    if len(np.shape(image)) == 3:
        try:
            img = image[:, :, select]
        except IndexError:
            img = image[:, :, 0]
    else:
        img = image


    # Perform the thresholding
    if method == 'Triangle':
        meth = cv2.THRESH_TRIANGLE
    elif method == 'Otsu':
        meth = cv2.THRESH_OTSU
    else:
        meth = 0
    if np.abs(img[0][0]) % 1 > 0:
        img = np.multiply(img, 255)
        img = img.astype(np.uint8)
        print('Hold')
    ret, binIm = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+meth)

    # Fill the holes in the cells
    if bf:
        binIm[binIm == 0] = True
        binIm[binIm == 255] = False
    else:
        binIm[binIm == 0] = False
        binIm[binIm == 255] = True
    filIm = binary_fill_holes(binIm)
    imtst = np.zeros(np.shape(filIm), np.uint8)

    imtst[filIm == False] = 0
    imtst[filIm == True] = 255

    outim = segment(imtst, image)
    return outim


def segment(img, image):
    """
    Separates cells from the background of the image.

    The image is binarized, using the specified method. The cells in this binary image are then segmented out from
    the background.
    Parameters
    ----------
    img : ndarray
        An array representing a binary image with dark spots representing cells on a white background.
        Numbers must have type uint8.
    image : ndarray
        An array containing the pixel values of a single channel image. Numbers must have type uint8.

    Returns
    -------
    markers : ndarray
        An array of the same size as the input image. The elements along the edge have a value -1, the background
        of the image is 1 and each detected cell has a unique positive integer value.
    """
    if (len(np.shape(image)) != 3) or (np.shape(image)[2] == 1):
        image = np.stack((image,) * 3, axis=-1)

    # Remove any small black noise spots
    kernel = np.ones((3, 3), np.uint8)

    op = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=2)
    op = np.uint8(op)

    # Prepare the image for watershedding
    sureBg = cv2.dilate(op, kernel, iterations=3)

    dstTransf = cv2.distanceTransform(op, cv2.DIST_L2, 5)

    dstTransf = np.rint(dstTransf).astype('uint8')
    _, sureFg = cv2.threshold(dstTransf, 0.6*np.max(dstTransf), 255, cv2.THRESH_BINARY)

    sureFg = np.uint8(sureFg)
    unknown = cv2.subtract(sureBg, sureFg)
    _, markers = cv2.connectedComponents(sureFg)

    markers = markers + 1
    markers[unknown == 255] = 0

    # Segment the images
    markers = cv2.watershed(image, markers)
    return markers


def analyze(segIm, minSize):
    """
    Counts the segmented cells in an image

    This counts the number of pixels with a unique value in an array and notes their co-ordinates within the array.
    For values with a high enough pixel count, it averages the co-ordinates and returns a centroid.

    Parameters
    ----------
    minSize : int
        The minimum number of pixels in a blob for it to be considered a cell and not small debris.
    segIm : ndarray
        An array of the same size as the input image. The elements along the edge have a value -1, the background
        of the image is 1 and each detected cell has a unique positive integer value.

    Returns
    -------
    list
        A list of the approximate centroid for each cell detected in an image.
    """
    # Counts the number of dark blobs in the image
    segment, count = np.unique(segIm, return_counts=True)
    resArr = []
    # Get all the relevant information from any cells.
    for j in range(len(segment)):
        if j > 1 and count[j] >= minSize:
            y, x = np.where(segIm == segment[j])
            resArr.append([int(np.round(np.mean(y))), int(np.round(np.mean(x)))])

    return resArr


