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
            "userId": userId,
            "vehicleType": bsonO.ObjectId(data["vehicle_type"]),
            "fuelType": bsonO.ObjectId(data["fuelType"]),
            "vehicleNumber": data["vehicleNumber"],
            "regNumber": data["regNumber"],
            "chassisNumber": data["chassisNumber"],
            "engineNumber":  data["engineNumber"],
            "tiresNumber": data["tiresNumber"],
            "capacity": data["capacity"],
            "vehicleCC": data["vehicleCC"],
            "color": data["color"],
            "vehicleLength": data["vehicleLength"],
            "licenceVelidation": data["licenceVelidation"],
            "coverImage": data["coverImage"],
            "vehicle_imgs": data["vehicle_imgs"],
            "brand": bsonO.ObjectId(data["brand"]),
            "model": data["model"],
            "manufactureYear": data["manufactureYear"],
            "video": data["video"],
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
            "default_contact_number":data["default_contact_number"],
            "refType": data["refType"],
            "create_date": datetime.datetime.now()
    }
    return dt

def insertData(data):
    error = False
    msg = ""
    vehicleId = bsonO.ObjectId()
    userId = bsonO.ObjectId(get_jwt_identity())    
    dt = getAllDataField(data) 
    dt["_id"] = vehicleId
    userRole = data["role"]
    driverInfo=data["driverInfo"]
    ownerInfo  = []
    references = []
    if userRole =="owner":        
        driverId = bsonO.ObjectId()
        driverInfo["_id"] = driverId
        driverInfo["refType"] = data["refType"]
        if data["refType"] == "byOwner" :            
            driverInfo["vehicleId"] = vehicleId 
            dt["driver"] = driverId         
    else:
        ownerInfo=data["ownerInfo"]
        dt["driver"] = userId
        ownerInfo["_id"] = bsonO.ObjectId()
        ownerInfo["vehicleId"] = vehicleId
        references = data["reference"]
    try:
        fuelData = mongo.db.fuelType.find({"_id":bsonO.ObjectId(data["fuelType"])}).count()
        if fuelData == 0:
            return jsonify({
            "msg": "Fuel is not valid",
            "error": True,
            "data": json.loads(dumps(dt))
        })      
        vehicleTypeData = mongo.db.vehicleType.find({"_id":bsonO.ObjectId(data["vehicle_type"])}).count()
        if vehicleTypeData == 0:
            return jsonify({
            "msg": "Vehicle Type is not valid",
            "error": True,
            "data": json.loads(dumps(dt))
        })                     
        ins = mongo.db.vehicles.insert(dt)
        statusChange = mongo.db.userRegister.update(
            {
                "_id":userId
            },           
            {
                "$addToSet": {
                    "role":userRole,
                    "drivers" : driverInfo,
                    "owners" : ownerInfo,
                    "reference":references                    
                }
            }            
        )
        msg = "SUCCESS"
        error = False
    except Exception as ex:
        msg = str(ex)
        error = True
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
    def get() -> Response:
        msg = ""
        vehicleDetails = None
        current_user = bsonO.ObjectId(get_jwt_identity())
        try:
            dt = mongo.db.vehicles.aggregate(
                [{
                    "$match": {
                        "userId": current_user,
                        "del_status": False
                    }
                },                
                {
                    "$lookup": {
                        "from": "fuelType",
                        "localField": "fuelType",
                        "foreignField": "_id",
                        "as": "fuel_details"
                    },
                }
                ])
            vehicelTypeId = None            
            for i in dt:
                if i["vehicleType"] != None:               
                    vehicelTypeId = bsonO.ObjectId(i["vehicleType"])
                    vehicleDetails=i
            vehicleTypeDetails = mongo.db.vehicleType.find_one({"_id":vehicelTypeId})
            vehicleDetails["vehicleTypeTitle"]= vehicleTypeDetails["title"]  
            for i in vehicleTypeDetails["brands"]:
                if i["_id"] ==  bsonO.ObjectId(vehicleDetails["brand"]):
                    vehicleDetails["brandTitle"]=i["brand"]
                    print(vehicleDetails["brandTitle"])  
                
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            dt=None
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(vehicleDetails))
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
        