## Ground Station

### Intro
This is a Python project for connecting all of the various parts of the AERO ground station software suite. The ground station will receive images and telemetry, store all of this data into a database, and interface with the web client software to support in finding and documenting targets of interest.

### Requirements
This project depends on Python 3.6+

### Getting started
In the root directory, run the following command to install the project dependencies:

    python setup.py install

To run the project, use the following command:

    python start.py

This will start the various servers and continue running.

### Options
To simulate the receiving of images and telemetry for testing the web client, pass in the 'simulate' command line option. Example:

    python start.py simulate
