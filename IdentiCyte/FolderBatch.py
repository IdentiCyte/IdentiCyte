import os
import sys
import IdentiCyte.Globs as Globs
from IdentiCyte.CellRecognitionDriver import driver


def batch(l_dir,  # type: str
           pics_dirs,  # type: str
           window=None,  # type: Opional(MainWindow)
           userver=False,  # type: Opional(bool)
           bits=3,  # type: Opional(int)
           color='B',  # type: Opional(str)
           method='Triangle',  # type: Opional(str)
           cellSize=9000,  # type: Opional(int)
           pcThresh=90,  # type: Opional(float)
           confThresh=50,  # type: Opional(float)
           bf=True,  # type: Opional(bool)
           near=10  # type: Opional(int)
           ):
    folders = []
    for item in os.listdir(pics_dirs):
        if os.path.isdir(os.path.join(pics_dirs, item)) and not item == 'Labelled' and not Globs.batchEnd:
            window.printout('Batching ' + item)
            batch(l_dir,  # type: str
                  os.path.join(os.path.join(pics_dirs, item)),  # type: str
                  window=window,  # type: Opional(MainWindow)
                  userver=False,  # type: Opional(bool)
                  bits=3,  # type: Opional(int)
                  color='B',  # type: Opional(str)
                  method='Triangle',  # type: Opional(str)
                  cellSize=9000,  # type: Opional(int)
                  pcThresh=90,  # type: Opional(float)
                  confThresh=50,  # type: Opional(float)
                  bf=True,  # type: Opional(bool)
                  near=10  # type: Opional(int)
                  )
            driver(l_dir,  # type: str
                   os.path.join(os.path.join(pics_dirs, item)),  # type: str
                   window=window,  # type: Opional(MainWindow)
                   userver=False,  # type: Opional(bool)
                   bits=3,  # type: Opional(int)
                   color='B',  # type: Opional(str)
                   method='Triangle',  # type: Opional(str)
                   cellSize=9000,  # type: Opional(int)
                   pcThresh=90,  # type: Opional(float)
                   confThresh=50,  # type: Opional(float)
                   bf=True,  # type: Opional(bool)
                   near=10  # type: Opional(int)
                   )
