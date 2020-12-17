# Raspberry Pi AIoT application for structural health monitoring
AIoT application that focuses on load/displacement monitoring and crack detection using Raspberry Pi, fibre optic sensor, camera module. 

## Table of contents
* [General info](#general-info)
* [Installation](#installation)
* [Hardware](#Hardware)
* [Usage](#usage)

## General info
This application aims to provide a highly automated, real-time, accurate solution to structural health monitoring.
There are two main functions: 
- load/displacement monitoring using fibre optic sensor; 
- crack detectioin using pretrained deep learning CNN model and camera module. 

Parameters such as sensor interval can be configured via UI. 
The real-time monitoring and scan results will be updated on a webpage.
	
## Installation

installer.sh takes care of all the installation and configuration for this application. Run the following command:

```bash
chmod u+x installer.sh
./installer.sh
```

## Hardware
There are three modes in this application which require different hardware settings.
1. Load monitoring using fibre optic sensor

For this mode to work, you need to have a fiber optic sensor, analog digital converter, breadboard, several jumper wires, resistors. Please connect the sensor based on the breadboard diagram below:

![Image of sensor connection](https://github.com/DINGMAN17/Raspi-IoT-SHM/blob/main/Breadboard%20final.JPG)

2. Crack scan using pretrained CNN model

This mode can be further divided into two sub-modes:
- real-time crack detection using camera module: a Raspberry Pi camera module is required. (both v2 and HD camera module are suitable)

If camera is installed, to adjust camera, run:
```bash
python3 camera.py
```
If the photo needs to be cropped, follow the steps below:

(a) Take a photo and save as test.jpg
```bash
raspistill -o test.jpg
```
(b) Open the test.jpg file using Mirage. Select edit -> crop, select the correct region, take note of the value of X, Y, width, height:

![crop image using mirage](https://github.com/DINGMAN17/Raspi-IoT-SHM/blob/main/crop_mirage.PNG)

(c) Enter the above values in the UI:

![Entering values in UI](https://github.com/DINGMAN17/Raspi-IoT-SHM/blob/main/crop_image.PNG)

- crack detection via file-upload: no hardware is required, image file can be uploaded via UI

3. Load monitoring with scheduled crack scan and emergency scan

Both sensor and camera module are required. 


## Usage

After hardware setup, run the program:
```bash
sudo python3 main.py
```
When results start printing out in the terminal, run the web application (better to open a new connection so that the main program's output result can be clearly seen). 

The images taken by camera module are saved in 
[real_images](https://github.com/DINGMAN17/Raspi-IoT-SHM/tree/main/real_images) folder.
(feel free to use any images in this folder to test the crack detection model)

The output images from scan process are saved automatically in [scan_image](https://github.com/DINGMAN17/Raspi-IoT-SHM/tree/main/static/scan_image) folder under static directory. The image file is named with 'out_' and the timestamp. 

Run the following command:
```bash
FLASK_APP=webapp.py flask run --host=0.0.0.0
```
Open a browser and navigate to http://raspberrypi:5000/ (or use raspberry Pi's IP address, for example, http://192.168.0.18:5000/ )
To find Raspberry Pi's IP address, run:
```bash
hostname -I
```
