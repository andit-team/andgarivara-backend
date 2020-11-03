
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
            indexCreate = mongo.db.vehicleType.create_index(
                'title', unique=True)
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
        try:
            insD = mongo.db.vehicleType.update_one(
                {
                    "_id": bson.ObjectId(data["_id"])
                },
                {
                    "$set": {
                        "title": data["title"],
                        "update_date": datetime.datetime.now()
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

class VehicleTypeById(Resource):
    @staticmethod
    def get() -> Response:
        data = request.get_json()
        allData = None
        try:
            allData = mongo.db.vehicleType.find_one(
                {
                    "_id": bson.ObjectId(data["_id"])
                })  
            msg = "SUCCESSFULL"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(allData))
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
        data = None
        try:
            data = mongo.db.vehicleType.find({},{"_id":1,"title":1,})
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
        
class AddBrandWithVehicleType(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        try:
            countModel = mongo.db.vehicleType.find({
                "_id": bson.ObjectId(data["_id"]),
                "brands.brand": data["brand"]
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
                        "brands": {
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
                        "brands.$": {
                            "_id": bson.ObjectId(data["brand_id"]),
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

class BrandWithVehicleTypeById(Resource):
    @staticmethod
    def get() -> Response:
        data = request.get_json()
        brandId = bson.ObjectId(data["brand_id"])
        allData = None
        try:
            getAllData = mongo.db.vehicleType.find_one(
                {
                   "_id": bson.ObjectId(data["_id"]),
                    "brands._id": brandId
                }) 
            if getAllData !=None:
                for i in getAllData["brands"]:
                    if i["_id"] == brandId:
                        allData = i                   
            msg = "SUCCESSFULL"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(allData))
        })
        
class VehicleBrandList(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        dt = None
        try:
            dt = mongo.db.vehicleType.find(
                {"_id": bson.ObjectId(data["_id"])}, {"_id": 0, "brands": 1})
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
