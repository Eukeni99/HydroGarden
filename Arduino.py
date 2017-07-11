import serial
from time import sleep
import sqlite3
import os.path


def serial_port(no_sensors):
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.sqlite')
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    ard_port = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
    while True:
        data = ard_port.read(ard_port.inWaiting())
        sleep(3)
        # ard_port.flush()
        for row in [x for x in data.split('\r\n') if x != '']:
            values = [x for x in row.split(';') if x != '']
            if len(values) == no_sensors:
                print values
                query = "INSERT INTO sensor_data(sensor_1, sensor_2, pump_on) VALUES({0}, {1}, 0)".format(*values)
                print(query)
                cur.execute(query)
                con.commit()
            else:
                print 'Corrupt data'
