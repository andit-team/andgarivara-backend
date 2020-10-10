from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps


class GetAreas(Resource):
    @staticmethod
    def get() -> Response:
        try:
            dt = mongo.db.locationArea.find({}, {"_id": 1, "area": 1})
            msg = "SUCCESS"
            error = False
        except:
            msg = "FAILED"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dt))
        })


class GetCities(Resource):
    @staticmethod
    def get() -> Response:
        try:
            dt = mongo.db.locationCity.find({}, {"_id": 1, "city": 1})
            msg = "SUCCESS"
            error = False
        except:
            msg = "FAILED"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dt))
        })


class GetVehicleType(Resource):
    @staticmethod
    def get() -> Response:
        try:
            dt = mongo.db.vehicle_types.find({}, {"_id": 1, "title": 1})
            msg = "SUCCESS"
            error = False
        except:
            msg = "FAILED"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dt))
        })


class GetUserList(Resource):
    @staticmethod
    def get() -> Response:
        try:
            dt = mongo.db.users.find(
                {"del_status": False}, {"_id": 1, "f_name": 1, "l_name": 1})
            msg = "SUCCESS"
            error = False
        except:
            msg = "FAILED"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dt))
        })
