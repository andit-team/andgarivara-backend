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
        try:
            dtLocation = mongo.db.locationCity.find({})
            dtVT = mongo.db.vehicle_types.find({})
            msg = "SUCCESS"
            error = False
        except:
            msg = "FAILED"
            error = True
        return dt


def SearchVehicleByLocation(city):
    try:
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
    except:
        msg = "FAILED"
        error = True
    return jsonify({
        "msg": msg,
        "error": error,
        "data": json.loads(dumps(dt))
    })


def SearchVehicleByType(vId):
    try:
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
    except:
        msg = "FAILED"
        error = True
    return jsonify({
        "msg": msg,
        "error": error,
        "data": json.loads(dumps(dt))
    })


def SearchVehicleFIlter(vId, city):
    try:
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
    except:
        msg = "FAILED"
        error = True
    return jsonify({
        "msg": msg,
        "error": error,
        "data": json.loads(dumps(dt))
    })


def SearchVehicleAll():
    try:
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
    except:
        msg = "FAILED"
        error = True
    return jsonify({
        "msg": msg,
        "error": error,
        "data": json.loads(dumps(dt))
    })
