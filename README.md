# IdentiCyte
IdentiCyte is a program which has been designed to count and classify cells in an image microscopy image as simply as possible. 
## Getting Started 

Identicyte has been tested on Windows 10, Windows 7 and Ubuntu 17.10
### Downloading
To download the executable only, enter the dist folder above, then click on IdentiCyte.exe and then the Download button. When the popup window comes up, click the Save File button. The manual can similarly be downloaded from the Manual folder. 

###Running IdentiCyte
Once the file has been downloaded, and you have read the manual, IdentiCyte can be run by double clicking IdentiCyte.exe. If you get a popup saying that an unauthorised app was prevented from starting, then click Run anyway.

## How to cite
If you use IdentiCyte in your research, please cite the following journal article:
G. F. G. Garnier, C. A. Manderson, S. Giri, G. Garnier, Identicyte: Simple red blood cell identification software, SoftwareX (2019) [pages].

    @article{identicyte,  
    title={IdentiCyte: Simple Red Blood Cell Identification Software},  
	author= Garnier, Guillaume F. G. and Manderson, Clare A. and Giri, Saveen and Garnier, Gil},
	journal={SoftwareX},
	pages={????},
	year={2019?},
	publisher={Elsevier}
    }


## Development

To download IdentiCyte either click the green 'Clone or download' button and download zip, then extract the contents into a convenient directory.

Using git, copy the command below into the command line
> git clone https://github.com/IdentiCyte/IdentiCyte.git \path\to\destination

#### Requirements and Dependencies
If you wish to modify and run Identicyte you will require Python 3.5 or later and the following packages:

+ numpy
+ scipy
+ opencv-python
+ scikit-learn
+ sklearn
+ Pillow
+ mttkinter
+ matplotlib
+ XlsXWriter

###Installing
Install setuptools if it isn't already installed
> pip install setuptools 

Navigate to the folder containing setup.py 

> pip setup.py install 


### Running the program

If you have downloaded or built the executable, running it will start the program.
If you have installed the package, IdentiCyte can be run with the command
> python IdentiCyte

Once the window has appeared, analysis can be performed by following the instructions in the IdentiCyte manual. (Link to IdentiCyte manual download)

### Testing
To run tests, run the following command from the first IdentiCyte directory (the one which contains the setup.py file)
> python -m IdentiCyte.test.UnitTests

### Building the executable
If after modifying IdentiCyte, you wish to create your own executable, this may be done by following the steps below

Install the pyinstaller package for python, either with the command below or otherwise
> pip install pyinstaller

Navigate to the folder which contains the file 'Identicyte.spec', and if you are on Windows, run 

> pyinstaller IdentiCyte.spec

Or if you are on linux, theninstead run the command

> pyinstaller IdentiCyte_linux.spec

### Known issues
+ As of 29/11/2018, running an executable built in Ubuntu 17.10 causes an unending number of IdentiCyte windows to open.  
### Contributing
IdentiCyte is currently in development and  we are not looking for contributors at the moment.
