
# IdentiCyte

## Getting Started 

Identicyte has been tested on Windows 10, Windows 7 and Ubuntu 17.10
### Downloading
To download IdentiCyte either click the green 'Clone or download' button and download zip, then extract the contents into a convenient directory.

Alternatively, to use the command line, ensure that you have git installed and  copy the command below into the command line
> git clone https://github.com/IdentiCyte/IdentiCyte.git \path\to\destination
###Installing
Install setuptools if it isn't already installed
> pip install setuptools 

Navigate to the folder containing setup.py 

> pip setup.py install 

## Building the executable
First ensure that all the dependencies for IdentiCyte have been installed. If you have already installed IdentiCyte then this should already be done, otherwise 

Install pyinstaller
> pip install pyinstaller

Navigate to the folder which contains the file 'Identicyte.spec'

> pyinstaller IdentiCyte.spec

+ Note: If you are running IdentiCyte in Linux then you will need to edit IdentiCyte.spec  in the following ways:
>  IdentiCyte\\\\\_\_main\_\_.py **becomes** IdentiCyte/\_\_main\_\_.py

> .\\\\IdentiCyte  **becomes** ./IdentiCyte


+ Note 2: As of 29/11/2018, running an executable built in Ubuntu 17.10 causes an unending number of IdentiCyte windows to open.  


## Running the program

If you have downloaded or built the executable, running it will start the program.
If you have installed the package, IdentiCyte can be run with the command
> python IdentiCyte

Once the window has appeared, analysis can be performed by following the instructions in the IdentiCyte manual. (Link to IdentiCyte manual download)

## Testing
To run tests, run the following command from the first IdentiCyte directory (the one which contains the setup.py file)
> python -m IdentiCyte.test.UnitTests
## Contributing
IdentiCyte is currently in development and  we are not looking for contributors at the moment.

## How to cite


G. F. G. Garnier, C. A. Henderson, S. Giri, G. Garnier, Identicyte: Simple red blood cell identification software, SoftwareX (2019) [pages].

@article{identicyte,
	title={IdentiCyte: Simple Red Blood Cell Identification Software},
	author={Guillaume F. G. Garnier and Clare A. Henderson and Saveen Giri and Gil Garnier},
	journal={SoftwareX},
	pages={????},
	year={2019?},
	publisher={Elsevier}
}
