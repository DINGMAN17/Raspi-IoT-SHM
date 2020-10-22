#!/bin/sh


# Install packages
#PACKAGES="python-picamera python-pip python-schedule python-smbus python-numpy python-matplotlib sqlite3"

#apt-get update
#apt-get upgrade -y
#apt-get install $PACKAGES -y
#pip install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_armv7l.whl
#pip3 install peewee flask flask-admin wtf-peewee

# ENABLE interface
#for testing use /home/pi/config.txt 

#CONFIG="/boot/config.txt"
CONFIG="/home/pi/config.txt"  

if grep -Fq "start_x" $CONFIG
then
	echo "start_x exists"
	sed -i "s/start_x=0/start_x=1/" $CONFIG
else
	echo "start_x not found"
	echo "start_x=1" >> $CONFIG
fi

if grep -Fq "gpu_mem" $CONFIG
then
	echo "gpu_mem exists"
	sed -i "/gpu_mem/c\gpu_mem=128" $CONFIG
else
	echo "gpu_mem not found"
	echo "gpu_mem=128" >> $CONFIG
fi

if grep -Fq "i2c_arm" $CONFIG
then
	echo "i2c_arm exists"
	sed -i "/i2c_arm/c\dtparam=i2c_arm=on" $CONFIG
fi
