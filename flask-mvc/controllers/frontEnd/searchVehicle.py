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
        if data["vehicle_type"] and not data["city"]:
            vId = bsonO.ObjectId(data["vehicle_type"])
            dt = SearchVehicleByType(vId)
        elif not data["vehicle_type"] and data["city"]:
            city = bsonO.ObjectId(data["city"])
            dt = SearchVehicleByLocation(city)
        elif not data["vehicle_type"] and not data["city"]:
            dt = SearchVehicleAll()
        else:
            vId = bsonO.ObjectId(data["vehicle_type"])
            city = bsonO.ObjectId(data["city"])
            dt = SearchVehicleFIlter(vId, city)
        return dt


def SearchVehicleByLocation(city):
    try:
        err_msg=None
        dt = mongo.db.vehicles.aggregate(
            [{
                "$match": {
                    "city": city,
                    "del_satus": False
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
                    "as": "location_details"
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
                    "del_satus": False
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
                    "as": "location_details"
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


def SearchVehicleFIlter(vId, city):
    try:
        err_msg=None
        dt = mongo.db.vehicles.aggregate(
            [{
                "$match": {
                    "vehicle_type": vId,
                    "city": city,
                    "del_satus": False
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
                    "as": "location_details"
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
                    "del_satus": False
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
                    "as": "location_details"
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
