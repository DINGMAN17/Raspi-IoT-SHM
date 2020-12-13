import smbus
import datetime
import time
import database

class Sensor():
    def __init__(self, sensor_interval):
        self.address = 0x48
        self.bus = smbus.SMBus(1)
        self.cmd = 0x40
        self.data = database.SensorData()
        self.sensor_interval = sensor_interval
        
    def add_sensor(self, name, sensor_type, channel):
        self.data.define_sensors(name, sensor_type, channel)
        
    def analogRead(self, chn):
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
        

def main():
    print ('Program is starting ... ')
    try:
        monitoring = Sensor()
        monitoring.log_data()
        
    except KeyboardInterrupt:
        monitoring.destroy()

if __name__ == '__main__':
    main()
        
    
