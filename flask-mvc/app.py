# import flask library------------------
from flask import Flask, app, jsonify
from flask_cors import CORS
from flask_restful import Api
from extension import mongo
from routes.api import create_routes
from flask_jwt_extended import JWTManager
# from flask_socketio import SocketIO


def create_app(config_object='settings'):
    flask_app = Flask(__name__)
    CORS(flask_app)
    cors = CORS(flask_app, resources={
        r"/*":{
        "origins": "*",
        "methods": ["OPTIONS", "GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Authorization", "Content-Type"]
        }
    })

    flask_app.config.from_object(config_object)
    mongo.init_app(flask_app)

    api = Api(app=flask_app)


    # init jwt manager
    jwt = JWTManager(app=flask_app)
    create_routes(api=api)

    return flask_app


if __name__ == '__main__':
    # Main entry point when run in stand-alone mode.
    app = create_app()
    # socketio = SocketIO(app)
    # socketio.run(app,debug=True, host='0.0.0.0')
    app.run(debug=True, host='0.0.0.0')
