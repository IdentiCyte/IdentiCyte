import unittest
import numpy as np
from IdentiCyte.DisplayIdentified import *
from IdentiCyte.PCARecognition import *
from IdentiCyte.CellDetection import *
from IdentiCyte.CellStatistics import *
from IdentiCyte.ToGreyScale import *
from IdentiCyte.ProcessFiles import *
import cv2
import os
import pickle


class gcdTest(unittest.TestCase):
    def testgcd(self):
        self.assertEqual(gcd(3, 9), 3)
        self.assertEqual(gcd(8, 3), 1)


class threshTest(unittest.TestCase):
    def testthresh(self):
        self.assertEqual(findThresh([1, 3, 8, 9, 7, 23], 9), 3)


class detectTest(unittest.TestCase):
    def testanalyze(self):
        tstarr = np.ones([100,100], dtype=int)
        tstarr[0:99, 0] = -1
        tstarr[0:99, 99] = -1
        tstarr[0, 0:99] = -1
        tstarr[99, 0:99] = -1
        tstarr[20:25, 31:36] = 2
        tstarr[80:84, 72:74] = 3
        self.assertEqual(analyze(tstarr, 20), [[22, 33]])
        self.assertEqual(analyze(tstarr, 8), [[22, 33], [82, 72]])

    def testsegment(self):
        #self.img = cv2.imread(os.path.join(os.getcwd(), 'Cell Examples', 'Cell5.png'))
        #self.greyim = self.img[:, :, 0]
        tstarr = np.zeros([100,100])
        tstarr[25:76, 25:76] = 1
        kernel = np.ones([5, 5]) / 25
        greyarr = cv2.filter2D(tstarr, -1, kernel=kernel)
        greyarr = np.rint((greyarr)*255)
        shade = np.stack((greyarr,)*3, axis=-1)
        with open(os.path.join(os.path.dirname(__file__),'segmentTestKey'), 'rb') as fp:
            result = pickle.load(fp)
        np.testing.assert_array_equal(segment((tstarr*255).astype(np.uint8), shade.astype(np.uint8)), result)

    def testprocess(self):
        img = cv2.imread(os.path.join(os.path.dirname(__file__), 'Cell5.png'))
        with open(os.path.join(os.path.dirname(__file__),'processTestKey'), 'rb') as file:
            result = pickle.load(file)
        np.testing.assert_array_equal(process(img, 'B'), result)
        with open(os.path.join(os.path.dirname(__file__),'processTestKeyGTriangle'), 'rb') as file:
            GTriangleResult = pickle.load(file)
        np.testing.assert_array_equal(process(img, 'G', 'Triangle'), GTriangleResult)

        img = cv2.imread(os.path.join(os.path.dirname(__file__), 'Cell5Inv.png'))
        with open(os.path.join(os.path.dirname(__file__), 'processTestKeyInverted'), 'rb') as file:
            FluoroResult = pickle.load(file)
        np.testing.assert_array_equal(process(img, bf=False), FluoroResult)

    def testdetect(self):
        img = cv2.imread(os.path.join(os.path.dirname(__file__), 'Cell5.png'))
        self.assertEqual(detect(img), [[109, 116]])


class cellStatisticsTest(unittest.TestCase):
    def teststats(self):
        types = ['Apples', 'Oranges', 'Pears']
        data = [['Apples', 'Pears', 'Pears', 'Apples', 'Oranges'],
                ['Oranges', 'Oranges', 'Oranges', 'Apples', 'Pears', 'Pears'],
                ['Pears', 'Pears', 'Pears', 'Pears', 'Oranges']]
        result = [[2, 1, 0],
                  [1, 3, 1],
                  [2, 2, 4]]
        np.testing.assert_array_equal(CellStats(data, types), result)


class toGreyScaleTest(unittest.TestCase):
    def testgrayalizw(self):
        img = cv2.imread(os.path.join(os.path.dirname(__file__), '1_2.tif'))
        greyIm = cv2.imread(os.path.join(os.path.dirname(__file__), '1_2Grey.tif'))
        np.testing.assert_array_equal(greyalize(img), greyIm[:, :, 0])


class pcaRecognitionTest(unittest.TestCase):
    def testpcarecognition(self):
        lib_file = os.path.join(os.path.dirname(__file__), 'Library', 'LibraryInfo.pkl')
        with open(lib_file, 'rb') as f:
            resDict = pickle.load(f)
        types = ['BicEchinocytic', 'Biconcave', 'Echinocytic', 'Lysing', 'Other', 'SphEchinocytic', 'Spherocytic']
        img = cv2.imread(os.path.join(os.path.dirname(__file__), '1_2.tif'))
        # Convert to greyscale by taking a  channel
        imLine = greyalize(img)

        # Normalize
        imLine = imLine / np.max(imLine)

        # Add to the matrix of cells, where each 'row' is a cell
        imLine = np.reshape(imLine, [1, np.size(imLine)])
        [classification, conf] = PCARecognition(inputData=imLine,
                            resDict=resDict,
                            userVer=False,
                            library_dir=os.path.split(lib_file)[0],
                            typeArray=types)
        self.assertEqual(classification, ['Spherocytic'])
        # Have to round this or array([[62.56521685]]) != array([[62.56521685]])
        self.assertEqual(np.round(conf, 8), np.round(np.asarray([[62.56521685]]), 8))


class processFilesTest(unittest.TestCase):
    def testprocessfiles(self):
        imdir = os.path.join(os.path.dirname(__file__))
        libdir = os.path.join(os.path.dirname(__file__), 'Library')
        types = ['BicEchinocytic', 'Biconcave', 'Echinocytic', 'Lysing', 'Other', 'SphEchinocytic', 'Spherocytic']
        [types, confs, locs] = ProcessFiles(libdir, imdir, types)
        self.assertEqual(locs, [[[155, 156]], [[156, 152]], [[99, 110]], []])
        self.assertEqual(types, [['Edge'], ['Edge'], ['Edge'], []])
        
        self.assertEqual(confs[0:3], [np.array([[100.]]), np.array([[100.]]), np.array([[100.]])])
        np.testing.assert_almost_equal(confs[3], np.transpose(np.array([[]])))


def main():
    unittest.main()



if __name__ == "__main__":
    main()
