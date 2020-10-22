from peewee import *

db = SqliteDatabase('sensor_data.db')

#Define data model classes that inherit from the PEEWEE ORM model class
class Sensor(Model):
    name = CharField()
    sensor_type = CharField()
    channel = IntegerField()
    
    class Meta:
        database = db
        
class SensorReading(Model):
    time = DateTimeField()
    name = CharField()
    value = FloatField()
     
    class Meta:
        database = db
        
class Scan(Model):
    time = DateTimeField()
    name = CharField()
    condition = BooleanField()
    cracks = IntegerField()
    
    class Meta:
        database = db
        
class SensorData(object):
    '''Main data access layer class which provides functions to query sensor types
    and sensor reading data from database.
    '''
    
    def __init__(self):
        #connect to database
        db.connect()
        db.create_tables([Sensor, SensorReading, Scan], safe=True)
    
    def define_sensors(self, name, sensor_type, channel):
        '''define each sensor and add them to the database. If a sensor of the same
        name, type, and channel exists, nothing will be added
        '''
        Sensor.get_or_create(name=name, sensor_type=sensor_type, channel=channel)
        
    def get_sensors(self):
        '''Return a list of all the sensors defined in the database'''
        return Sensor.select()
    
    def get_recent_readings(self, name, limit=20):
        '''Return a list of the most recent sensor readings with the specified name,
        in descending time order, by default, returns the last 20 readings'''
        return SensorReading.select() \
                            .where(SensorReading.name==name) \
                            .order_by(SensorReading.time.desc()) \
                            .limit(limit)
    
    def get_critical_readings(self, name, maximum=50, limit=20):
        '''Return a list of the most recent sensor readings with the specified name,
        in descending time order, by default, returns the last 20 readings'''
        return SensorReading.select() \
                            .where(SensorReading.name==name) \
                            .where(SensorReading.value > maximum) \
                            .order_by(SensorReading.value.desc()) \
                            .limit(limit)
    
    def get_daily_average(self, name, limit=20):
        '''Return a list of the daily average readings with the specified name,
        in descending time order, by default, returns the last 20 readings'''
        return SensorReading.select(fn.date_trunc('day', SensorReading.time).alias('day'), fn.avg(SensorReading.value).alias('avg')) \
                            .where(SensorReading.name==name) \
                            .group_by(fn.date_trunc('day', SensorReading.time)) \
                            .order_by(fn.date_trunc('day', SensorReading.time).desc()) \
                            .limit(limit)
    
    def get_scan_status(self):
        '''Return the most recent scan result:
        condition: boolean
        number of cracks: integer'''
        result = ''        
        d = Scan.select() \
                .order_by(Scan.time.desc()) \
                .limit(1)
        for item in d:
            result += str(item.condition)
        return result
    
    def get_scan_time(self):
        time = ''
        d = Scan.select() \
                .order_by(Scan.time.desc()) \
                .limit(1)
        for item in d:
            time += str(item.time)[:19]
        return time
    
    def get_scan_file(self):
        file = '/static/scan_image/out_'+ self.get_scan_time()+ '.png'
        return file
    
    def add_reading(self, time, name, value):
        SensorReading.create(time=time, name=name, value=value)
        
    def add_scan(self, time, name, condition, cracks):
        Scan.create(time=time, name=name, condition=condition, cracks=cracks)
        
    def close(self):
        db.close()
