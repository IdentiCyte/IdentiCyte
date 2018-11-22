"""
   File Name: ToGreyScale.py
   Author: Guillaume Garnier
   Date Modified: 2018-11-20
   License: GNU-GPL-3.0-or-later
   Python Version 3.5
   Description: Converts an RGB image to depth-bit greyscale.
"""
import numpy as np


def greyalize(imArray, depth=3, colour='B'):
    """
        Converts an image into a greyscale version with a lower bit depth.


        Parameters
        ----------
        imArray : ndarray
            An array containing the pixel values of the image. Can be 3 channel colour or grey scale
        depth : int
            The bit depth of the output image. there will be  2^depth levels of grey in the result. Valid values are
            between 1 and 8 inclusive.
        channel : str
            The colour channel that will be inspected, ignored if analyzing grey scale images

        Returns
        -------
        ndarray
            An array representing the grey scale image with 2^depth distinct values of grey
        """
    if depth < 1:
        depth = 1
    elif depth > 8:
        depth = 8
    greyShades = pow(2, depth)
    greyDist = 256/greyShades

    # Channel selection
    if colour == 'R':
        channel = 0
    elif colour == 'G':
        channel = 1
    else:
        channel = 2

    # Check if a channel needs to be selected
    if len(imArray.shape) == 3:
        try:
            greyim = imArray[:, :, channel]
        except IndexError:
            greyim = imArray[:, :, 0]
    else:
        greyim = imArray[:, :]

    mini = np.min(greyim)
    norm = greyim - mini
    out = np.ceil((norm/np.max(norm)) * greyShades)*greyDist
    out[out > 255] = 255
    return out.astype(int)
