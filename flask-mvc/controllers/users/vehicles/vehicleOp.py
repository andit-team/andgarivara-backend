from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from pymongo import GEO2D, UpdateOne, MongoClient, GEOSPHERE 
from bson.json_util import dumps
from flask_jwt_extended import jwt_required, get_jwt_identity
import constants.constantValue as constants

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
            "ac": data["ac"],
            "vehicleTitle": data["vehicleTitle"],
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
            "activeStatus" :constants.STATUS_PENDING,
            "default_contact_number":data["default_contact_number"],
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
    dt["refType"] = data["refType"]
    userRole = data["role"]
    driverInfo=data["driverInfo"]
    driverInfo["refType"] = data["refType"]
    ownerInfo  = []
    references = []

    if userRole == constants.ROLL_OWNER:
        if data["refType"] == constants.REFFERENCE_TYPE_OWNER :
            driverData = mongo.db.userRegister.distinct("drivers.drivingLicence",{"_id" : userId})
            if data["drivingLicence"] in driverData:
                error = True
                msg = "Driver is already Added to another Vehicle!!!" 
                return jsonify({
                "msg": msg,
                "error": error
                })
            else:
                driverInfo["vehicleId"] = vehicleId
                driverId = bsonO.ObjectId()
                driverInfo["_id"] = driverId
                dt["driver"] = driverId 
                  
    else:
        vehicleData = mongo.db.vehicles.find({"driver" : userId, "del_status" : False}).count()
        if vehicleData > 0:
            error = True
            msg = "Driver is already Occupied!!!" 
            return jsonify({
            "msg": msg,
            "error": error
            })
        else:
            ownerInfo=data["ownerInfo"]
            dt["driver"] = userId
            ownerInfo["_id"] = bsonO.ObjectId()
            ownerInfo["vehicleId"] = vehicleId
            references = data["reference"]
    try:
        createIndex = mongo.db.vehicles.create_index([("carLocation", GEOSPHERE)] )
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
        userRollData = mongo.db.userRegister.find_one({"_id":userId},{"role" : 1, "_id": 0})
        rolleNew = constants.ROLL_PASSENGER
        for i in userRollData["role"]:
            if i == constants.ROLL_OWNER:
                rolleNew = constants.ROLL_OWNER
            elif i == constants.ROLL_DRIVER:
                rolleNew = constants.ROLL_DRIVER
        
        if rolleNew == constants.ROLL_PASSENGER and userRole == constants.ROLL_DRIVER:            
            bulkAction = mongo.db.userRegister.bulk_write(
                [
                    UpdateOne(
                         {
                    "_id":userId
                },
                {
                    "$addToSet": {
                        "role":userRole,                        
                        "owners" : ownerInfo,                      
                        "reference": references
                    }
                }
                    ),
                    UpdateOne(
                    {
                        "_id":userId
                    },
                    {
                        "$set": {
                            "driverStatus" : constants.STATUS_PENDING,
                            "drivers" : driverInfo,
                            "driverOccupied" : True
                        }
                    }
                    )
                ]
            )
        elif userRole == constants.ROLL_OWNER:
            if data["refType"] == constants.REFFERENCE_TYPE_OWNER:
                statusChange = mongo.db.userRegister.update(
                    {
                        "_id":userId
                    },
                    {
                        "$addToSet": {
                            "role":userRole,
                            "drivers" : driverInfo,
                        }
                    }
                )
            else:
                statusChange = mongo.db.userRegister.update(
                    {
                        "_id":userId
                    },
                    {
                        "$addToSet": {
                            "role":userRole
                        }
                    }
                )
        else:
            bulkAction = mongo.db.userRegister.bulk_write(
                [
                    UpdateOne(
                         {
                    "_id":userId
                },
                {
                    "$addToSet": {
                        "role":userRole,
                        "owners" : ownerInfo,
                        "reference":references
                    }
                }
                    ),
                    UpdateOne(
                    {
                        "_id":userId
                    },
                    {
                        "$set": {
                            "drivers" : driverInfo
                        }
                    }
                    )
                ]
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
    def put(id) -> Response:
        data = request.get_json()
        userId = bsonO.ObjectId(get_jwt_identity())
        vehicelId = bsonO.ObjectId(id)        
        data["vehicleType"] = data["vehicle_type"]
        data["update_date"] = datetime.datetime.now()
        data.pop("vehicle_type")
        try:
            update_ = mongo.db.vehicles.update(
                {
                    "_id": vehicelId,
                    "userId" : userId
                },
                {
                    "$set": data
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
        vList = []
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
                if i != None:                    
                    vehicleTypeId = bsonO.ObjectId(i["vehicleType"])
                    vehicleTypeDetails = mongo.db.vehicleType.find_one(
                        {
                            "_id" : vehicleTypeId,
                            "brands" :
                                {
                                    "$elemMatch":{
                                        "_id" : bsonO.ObjectId(i["brand"])
                                    }
                                }
                        },
                        {
                            "_id" : 0, "brands.$" : 1, "title" : 1
                        }
                    )
                    i["vehicleTypeDetails"] = vehicleTypeDetails
                    vList.append(i)

            msg = "SUCCESS"
            error = False
        except Exception as ex:
            dt=None
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(vList))
        })

class DeleteVehicle(Resource):
    @staticmethod
    @jwt_required
    def put(id) -> Response:
        data = request.get_json()
        try:
            update_ = mongo.db.vehicles.update(
                {
                    "_id": bsonO.ObjectId(id)
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
        except Exception as ex:
            msg = str(ex)
            error = True 
            
        return jsonify({
            "msg": msg,
            "error": error,
            "data": None
        })

class GetVehicleDataById(Resource):
    @staticmethod
    @jwt_required
    def get(id) ->Response:
        vehicleData = None
        msg = ""
        error = None
        try:
            vehicleData = mongo.db.vehicles.find_one({"_id" : bsonO.ObjectId(id)})
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(vehicleData))
        })
        
class GetVehicleServiceHelperData(Resource):
    @staticmethod
    @jwt_required
    def get(id) ->Response:
        vehicleData = None
        msg = ""
        error = None
        try:            
            vehicleData = mongo.db.vehicles.aggregate(
                                                        [{
                                                            "$match": {
                                                                "_id" : bsonO.ObjectId(id),
                                                                "activeStatus" : constants.STATUS_VERIFIED,
                                                                "del_status": False
                                                            }
                                                        },
                                                            {
                                                            "$lookup": {
                                                                "from": "fuelType",
                                                                "localField": "fuelType",
                                                                "foreignField": "_id",
                                                                "as": "fuel_type_details"
                                                            }
                                                        },
                                                            { "$project" : 
                                                                { 
                                                                    "millage": 1,
                                                                    "activeStatus": 1,
                                                                    "fuel_type_details": 1
                                                                }
                                                        }                                                           
                                                        ])
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(vehicleData))
        })