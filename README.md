## Ground Station

### Intro
This is a Python project for connecting all of the various parts of the AERO ground station software suite. The ground station will receive images and telemetry, store all of this data into a database, and interface with the web client software to support in finding and documenting targets of interest.

### Requirements
* Python3
* MongoDB

### Getting started
1. Install Python3 [here](https://www.python.org/downloads/)
1. Install MongoDB [here](https://www.mongodb.com/download-center/community)
1. Install Pip Requirements using `python setup.py install` while in the groundstation directory.
* NOTE
	There may be some Python requirments not installed through the install script, just `pip3 install <package name>` for any dependencies that have not been installed yet.

### Usage
1. Run mongod in terminal `mongod`
1. To run the project(while in the groundstation directory), use the following command:

    `python start.py`

This will start the various servers and continue running.

