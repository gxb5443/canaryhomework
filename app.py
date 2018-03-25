import os
from flask import Flask, jsonify, request, make_response
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

    try:
        sample = SensorSample(device_uuid=device_uuid, sensor_type=sensor_type,
                              sensor_value=sensor_value, sensor_reading_time=sensor_reading_time)
        db.session.add(sample)
        db.session.flush()
        db.session.commit()
    except AssertionError as exception_message:
        raise InvalidUsage(str(exception_message))

    return jsonify(sample.serialize())


@app.route('/samples', methods=['GET'])
def getSamplesForID():
    device_uuid = request.args.get('device_uuid')
    sensor_type = request.args.get('sensor_type')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    bundle_query = db.session.query(SensorSample)

    if device_uuid is not None:
        bundle_query = bundle_query.filter(
            SensorSample.device_uuid == device_uuid)

    if sensor_type is not None:
        bundle_query = bundle_query.filter(
            SensorSample.sensor_type == sensor_type)

    if start_time is not None and end_time is not None:
        bundle_query = bundle_query.filter(
            SensorSample.sensor_reading_time.between(start_time, end_time))

    results = bundle_query.all()

    return jsonify(bundles=[r.serialize() for r in results])


if __name__ == '__main__':
    app.run(host='0.0.0.0')
