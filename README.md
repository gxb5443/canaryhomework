# Canary Homework
## Overview
### Design
I originally designed this with the understanding that the focus was on the API
and code design so I chose python and flask because of it's friendly structure,
however with the limited number of required endpoints this design may be slightly
overkill. The system consists of three docker containers: nginx, python, and postgres.
Nginx fields and buffers the HTTP request/reponses, postgres is the storage medium,
and the python container runs the application. There are two docker networks to isolate
the database from the gateway server, with the application in the middle.

The application itself consists of two main files: the app.py file and the models.py.
The models script. The models script contains the definition for the SensorSample object
which represents a sensor bundle. The model contains much of the necessary validation and
handles most of the communication with the database via SQLAlchemy. The app.py script
contains all the endpoints. There is third file which just contains a simple object defintion
used to represent a standard response to a malformed PUT request payload.

I worked out the design
and built the application before I realized there was a limitation on using an
application server so mine does include gunicorn, because the focus of our in-person
meeting seemed to be on API design rather than performance optimization with lower-level
concurrent, and didn't have time to rewrite it. Had I realized the focus was on concurrency and peformance I would
have rather built this application in Golang without a big HTTP framework like flask and
rather just use the built-in HTTP server, but for API design python+flask was faster.

## Operation
This project includes a docker-compose.yml file which spins up several docker
containers hosting the application and it's required resources. To run the application,
all you need is docker and docker-compose installed on your machine. Once you
have those, you can just run:
```
$ docker-compose up
```

## API
The API is a simple HTTP API.

| Endpoint | HTTP Method | Expected Response                                            | Details |
| -------- | ----------- | -----------------                                            | ------- |  
| /samples | GET         | JSON object containing the array of bundles in JSON format and a 200 HTTP Code   | The /samples GET endpoint will return all bundles available. Clients can add query parameters for device_uuid, sensor_type, start_times, and end_times. start_times and end_times are both required, but the time, device_uuid, and sensor_types are each optional. |
| /samples | PUT         | JSON object containing the newly INSERTed object and a 200 HTTP Code | The backend requires all the fields to be filled and it will enforce all the specs of the object, otherwise returning a JSON object with the error message of what's wrong along with an HTTP code of 400 |

## Contributors
* **Gian Biondi** <gianbiondijr@gmail.com>
