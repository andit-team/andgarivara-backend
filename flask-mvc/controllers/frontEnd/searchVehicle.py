from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps


class SearchVehicle(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        if data["vehicle_type"] and not data["area"]:
            vId = bsonO.ObjectId(data["vehicle_type"])
            dt = SearchVehicleByType(vId)
        elif not data["vehicle_type"] and data["area"]:
            area = bsonO.ObjectId(data["area"])
            dt = SearchVehicleByLocation(area)
        elif not data["vehicle_type"] and not data["area"]:
            dt = SearchVehicleAll()
        else:
            vId = bsonO.ObjectId(data["vehicle_type"])
            area = bsonO.ObjectId(data["area"])
            dt = SearchVehicleFIlter(vId, area)
        return dt


def SearchVehicleByLocation(area):
    try:
        err_msg=None
        dt = mongo.db.vehicles.aggregate(
            [{
                "$match": {
                    "area": area,
                    "del_status": False
                }
            },
                {
                "$lookup": {
                    "from": "vehicle_types",
                    "localField": "vehicle_type",
                    "foreignField": "_id",
                    "as": "vehicle_type_details"
                },

            },
                {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user_details"
                }
            },
                {
                "$lookup": {
                    "from": "locationCity",
                    "localField": "city",
                    "foreignField": "_id",
                    "as": "city_details"
                }
            },
                {
                "$lookup": {
                    "from": "locationArea",
                    "localField": "area",
                    "foreignField": "_id",
                    "as": "area_details"
                }
            }
            ])
        msg = "SUCCESS"
        error = False
    except Exception as ex:
        msg = "FAILED"
        error = True
        err_msg=ex
    return jsonify({
        "msg": msg,
        "error": error,
        "err_msg" : str(err_msg),
        "data": json.loads(dumps(dt))
    })


def SearchVehicleByType(vId):
    try:
        err_msg=None
        dt = mongo.db.vehicles.aggregate(
            [{
                "$match": {
                    "vehicle_type": vId,
                    "del_status": False
                }
            },
                {
                "$lookup": {
                    "from": "vehicle_types",
                    "localField": "vehicle_type",
                    "foreignField": "_id",
                    "as": "vehicle_type_details"
                },

            },
                {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user_details"
                }
            },
                {
                "$lookup": {
                    "from": "locationCity",
                    "localField": "city",
                    "foreignField": "_id",
                    "as": "city_details"
                }
            },
                {
                "$lookup": {
                    "from": "locationArea",
                    "localField": "area",
                    "foreignField": "_id",
                    "as": "area_details"
                }
            }
            ])
        msg = "SUCCESS"
        error = False
    except Exception as ex:
        msg = "FAILED"
        error = True
        err_msg=ex
    return jsonify({
        "msg": msg,
        "error": error,
        "err_msg" : str(err_msg),
        "data": json.loads(dumps(dt))
    })


def SearchVehicleFIlter(vId, area):
    try:
        err_msg=None
        dt = mongo.db.vehicles.aggregate(
            [{
                "$match": {
                    "vehicle_type": vId,
                    "area": area,
                    "del_status": False
                }
            },
                {
                "$lookup": {
                    "from": "vehicle_types",
                    "localField": "vehicle_type",
                    "foreignField": "_id",
                    "as": "vehicle_type_details"
                },

            },
                {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user_details"
                }
            },
                {
                "$lookup": {
                    "from": "locationCity",
                    "localField": "city",
                    "foreignField": "_id",
                    "as": "city_details"
                }
            },
                {
                "$lookup": {
                    "from": "locationArea",
                    "localField": "area",
                    "foreignField": "_id",
                    "as": "area_details"
                }
            }
            ])

        msg = "SUCCESS"
        error = False
    except Exception as ex:
        msg = "FAILED"
        error = True
        err_msg=ex
    return jsonify({
        "msg": msg,
        "error": error,
        "err_msg" : str(err_msg),
        "data": json.loads(dumps(dt))
    })


def SearchVehicleAll():
    try:
        err_msg=None
        dt = mongo.db.vehicles.aggregate(
            [{
                "$match": {
                    "del_status": False
                }
            },
                {
                "$lookup": {
                    "from": "vehicle_types",
                    "localField": "vehicle_type",
                    "foreignField": "_id",
                    "as": "vehicle_type_details"
                },

            },
                {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user_details"
                }
            },
                {
                "$lookup": {
                    "from": "locationCity",
                    "localField": "city",
                    "foreignField": "_id",
                    "as": "city_details"
                }
            },
                {
                "$lookup": {
                    "from": "locationArea",
                    "localField": "area",
                    "foreignField": "_id",
                    "as": "area_details"
                }
            }
            ])
        msg = "SUCCESS"
        error = False
    except Exception as ex:
        msg = "FAILED"
        error = True
        err_msg=ex
    return jsonify({
        "msg": msg,
        "error": error,
        "err_msg" : str(err_msg),
        "data": json.loads(dumps(dt))
    })
