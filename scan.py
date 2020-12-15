from image_classifier import CrackDectectorLite
import os
import subprocess
import schedule
import picamera
import datetime
import time
import smtplib
import imghdr
import database
from email.message import EmailMessage

class Scan():
    def __init__(self):
        self.data = database.SensorData()
        
    def scan_file(self, scan_image):
        detector = CrackDectectorLite(scan_image)
        output_image, condition = detector.predict_tlite_real(scan_image)
        detector.close()
        return condition
    
    def scan_camera(self, recipients=None, alert=False, crop=False, position=None):

        file = time.strftime("%Y-%m-%d %H:%M:%S")
        filename = "real_images/" + file + ".jpg"
        subprocess.run(["raspistill", "-o", filename])

        detector = CrackDectectorLite(filename)
        if crop:
            detector.crop_img(position)
        (condition, cracks) = detector.predict_tlite_real(filename)[1]
        detector.close()
        self.data.add_scan(time=file, name='scan', condition=condition, cracks=cracks)
        if condition == True and alert == True:
            self.send_alert(file, recipients)
        return condition, file
    
    def schedule_scan(self, scan_interval, recipients, crop, position):
        schedule.every(scan_interval).minutes.do(self.scan_camera, 
                                                 recipients=recipients, 
                                                 alert=True, crop=crop,
                                                 position=position)                    

        while True:
            schedule.run_pending()
            time.sleep(30)

    def send_alert(self, filename, recipients):  #user input
        '''configure email alert when crack is detected'''
        contacts = recipients
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
            