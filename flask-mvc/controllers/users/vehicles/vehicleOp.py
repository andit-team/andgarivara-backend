from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps
from flask_jwt_extended import jwt_required, get_jwt_identity

class AddVehicle(Resource):
    @staticmethod
    @jwt_required
    def post() -> Response:
        data = request.get_json()
        flag = insertData(data)
        return flag


def insertData(data):
    userId = bsonO.ObjectId(get_jwt_identity())
    vehicelTypeId = bsonO.ObjectId(data["vehicle_type"])
    dt = {
        "user_id": userId,
        "vehicle_type": bsonO.ObjectId(data["vehicle_type"]),
        "description": data["description"],
        "country": data["country"],
        "city": bsonO.ObjectId(data["city"]),
        "area":  bsonO.ObjectId(data["area"]),
        "car_location": data["car_location"],
        "cover_img": data["cover_img"],
        "brand": data["brand"],
        "model": data["model"],
        "year_of_manufacture": data["year_of_manufacture"],
        "vehicle_imgs": data["vehicle_imgs"],
        "del_status": False,
        "create_date": datetime.datetime.now()
    }
    fieldData = GetDataFields(vehicelTypeId)
    if fieldData != None:
        for key, value in fieldData.items():
            for valueData in value:
                txt = valueData["field_label"]
                dt[txt] = data[txt]
    try:
        ins = mongo.db.vehicles.insert(dt)
        statusChange = mongo.db.userRegister.update(
            {
                "_id":userId
            },
            {
                "$addToSet": {
                    "role":"owner"
                }
            }
        )
        msg = "SUCCESS"
        error = False
    except Exception as ex:
        msg = str(ex)
        error = True
        err_msg = ex
        dt = None
    return jsonify({
        "msg": msg,
        "error": error,
        "data": json.loads(dumps(dt))
    })

class EditVehicle(Resource):
    @staticmethod
    @jwt_required
    def put() -> Response:
        data = request.get_json()
        userId = bsonO.ObjectId(get_jwt_identity())
        vehicelTypeId = bsonO.ObjectId(data["vehicle_type"])
        dt = {
            "user_id": userId,
            "vehicle_type": bsonO.ObjectId(data["vehicle_type"]),
            "description": data["description"],
            "country": data["country"],
            "city": bsonO.ObjectId(data["city"]),
            "area":  bsonO.ObjectId(data["area"]),
            "car_location": data["car_location"],
            "cover_img": data["cover_img"],
            "brand": data["brand"],
            "model": data["model"],
            "year_of_manufacture": data["year_of_manufacture"],
            "vehicle_imgs": data["vehicle_imgs"],
            "del_status": False,
            "update_date": datetime.datetime.now()
        }
        fieldData = GetDataFields(vehicelTypeId)
        if fieldData != None:
            for key, value in fieldData.items():
                for valueData in value:
                    txt = valueData["field_label"]
                    dt[txt] = data[txt]
        try:
            update_ = mongo.db.vehicles.update(
                {
                    "_id": bsonO.ObjectId(data["_id"])
                },
                {
                    "$set": dt
                }
            )
            msg = "SUCCESSFULL"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })
class UserVehicleList(Resource):
    @staticmethod
    @jwt_required
    def post() -> Response:
        data = request.get_json()
        current_user = bsonO.ObjectId(get_jwt_identity())
        try:
            dt = mongo.db.vehicles.aggregate(
                [{
                    "$match": {
                        "user_id": current_user,
                        "del_status": False
                    }
                },
                {
                    "$lookup": {
                        "from": "vehicleType",
                        "localField": "vehicle_type",
                        "foreignField": "_id",
                        "as": "vehicle_type_details"
                    },
                },
                {
                    "$lookup": {
                        "from": "cities",
                        "localField": "city",
                        "foreignField": "_id",
                        "as": "city_details"
                    },
                },
                {
                    "$lookup": {
                        "from": "areas",
                        "localField": "area",
                        "foreignField": "_id",
                        "as": "area_details"
                    },
                }
                ])
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            dt=None
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dt))
        })

class DeleteVehicle(Resource):
    @staticmethod
    @jwt_required
    def post() -> Response:
        data = request.get_json()
        try:
            update_ = mongo.db.vehicles.update(
                {
                    "_id": bsonO.ObjectId(data["_id"])
                },
                {
                    "$set": {
                        "del_status": True,
                        "del_resone": data["del_resone"],
                        "del_date": datetime.datetime.now()
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

class GetVehicleTypeDataField(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        try:
            data = GetDataFields(bsonO.ObjectId(data["_id"]))
            msg = "SUCCESS"
            error = False
        except Exception as e:
            msg = str(ex)
            error = True
            err_msg = ex
            dt = None
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })


def GetDataFields(vehicleID):
    try:
        fieldData = mongo.db.vehicleType.find_one({"_id":vehicleID},{"data_fields": 1,"_id":0})
        return fieldData
    except Exception as e:
        return None
