from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView
import database

app = Flask(__name__)
app.config['SECRET_KEY'] = '0000'
app.config['DATABASE'] = database.SensorData()

admin = Admin(app, name='Sensors', template_mode='bootstrap3', url='/')
admin.add_view(ModelView(database.Sensor))
admin.add_view(ModelView(database.Scan))
admin.add_view(ModelView(database.SensorReading))
