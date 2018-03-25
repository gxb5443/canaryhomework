from app import app, db
from sqlalchemy.sql import func
from flask_migrate import Migrate
from sqlalchemy.orm import validates

migrate = Migrate(app, db)


class SensorSample(db.Model):
    __tablename__ = 'sensor_samples'

    device_uuid = db.Column(db.String, primary_key=True)
    sensor_type = db.Column(db.String, primary_key=True)
    sensor_value = db.Column(db.Float, primary_key=True)
    sensor_reading_time = db.Column(db.Integer, primary_key=True)

    def __init__(self, device_uuid=None, sensor_type=None, sensor_value=None, sensor_reading_time=None):
        self.device_uuid = device_uuid
        self.sensor_type = sensor_type
        self.sensor_value = sensor_value
        self.sensor_reading_time = sensor_reading_time

    @validates('sensor_type')
    def validate_sensor_type(self, key, sensor_type):
        if not (sensor_type == 'temperature' or sensor_type == 'humidity'):
            raise AssertionError('sensor_type must be "temperature" or "humidity"')
        return sensor_type

    @validates('sensor_value')
    def validate_sensor_value(self, key, sensor_value):
        try:
            sv = float(sensor_value)
            if not (sv <= 100.0 and sv >= 0.0):
                raise AssertionError('sensor_value must be between 0.0 and 100.0')
        except:
            raise AssertionError('sensor_value must be a number')
        return sv

    def __iter__(self):
        return iter([
            ('device_uuid', self.device_uuid),
            ('sensor_type', self.sensor_type),
            ('sensor_value',  self.sensor_value),
            ('sensor_reading_time', self.sensor_reading_time)])

    def serialize(self):
        return {
            'device_uuid': self.device_uuid,
            'sensor_type': self.sensor_type,
            'sensor_value':  self.sensor_value,
            'sensor_reading_time': self.sensor_reading_time
        }
