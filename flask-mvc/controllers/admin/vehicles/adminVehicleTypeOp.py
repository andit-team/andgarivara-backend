from bson.json_util import dumps
from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import datetime
import bson
import json
from flask_jwt_extended import jwt_required, get_jwt_identity


class AddVehicleType(Resource):
    @staticmethod
    @jwt_required
    def post() -> Response:
        data = request.get_json()
        dt = {
            "title": data["title"],
            "typeIcon": data["typeIcon"],
            "create_date": datetime.datetime.now()
        }
        try:
            adminCount = mongo.db.adminRegister.find({"_id": bson.ObjectId(get_jwt_identity())}).count()
            if adminCount == 0:
                return jsonify({
                    "msg": "Your Are not Authenticate Admin",
                    "error": True,
                    "data": None
                })
            indexCreate = mongo.db.vehicleType.create_index('title', unique=True)
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
    @jwt_required
    def put(id) -> Response:
        print(id)
        data = request.get_json()
        try:
            adminCount = mongo.db.adminRegister.find({"_id": bson.ObjectId(get_jwt_identity())}).count()
            if adminCount == 0:
                return jsonify({
                    "msg": "Your Are not Authenticate Admin",
                    "error": True,
                    "data": None
                })
            insD = mongo.db.vehicleType.update_one(
                {
                    "_id": bson.ObjectId(id)
                },
                {
                    "$set": {
                        "title": data["title"],
                        "typeIcon": data["typeIcon"],
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
    @jwt_required
    def get(id) -> Response:
        allData = None
        try:
            adminCount = mongo.db.adminRegister.find({"_id": bson.ObjectId(get_jwt_identity())}).count()
            if adminCount == 0:
                return jsonify({
                    "msg": "Your Are not Authenticate Admin",
                    "error": True,
                    "data": None
                })
            allData = mongo.db.vehicleType.find_one(
                {
                    "_id": bson.ObjectId(id)
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
    @jwt_required
    def delete() -> Response:
        data = request.get_json()
        dt = {
            "_id": bson.ObjectId(data["_id"])
        }
        try:
            adminCount = mongo.db.adminRegister.find({"_id": bson.ObjectId(get_jwt_identity())}).count()
            if adminCount == 0:
                return jsonify({
                    "msg": "Your Are not Authenticate Admin",
                    "error": True,
                    "data": None
                })
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
            data = mongo.db.vehicleType.find({},{"_id":1,"title":1, "typeIcon":1}).sort("create_date")
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
    @jwt_required
    def post() -> Response:
        data = request.get_json()
        try:
            adminCount = mongo.db.adminRegister.find({"_id": bson.ObjectId(get_jwt_identity())}).count()
            if adminCount == 0:
                return jsonify({
                    "msg": "Your Are not Authenticate Admin",
                    "error": True,
                    "data": None
                })
            countModel = mongo.db.vehicleType.find({
                "_id": bson.ObjectId(data["_id"]),
                "brands.brand": data["brand"]
            }).count()
            if countModel > 0:
                return jsonify({
                    "msg": "Duplicate Brand Found!!!",
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
    @jwt_required
    def put() -> Response:
        data = request.get_json()

        try:
            adminCount = mongo.db.adminRegister.find({"_id": bson.ObjectId(get_jwt_identity())}).count()
            if adminCount == 0:
                return jsonify({
                    "msg": "Your Are not Authenticate Admin",
                    "error": True,
                    "data": None
                })
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
    @jwt_required
    def get(id) -> Response:
        brandId = bson.ObjectId(id)
        allData = None
        try:
            adminCount = mongo.db.adminRegister.find({"_id": bson.ObjectId(get_jwt_identity())}).count()
            if adminCount == 0:
                return jsonify({
                    "msg": "Your Are not Authenticate Admin",
                    "error": True,
                    "data": None
                })
            getAllData = mongo.db.vehicleType.find_one(
                {
                   "brands._id": brandId
                }) 
            if getAllData !=None:
                for i in getAllData["brands"]:
                    if i["_id"] == brandId:
                        allData = i                   
            allData["vehicle_type"] = getAllData["title"]
            allData["vehicle_type_id"] = getAllData["_id"]
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
    def get(id) -> Response:
        dt = None
        try:
            dt = mongo.db.vehicleType.find(
                {"_id": bson.ObjectId(id)}, {"_id": 0, "brands": 1})
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