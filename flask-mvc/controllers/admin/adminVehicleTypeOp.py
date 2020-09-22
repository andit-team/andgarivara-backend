
from bson.json_util import dumps
from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import datetime
import bson
import json


class AddVehicleType(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        dt = {
            "title": data["title"],
            "create_date": datetime.datetime.now()
        }
        try:
            insD = mongo.db.vehicle_types.insert_one(dt)
            msg = "SUCCESSFULL"
            error = False
        except:
            msg = "Failed"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })


class EditVehicleType(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()

        try:
            insD = mongo.db.vehicle_types.update_one(
                {
                    "_id": bson.ObjectId(data["_id"])
                },
                {
                    "$set": {
                        "title": data["title"],
                        "Update_date": datetime.datetime.now()
                    }
                }
            )
            msg = "SUCCESSFULL"
            error = False
        except:
            msg = "Failed"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })


class DeleteVehicleType(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        dt = {
            "_id": bson.ObjectId(data["_id"])
        }
        try:
            delD = mongo.db.vehicle_types.delete_one(dt)
            msg = "SUCCESSFULL"
            error = False
        except:
            msg = "Failed"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })


class VehicleTypeList(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        try:
            dt = mongo.db.vehicle_types.find({})
            msg = "SUCCESSFULL"
            error = False
        except:
            msg = "Failed"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dt))
        })
