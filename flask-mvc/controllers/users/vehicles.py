from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps


class AddVehicle(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        flag = insertData(data)
        if flag == True:
            msg = "SUCCESS"
            error = False
        else:
            msg = "FAILED"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })


def insertData(data):
    userId = bsonO.ObjectId(data["user_id"])
    dt = {
        "user_id": userId,
        "title": data["title"],
        "vehicle_type": bsonO.ObjectId(data["vehicle_type"]),
        "description": data["description"],
        "country": data["country"],
        "city": data["city"],
        "car_location": data["car_location"],
        "total_seat": data["total_seat"],
        "min_price_per_day": data["min_price_per_day"],
        "cover_img": data["cover_img"],
        "brand": data["brand"],
        "model": data["model"],
        "year_of_manufacture": data["year_of_manufacture"],
        "color": data["color"],
        "ac": data["ac"],
        "vehicle_imgs": [

        ],
        "del_status": False,
        "create_date": str(datetime.datetime.now())
    }
    try:
        ins = mongo.db.vehicles.insert(dt)
        return True
    except:
        return False


class UserVehicleList(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        try:
            dt = mongo.db.vehicles.aggregate(
                [{
                    "$match": {
                        "user_id": bsonO.ObjectId(data["user_id"]),
                        "del_satus": False
                    }
                },
                    {
                    "$lookup": {
                        "from": "vehicle_types",
                        "localField": "vehicle_type",
                        "foreignField": "_id",
                        "as": "vehicle_type_details"
                    }
                },
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


class EditVehicle(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        flag = UpdateVehicleInfo(data)
        if flag == True:
            msg = "SUCCESS"
            error = False
        else:
            msg = "FAILED"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })


class DeleteVehicle(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        try:
            update_ = mongo.db.vehicles.update(
                {
                    "_id": bsonO.ObjectId(data["_id"])
                },
                {
                    "$set": {
                        "del_satus": True,
                        "del_resone": data["del_resone"],
                        "del_date": str(datetime.datetime.now())
                    }
                }
            )
            msg = "SUCCESS"
            error = False
        except:
            msg = "FAILED"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": None
        })


def UpdateVehicleInfo(data):
    userId = bsonO.ObjectId(data["user_id"])
    try:
        update_ = mongo.db.vehicles.update(
            {
                "_id": bsonO.ObjectId(data["_id"])
            },
            {
                "$set": {
                    "user_id": userId,
                    "title": data["title"],
                    "vehicle_type": bsonO.ObjectId(data["vehicle_type"]),
                    "description": data["description"],
                    "country": data["country"],
                    "city": data["city"],
                    "car_location": data["car_location"],
                    "total_seat": data["total_seat"],
                    "min_price_per_day": data["min_price_per_day"],
                    "cover_img": data["cover_img"],
                    "brand": data["brand"],
                    "model": data["model"],
                    "year_of_manufacture": data["year_of_manufacture"],
                    "color": data["color"],
                    "ac": data["ac"],
                    "vehicle_imgs": [

                    ],
                    "update_date": str(datetime.datetime.now())
                }
            }
        )
        return True
    except:
        return False
