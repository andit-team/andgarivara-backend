from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps


class AddVehicleAdmin(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        flag = insertData(data)
        return flag


def insertData(data):
    userId = bsonO.ObjectId(data["user_id"])
    err_msg=None
    dt = {
        "user_id": userId,
        "title": data["title"],
        "vehicle_type": bsonO.ObjectId(data["vehicle_type"]),
        "description": data["description"],
        "country": data["country"],
        "city": bsonO.ObjectId(data["city"]),
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
        "create_date": datetime.datetime.now()
    }
    try:
        ins = mongo.db.vehicles.insert(dt)
        msg = "SUCCESS"
        error = False
    except Exception as ex:
        msg = "FAILED"
        error = True
        err_msg=ex
        dt = None
    return jsonify({
        "msg": msg,
        "error": error,
        "err_msg" : str(err_msg),
        "data": json.loads(dumps(dt))
    })


class AdminVehicleList(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        err_msg=None
        try:
            dt = mongo.db.vehicles.aggregate(
                [
                    {
                        "$lookup": {
                            "from": "vehicle_types",
                            "localField": "vehicle_type",
                            "foreignField": "_id",
                            "as": "vehicle_type_details"
                        }
                    }
                ])
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = "FAILED"
            error = True
            err_msg=ex
            dt = None
        return jsonify({
            "msg": msg,
            "error": error,
            "err_msg" : str(err_msg),
            "data": json.loads(dumps(dt))
        })


class EditVehicleAdmin(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        flag = UpdateVehicleInfo(data)
        return flag


class DeleteVehicleAdmin(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        err_msg=None
        try:
            update_ = mongo.db.vehicles.update(
                {
                    "_id": bsonO.ObjectId(data["_id"])
                },
                {
                    "$set": {
                        "del_status": True,
                        "del_resone": "Deleted By Admin",
                        "del_date": datetime.datetime.now()
                    }
                }
            )
            msg = "SUCCESSFULL"
            error = False
        except Exception as ex:
            msg = "FAILED"
            error = True
            err_msg=ex
        return jsonify({
            "msg": msg,
            "error": error,
            "err_msg" : str(err_msg),
            "data": json.loads(dumps(data))
        })


def UpdateVehicleInfo(data):
    userId = bsonO.ObjectId(data["user_id"])
    err_msg=None
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
                    "city":  bsonO.ObjectId(data["city"]),
                    "car_location": data["car_location"],
                    "total_seat": data["total_seat"],
                    "min_price_per_day": data["min_price_per_day"],
                    "cover_img": data["cover_img"],
                    "brand": data["brand"],
                    "model": data["model"],
                    "year_of_manufacture": data["year_of_manufacture"],
                    "color": data["color"],
                    "ac": data["ac"],
                    "vehicle_imgs":data["vehicle_imgs"],
                    "update_date": datetime.datetime.now()
                }
            }
        )
        msg = "SUCCESSFULL"
        error = False
    except Exception as ex:
        msg = "SUCCESS"
        error = True
        err_msg=ex
    return jsonify({
        "msg": msg,
        "error": error,
        "err_msg" : str(err_msg),
        "data": json.loads(dumps(data))
    })
