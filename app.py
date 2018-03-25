import os
from flask import Flask,jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import json
from invalid_usage import InvalidUsage


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from models import SensorSample

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/sample', methods=['PUT'])
def addSample():
    content = request.get_json()
    device_uuid = content.get('device_uuid')
    sensor_type = content.get('sensor_type')
    sensor_value = content.get('sensor_value')
    sensor_reading_time = content.get('sensor_reading_time')

    if device_uuid is None:
        raise InvalidUsage("Requires device_uuid")
    if sensor_type is None:
        raise InvalidUsage("Requires sensor_type")
    if sensor_value is None:
        raise InvalidUsage("Requires sensor_value")
    if sensor_reading_time is None:
        raise InvalidUsage("Requires sensor_reading_time")

    app.logger.info(content)
    app.logger.info(sensor_value)
    try:
        sample = SensorSample(device_uuid = device_uuid, sensor_type = sensor_type, sensor_value = sensor_value, sensor_reading_time = sensor_reading_time)
        db.session.add(sample)
        db.session.flush()
        db.session.commit()
    except AssertionError as exception_message:
        raise InvalidUsage(str(exception_message))

    return jsonify(sample.serialize())

if __name__ == '__main__':
    app.run(host='0.0.0.0')
