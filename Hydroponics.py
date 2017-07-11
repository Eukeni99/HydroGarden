from flask import Flask, render_template, request, Response
from Models import db, SensorData, CustomSensor
from flask.json import jsonify
from Arduino import serial_port
from threading import Thread
from Helpers import search_sensor
from Constants import DataTypes
import os.path


db_path = os.path.join('sqlite://', os.path.dirname(os.path.abspath(__file__)), 'database.sqlite')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/eukeni/PycharmProjects/Hydroponics/database.sqlite'
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/query', methods=['GET'])
def query():
    headers = dict()
    cs = CustomSensor.query.all()
    sensors = [name for name in dir(SensorData) if name.startswith('sensor_')]
    for sensor in sensors:
        row = search_sensor(sensor, cs)
        if row is None:
            headers[sensor] = sensor
        else:
            headers[sensor] = row.name
    data = [x.to_json() for x in SensorData.query.all()]
    return jsonify(data=data, headers=headers)


@app.route('/api/get_custom_sensor', methods=['GET'])
def get_custom_sensors():
    return_list = list()
    data = CustomSensor.query.all()
    sensors = [name for name in dir(SensorData) if name.startswith('sensor_')]
    for sensor in sensors:
        row = search_sensor(sensor, data)
        if row is None:
            return_list.append(dict(name='', formula='', data_type=0, sensor_field=sensor))
        else:
            return_list.append(dict(name=row.name, data_type=row.data_type, formula=row.formula, sensor_field=row.sensor_field))
    return jsonify(sensors=return_list)


@app.route('/api/get_available_sensors', methods=['GET'])
def get_available_sensors():
    data = [name for name in dir(SensorData) if name.startswith('sensor_')]
    return jsonify(sensors=data)


@app.route('/api/save_custom_sensors', methods=['POST'])
def save_custom_sensors():
    data = request.get_json()
    sensors = CustomSensor.query.all()
    for sensor in data:
        row = search_sensor(sensor['sensor_field'], sensors)
        if row is None:
            cs = CustomSensor(None, None, sensor['name'], sensor['sensor_field'], sensor['formula'], sensor['data_type'])
            db.session.add(cs)
        else:
            row.name = sensor['name']
            row.formula = sensor['formula']
            row.data_type = sensor['data_type']
    db.session.commit()
    return Response(status=200)


@app.route('/api/get_data_types', methods=['GET'])
def get_data_types():
    return jsonify(types=[dict(name=key.title(), value=DataTypes.__dict__[key]) for key in DataTypes.__dict__ if not key.startswith('__')])


if __name__ == '__main__':
    t = Thread(target=serial_port, args=(2, ))
    t.daemon = False
    # t.start()
    app.run()

