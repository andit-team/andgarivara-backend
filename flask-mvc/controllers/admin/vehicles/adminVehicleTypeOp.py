
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
        dtList = []
        dtDict = None
        for dt in data["data_fields"]:
            dtDict = {
            "_id": bson.ObjectId(),
            "field_label":dt["field_label"].upper(),
            "field_type":dt["field_type"],
            "value_type":dt["value_type"]
            }
            dtList.append(dtDict)
        dt = {
            "title": data["title"],
            "data_fields": dtList,
            "create_date": datetime.datetime.now()
        }
        try:
            insD = mongo.db.vehicleType.insert_one(dt)
            msg = "SUCCESSFULL"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dt))
        })


class EditVehicleType(Resource):
    @staticmethod
    def put() -> Response:
        data = request.get_json()
        dtList = []
        dtDict = None
        for dt in data["data_fields"]:
            dtDict = {
            "_id": bson.ObjectId(),
            "field_label":dt["field_label"].upper(),
            "field_type":dt["field_type"],
            "value_type":dt["value_type"]
            }
            dtList.append(dtDict)
        try:
            insD = mongo.db.vehicleType.update_one(
                {
                    "_id": bson.ObjectId(data["_id"])
                },
                {
                    "$set": {
                        "title": data["title"],
                        "data_fields": dtList,
                        "update_date": datetime.datetime.now()
                    }
                }
            )
            msg = "SUCCESSFULL"
            error = False
        except Exception as ex:
            msg =str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })


class DeleteVehicleType(Resource):
    @staticmethod
    def delete() -> Response:
        data = request.get_json()
        dt = {
            "_id": bson.ObjectId(data["_id"])
        }
        try:
            delD = mongo.db.vehicleType.delete_one(dt)
            msg = "SUCCESSFULL"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dt))
        })


class VehicleTypeList(Resource):
    @staticmethod
    def get() -> Response:
        data = request.get_json()

        try:
            dt = mongo.db.vehicleType.find({})
            msg = "SUCCESSFULL"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dt))
        })

class AddBrandWithVehicleType(Resource):
    @staticmethod
    def put() -> Response:
        data = request.get_json()

        try:
            countModel=mongo.db.vehicleType.find({
            "_id": bson.ObjectId(data["_id"]),
            "brands.model": data["model"]
            }).count()
            if countModel > 0:
                return jsonify({
                    "msg": "Duplicate Model Found!!!",
                    "error": True,
                    "data": json.loads(dumps(data))
                })
            insD = mongo.db.vehicleType.update_one(
                {
                    "_id": bson.ObjectId(data["_id"])
                },
                {
                    "$addToSet": {
                        "brands":{
                            "_id": bson.ObjectId(),
                            "brand": data["brand"]
                        }
                    }
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


class EditBrandWithVehicleType(Resource):
    @staticmethod
    def put() -> Response:
        data = request.get_json()

        try:
            insD = mongo.db.vehicleType.update_one(
                {
                    "_id": bson.ObjectId(data["_id"]),
                    "brands._id": bson.ObjectId(data["brand_id"])
                },
                {
                    "$set": {
                        "brands.$":{
                            "_id": bson.ObjectId(data["brand_id"]),
                            "brand": data["brand"]
                        }
                    }
                }
            )
            msg = "SUCCESSFULL"
            error = False
        except Exception as ex:
            msg =  str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })

class VehicleBrandList(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        try:
            dt = mongo.db.vehicleType.find({"_id":bson.ObjectId(data["_id"])},{"_id":0,"brands":1})
            msg = "SUCCESSFULL"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dt))
        })
