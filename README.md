# IdentiCyte
IdentiCyte is software which counts and classifies cells in an microscopy image with a focus on ease of use.
## Using IdentiCyte 

### Downloading and Running IdentiCyte
To download the software, enter the dist folder above, then click on IdentiCyte.exe and then the Download button. When the popup window comes up, click the Save File button. Identicyte has been tested on Windows 10, Windows 7 and Ubuntu 17.10

The manual contains instructions for using IdentiCyte and can be found in the Manual folder. 

###Running IdentiCyte
Once the file has been downloaded, and you have read the manual, IdentiCyte can be run by double clicking IdentiCyte.exe. If you get a popup saying that an unauthorised app was prevented from starting, then click Run anyway.

## How to cite
If you use IdentiCyte in your research, please cite the following journal article:

G. F. G. Garnier, C. A. Manderson, S. Giri, G. Garnier, IdentiCyte: Simple red blood cell identification software, [in press].

## Development and Contributing to IdentiCyte

### Contributing
IdentiCyte is currently in development and  we are not looking for contributors at the moment.


To download the source code of IdentiCyte either click the green 'Clone or download' button and download zip, then extract the contents into a convenient directory.

Alternatively, to download with git from the command line, copy the command below into the command line and change the path to destination to the directory where you wish to download IdentiCyte.
> git clone https://github.com/IdentiCyte/IdentiCyte.git \path\to\destination

###Installing
IdentiCyte has been written in Pythin and requires a 64 bit Python 3.5 installation. To set up and run Identicyte from the command line, follow the instrictions below.
 
Install setuptools if it isn't already installed
> pip install setuptools 

Navigate to the folder containing setup.py 

> pip install -e .

IdentiCyte can then be run with the command
> python IdentiCyte

#### Requirements and Dependencies
If you wish to modify and run IdentiCyte you will require 64-bit Python 3.5 or later and the following packages:

+ numpy
+ scipy
+ opencv-python
+ scikit-learn
+ Pillow
+ mttkinter
+ matplotlib
+ XlsXWriter
+ scikit-image

### Testing
If you have made changes to the code and wish to verify that IdentiCyte is still behaving as intended, unit tests can be run with the following command
> python -m IdentiCyte.test.UnitTests

### Building the executable
If after modifying IdentiCyte, you wish to create your own executable, this may be done by following the steps below.

Install the pyinstaller package for python, either with the command below or otherwise
> pip install pyinstaller

Navigate to the folder which contains the file 'Identicyte.spec', and if you are on Windows, run 

> pyinstaller IdentiCyte.spec

Or if you are on linux, theninstead run the command

> pyinstaller IdentiCyte_linux.spec

The executable will be created in the dist folder of the project.

### Known issues
+ As of 29/11/2018, running an executable built in Ubuntu 17.10 causes an unending number of IdentiCyte windows to open.  
