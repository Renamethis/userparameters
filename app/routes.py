from flasgger import Swagger
from flask import jsonify, abort, request
from .tasks import *
from . import app

# Swagger configuration
swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'api',
            "route": '/api',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs/"
}

# Swagger template configuration
template = {
  "swagger": "2.0",
  "info": {
    "title": "User Parameters API",
    "description": "API for managing a database of users and their parameters",
    "contact": {
      "responsibleOrganization": "Ivan Gavrilov",
      "responsibleDeveloper": "Ivan Gavrilov",
      "email": "enderjoin@gmail.com",
    },
    "version": "0.0.1"
  },
}

swagger = Swagger(app, config=swagger_config, template=template)

# Users endpoints
@app.route("/users/<username>", methods=["POST"])
def add_user(username):
    """Endpoint which adds user in database
    ---
    tags:
      - Users
    parameters:
      - name: username
        in: path
        type: string
        required: true
        description: The username of given user
    responses:
      200:
        description: User successfully created
      409:
        description: User already exists
    """
    task = add_user_task.delay(username)
    result = task.wait(timeout=None)
    if result is None:
        abort(409)
    return jsonify(result), 200

@app.route("/users/<username>", methods=["DELETE"])
def delete_user(username):
    """Endpoint which deletes user from database
    ---
    tags:
      - Users
    parameters:
      - name: username
        in: path
        type: string
        required: true
        description: The username of given user
    responses:
      200:
        description: User successfully deleted
      404:
        description: User not found
    """
    task = delete_user_task.delay(username)
    result = task.wait(timeout=None)
    if result is None:
        abort(400)
    return jsonify({'status': 'OK'}), 200

@app.route("/users", methods=["GET"])
def get_users():
    """Endpoint which returns list of all users
    ---
    tags:
      - Users
    responses:
      200:
        description: List of all users
    """
    task = get_users_task.delay()
    result = task.wait(timeout=None)
    return jsonify(result), 200

# Parameters endpoints
@app.route("/api/parameters/<username>/<name>/<type>", methods=["POST"])
def set_parameter(username, name, type):
    """Endpoint which creates or updates user parameter
    ---
    tags:
      - Parameters
    parameters:
      - name: username
        in: path
        type: string
        required: true
        description: The username of given user
      - name: name
        in: path
        type: string
        required: true
        description: The name of given parameter
      - name: type
        in: path
        type: string
        required: true
        enum: ['str', 'int']
        default: 'str'
        description: The type of given parameter
      - name: value
        in: formData
        type: string
        required: true
        description: The value of given parameter
    responses:
      200:
        description: All parameters of given user
      400:
        description: Value for given type is incorrect
      404:
        description: User not found
    """
    task = set_parameter_task.delay(username, name, type, 
                                    request.form.get('value'))
    result = task.wait(timeout=None)
    if(result != 200):
      abort(result)
    return jsonify({'status': 'OK'}), 200

@app.route("/api/parameters/<username>/<name>/<type>", methods=["GET"])
def get_parameter(username, name, type):
    """Endpoint which returns given parameter
    ---
    tags:
      - Parameters
    parameters:
      - name: username
        in: path
        type: string
        required: true
        description: The username of given user
      - name: name
        in: path
        type: string
        required: true
        description: The name of given parameter
      - name: type
        in: path
        type: string
        required: true
        enum: ['str', 'int']
        default: 'str'
        description: The type of given parameter
    responses:
      200:
        description: Parameter entry
      404:
        description: User or parameter not found
    """
    task = get_parameter_task.delay(username, name, type)
    result = task.wait(timeout=None)
    if result is None:
        abort(404)
    return jsonify(result), 200

@app.route("/api/parameters/<username>", methods=["GET"])
def get_parameters(username):
    """Endpoint which returns all user parameters
    ---
    tags:
      - Parameters
    parameters:
      - name: username
        in: path
        type: string
        required: true
        description: The username of given user
    responses:
      200:
        description: All parameters of given user
      404:
        description: User parameters not found
    """
    task = get_parameters_task.delay(username)
    result = task.wait(timeout=None)
    if result is None:
        abort(404)
    return jsonify(result), 200

# JSON operation endpoint
@app.route("/api/<username>", methods=["POST"])
def json_set(username):
    """Endpoint set up parameter with JSON 
    ---
    tags:
      - JSON
    consumes:
      - application/json
    parameters:
      - name: username
        in: path
        type: string
        required: true
        description: The username of given user
      - name: data
        in: body
        schema:
          type: object
          required:
            - Operation
            - Name
            - Type
            - Value
          properties:
            Operation:
              type: string
            Name:
              type: string
            Type:
              type: string
            Value:
              type: string
        description: Parameter entry in JSON format
    responses:
      200:
        description: Response sucessfully returned
    """
    body = request.json
    response = body.copy()
    del response['Value']
    if(body['Operation'] == 'SetParam'):
      task = set_parameter_task.delay(username, body['Name'], body['Type'], 
                                      body['Value'])
      result = task.wait(timeout=None)
      if(result != 200):
        response['Status'] = 'ERROR'
      else:
        response['Status'] = 'OK'
    else:
      response['Status'] = 'ERROR'
    return response