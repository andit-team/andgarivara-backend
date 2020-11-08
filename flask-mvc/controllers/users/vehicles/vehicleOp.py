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
def getAllDataField(data):
    userId = bsonO.ObjectId(get_jwt_identity())
    dt = {
            "user_id": userId,
            "vehicle_type": bsonO.ObjectId(data["vehicle_type"]),
            "vehicleNumber": data["vehicleNumber"],
            "regNumber": data["regNumber"],
            "chassisNumber": bsonO.ObjectId(data["chassisNumber"]),
            "engineNumber":  bsonO.ObjectId(data["engineNumber"]),
            "tiresNumber": data["tiresNumber"],
            "capacity": data["capacity"],
            "vehicleCC": data["vehicleCC"],
            "color": data["color"],
            "vehicleLength": data["vehicleLength"],
            "licenceVelidation": data["licenceVelidation"],
            "coverImage": data["coverImage"],
            "vehicle_imgs": data["vehicle_imgs"],
            "description": data["description"],
            "brand": data["brand"],
            "model": data["model"],
            "manufactureYear": data["manufactureYear"],
            "video": data["video"],
            "fuelType": data["fuelType"],
            "millage": data["millage"],
            "gearType": data["gearType"],
            "policyType": data["policyType"],
            "policyNumber": data["policyNumber"],
            "insuranceName": data["insuranceName"],
            "insuranceExpiry": data["insuranceExpiry"],
            "insuranceCompany": data["insuranceCompany"],
            "country": data["country"],
            "carLocation": data["carLocation"],
            "carAddress": data["carAddress"],
            "del_status": False,
            "activeStatus" :"pending",
            "create_date": datetime.datetime.now()
    }
    return dt

def insertData(data):
    userId = bsonO.ObjectId(get_jwt_identity())    
    dt = getAllDataField(data) 
    userRole = data["role"]
    driverInfo = []
    ownerInfo  = []
    if userRole =="owner":
        driverInfo=data["driverInfo"]
        if data["refType"] == "byOwner" :
            driverInfo["_id"] = bsonO.ObjectId()
            driverInfo["refType"] = data["refType"]
        else:
            driverInfo["refType"] = "byAdmin"
        dt["driver"] = driverInfo["_id"]
    else:
        ownerInfo=data["ownerInfo"]
        dt["driver"] = userId
        driverInfo["_id"] = userId
        driverInfo["refType"] = "byDriver"
    try:
        ins = mongo.db.vehicles.insert(dt)
        statusChange = mongo.db.userRegister.update(
            {
                "_id":userId
            },
            {
                "$addToSet": {
                    "role":userRole,
                    "driverInfo" : driverInfo,
                    "ownerInfo" : ownerInfo
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
        dt = getAllDataField(data)
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