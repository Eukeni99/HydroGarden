from flask_sqlalchemy import SQLAlchemy
from Helpers import resolve_data
from datetime import date, datetime

db = SQLAlchemy()


class SensorData(db.Model):
    __tablename__ = 'sensor_data'
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.Date, nullable=False, default=date.today)
    time_created = db.Column(db.Time, nullable=False, default=lambda: datetime.now().time())
    sensor_1 = db.Column(db.Float)
    sensor_2 = db.Column(db.Float)
    sensor_3 = db.Column(db.Float)
    sensor_4 = db.Column(db.Float)
    sensor_5 = db.Column(db.Float)
    sensor_6 = db.Column(db.Float)
    pump_on = db.Column(db.Boolean)

    def __init__(self, date_created,time_created,sensor_1, sensor_2, sensor_3, sensor_4, sensor_5, sensor_6, pump_on):
        self.date_created = date_created
        self.time_created = time_created
        self.sensor_1 = sensor_1
        self.sensor_2 = sensor_2
        self.sensor_3 = sensor_3
        self.sensor_4 = sensor_4
        self.sensor_5 = sensor_5
        self.sensor_6 = sensor_6
        self.pump_on = pump_on

    def to_json(self):
        return {key: resolve_data(self.__dict__[key]) for key in self.__dict__ if not key.startswith('_')}

    def __repr__(self):
        return 'SensorData: {}'.format(self.id)

    def __str__(self):
        return 'SensorData: {}'.format(self.id)


class CustomSensor(db.Model):
    __tablename__ = 'custom_sensor'
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.Date, nullable=False, default=date.today)
    time_created = db.Column(db.Time, nullable=False, default=lambda: datetime.now().time())
    name = db.Column(db.String(20), nullable=False)
    sensor_field = db.Column(db.String(10), unique=True, nullable=False)
    formula = db.Column(db.String(50))
    data_type = db.Column(db.Integer, nullable=False)

    def __init__(self, date_created, time_created, name, sensor_field, formula, data_type):
        self.date_created = date_created
        self.time_created = time_created
        self.name = name
        self.sensor_field = sensor_field
        self.formula = formula
        self.data_type = data_type

    def to_json(self):
        return {key: resolve_data(self.__dict__[key]) for key in self.__dict__ if not key.startswith('_')}

    def __repr__(self):
        return 'CustomSensor: {}, {} -> {} '.format(self.id, self.sensor_field, self.name)

    def __str__(self):
        return 'CustomSensor: {}, {} -> {} '.format(self.id, self.sensor_field, self.name)
