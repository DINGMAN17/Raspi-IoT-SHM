import smbus
import datetime
import time
import os
import schedule
import subprocess
import threading
import picamera
import smtplib
import imghdr
import database
from email.message import EmailMessage
from image_classifier import CrackDectectorLite

class Monitoring():
    def __init__(self, critical_load, sensor_interval, scan_interval, recipients, crop, position):
        self.address = 0x48
        self.bus = smbus.SMBus(1)
        self.cmd = 0x40
        self.critical_load = critical_load
        self.sensor_interval = sensor_interval
        self.scan_interval = scan_interval
        self.recipients = recipients
        self.crop = crop
        self.position = position
        self.data = database.SensorData() #create a database instance
        self._lock = threading.Lock() #create a lock to syncronize access to hardware from different threads
        #setup a thread to read sensor value every 3 seconds and store its last known value
        self._load = 0
        self._displacement = 0
        self._sensor_thread = threading.Thread(target=self.log_data)
        self._scan_thread = threading.Thread(target=self.critical_scan)
        self._sensor_thread.daemon = True #make sure the thread don't block exiting
        self._scan_thread.daemon = True        
        self._sensor_thread.start()
        self._scan_thread.start() 
        
    def add_sensor(self, name, sensor_type, channel):
        self.data.define_sensors(name, sensor_type, channel)

    def analogRead(self, chn):
        with self._lock:
            value = self.bus.read_byte_data(self.address,self.cmd + chn)
            return value
    
    def analogWrite(self, value):
        self.bus.write_byte_data(self.address,self.cmd,value) 
    
    def log_data(self):       
        try:    
            while True:
                read_time = time.strftime("%Y-%m-%d %H:%M:%S")
                for sensor in self.data.get_sensors():
                    value = self.analogRead(sensor.channel)       
                    voltage = value / 255.0 * 5
                    self._load = 33.367 * voltage - 34.067
                    self._displacement = -0.03483 * self._load - 0.05111  
                    print('Read sensor: {0} load: {1:0.2f}N'.format(sensor.name, self._load))
                    self.data.add_reading(time=read_time, name='{0} load'.format(sensor.name), value='{0:0.2f}'.format(self._load))
                    self.data.add_reading(time=read_time, name='{0} displacement'.format(sensor.name), value='{0:0.2f}'.format(self._displacement))
                time.sleep(self.sensor_interval)
        finally:
            self.data.close()
    
    def get_load(self):
        '''get the most recent load value'''
        return self._load
        
    def get_displacement(self):
        '''get the most recent displacement value'''
        return self._displacement
            
    def scan(self, name, alert=True):    
        file = time.strftime("%Y-%m-%d %H:%M:%S")
        filename = "real_images/" + file + ".jpg"
        subprocess.run(["raspistill", "-o", filename])
        
        detector = CrackDectectorLite(filename)
        if self.crop:
            detector.crop_img(self.position)
        (condition, cracks) = detector.predict_tlite_real(filename)[1]
        detector.close()
        self.data.add_scan(time=file, name=name, condition=condition, cracks=cracks)
        if condition == True and alert == True:
            print('sending alert email')
            self.send_alert(file)
        return condition, file
    
    def send_alert(self, filename):  #user input
        '''configure email alert when crack is detected'''
        contacts = self.recipients
        email_sender = os.environ.get('EMAIL_USER') 
        email_password = os.environ.get('EMAIL_PASSWORD')

        msg = EmailMessage()
        msg['Subject'] = 'Crack Alert!!!'
        msg['From'] = email_sender
        msg['To'] = ', '.join(contacts)
        time_scan = self.data.get_scan_time()
        msg.set_content('Crack is detected in the most recent scan at ' + time_scan)
        
        filename = os.path.join('static','scan_image', "out_" + filename + '.png')
        with open(filename, 'rb') as f:
            file_data = f.read()
            file_type = imghdr.what(f.name)
            file_name = f.name

        msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_sender, email_password)    

            smtp.send_message(msg)

    def critical_scan(self):
        '''critical scan is called if the load value reaches 
        the maximum capacity of the structural'''
        while True:
            if self.get_load() > self.critical_load:     #assume a random critical condition
                print('perform emergency scan')
                self.scan('emergency_scan')
            time.sleep(5)
                
    def schedule_scan(self):
        '''configure the scan to be a schedule task, automatically perform every user defined intervals'''
        schedule.every(self.scan_interval).minutes.do(self.scan, name='schedule_scan')
        
        while True:
            schedule.run_pending()
            time.sleep(30)

def main():
    print ('Program is starting ... ')
    
    try:
        monitoring = Monitoring(50, 10, 5, ['man.ding@u.nus.edu'])
        monitoring.add_sensor('sensor1', 'Fibre-optic', 0) #set it as user input
        monitoring.schedule_scan()
        
    except KeyboardInterrupt:
        monitoring.destroy()

if __name__ == '__main__':
    main()
        
    
