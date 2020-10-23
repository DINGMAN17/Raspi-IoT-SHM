# Raspberry Pi IoT application for strucural health monitoring
IoT application in structural health monitoring using Raspberry Pi

## Table of contents
* [General info](#general-info)
* [Installation](#installation)
* [Hardware](#Hardware)
* [Usage](#usage)

## General info

	
## Installation

installer.sh takes care of all the installation and configuration for this application. Run the following command:

```bash
chmod u+x installer.sh
./installer.sh
```

## Hardware
There are three modes in this application which require different hardware settings.
1. Load monitoring using fibre optic sensor
For this mode to work, you need to have a fiber optic sensor, analog digital converter, breadboard, jumper wires.


## Usage

After hardware setup, run the program:
```bash
sudo python3 main.py
```
When results start printing out in the terminal, run the web application (better to open a new connection so that the main program's output result can be clearly seen). 
Run the following command:
```bash
FLASK_APP=webapp.py flask run --host=0.0.0.0
```
Open a browser and navigate to http://raspberrypi:5000/ (or use raspberry Pi's IP address, for example, http://192.168.0.18:5000/ )
To find Raspberry Pi's IP address, run:
```bash
hostname -I
```
