# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 21:07:22 2020

@author: DINGMAN
"""
import tkinter as tk
from user_interface import Setting
from monitoring_scan import Monitoring
from sensor import Sensor
from scan import Scan
from subprocess import call


class Run():
    
    def __init__(self):
        self.root = tk.Tk()
        self.setting = Setting(self.root)
        self.reset()        
        
    def reset(self):
        self.root.mainloop()
        self.get_parameters()
        
    def get_parameters(self):
        self.mode = self.setting.get_mode()
        self.sensor_interval = self.setting.get_sensor_interval()
        self.critical_load = self.setting.get_critical_load()
        self.camera = self.setting.get_camera()
        self.upload_status = self.setting.upload
        if self.upload_status == True:
            self.scan_image = self.setting.filename
        self.scan_interval = self.setting.get_scan_interval()
        self.recipients = self.setting.get_recipients()
    
    def mode_all(self):
        if self.camera == 'True':
            if self.sensor_interval > 0 and self.scan_interval > 0:
                try:
                    print('Program starts...')
                    monitoring = Monitoring(self.critical_load, self.sensor_interval, self.scan_interval, self.recipients)
                    monitoring.add_sensor('sensor1', 'Fibre-optic', 0) #set it as user input
                    monitoring.schedule_scan()
                except KeyboardInterrupt:
                    print('Monitoring stops...')
            else:
                print('Please rerun the program and enter the intervals')
        else:
            print('Please install camera module and rerun the program')
        

    def mode_sensor(self):
        if self.sensor_interval > 0:
            try:
                print('Program starts...')
                sensor = Sensor(self.sensor_interval)
                sensor.add_sensor('sensor1', 'Fibre-optic', 0) #set it as user input
                sensor.log_data()
            except KeyboardInterrupt:
                print('Monitoring stops...')
            
        else:
            print('Please rerun the program and enter the sensor interval')
        
    
    def mode_scan(self):       
        scan = Scan()  
        if self.upload_status == True:
            condition = scan.scan_file(self.scan_image)
            print(condition)
        elif self.camera == 'True' and self.scan_interval > 0:
            scan.schedule_scan(self.scan_interval)
            self.execute_web = True
        elif self.camera == 'False' and self.upload_status == False:
            print('Please install camera or upload an image')
        else:
            scan.scan_camera()

def main():
    r = Run()
    if r.mode == "load monitoring and scan" :
        r.mode_all()
        
    elif r.mode == 'load monitoring only':
        r.mode_sensor()
    
    elif r.mode == 'scan only':
        r.mode_scan()
        
    else:
        print('Please rerun the program and choose a mode')

if __name__ == '__main__':
    main()



    
