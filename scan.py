from image_classifier import CrackDectectorLite
import picamera
import datetime
import time
import database

class Scan():
    def __init__(self):
        self.data = database.SensorData()
        
    def scan_file(self, scan_image):
        detector = CrackDectectorLite(scan_image)    
        output_image, condition = detector.predict_tlite_real(scan_image)
        detector.close()
        return condition
    
    def scan_camera(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (1296, 972)
            file = time.strftime("%Y-%m-%d %H:%M:%S")
            filename = "real_images/" + file + ".jpg"
            camera.capture(filename)

        detector = CrackDectectorLite(filename)    
        (condition, cracks) = detector.predict_tlite_real(filename)[1]
        detector.close()
        self.data.add_scan(time=file, name='scan', condition=condition, cracks=cracks)
        return condition, file
    
    def schedule_scan(self, scan_interval):
        schedule.every(scan_interval).minutes.do(self.scan_camera)
        return_condition = scan_camera()[0]
        return_filename = scan_camera()[1]
        
        while True:
            schedule.run_pending()
            condition, cracks = return_condition
            #print('schedule check condition: ', condition)
            file = return_filename
            scan_time = file                       
            self.data.add_scan(time=scan_time, name='schedule_scan', condition=condition, cracks=cracks)
            if condition == True:
                self.send_alert(file)                
            time.sleep(5)
