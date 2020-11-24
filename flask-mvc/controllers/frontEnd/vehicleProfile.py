from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps
import constants.constantValue as constants


class VehicleProfile(Resource):
    @staticmethod
    def get(id) -> Response:
        msg = ""
        vehicleDataList = []
        try:
            vehicleData = mongo.db.vehicles.aggregate(
                                                        [{
                                                            "$match": {
                                                                "_id" : bsonO.ObjectId(id),
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
                                                        }                                                                                                               
                                                        ]) 
            for i in vehicleData:
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
                    if i["refType"] == constants.REFFERENCE_TYPE_OWNER:
                        allDetails = mongo.db.userRegister.find_one({
                                                                            "_id" : bsonO.ObjectId(i["userId"]),
                                                                           "drivers" :{
                                                                                "$elemMatch":{
                                                                                    "_id" : bsonO.ObjectId(i["driver"])
                                                                                }
                                                                            }

                                                                     },{"_id" : 0, "drivers.$" : 1})
                        i["driverDetails"] = allDetails["drivers"]                        
                    elif i["refType"] == constants.REFFERENCE_TYPE_DRIVER:
                        allDetails = mongo.db.userRegister.find_one({
                                                                            "_id" : bsonO.ObjectId(i["userId"]),
                                                                            "owners" :{
                                                                                "$elemMatch":{
                                                                                    "vehicleId" : bsonO.ObjectId(id)
                                                                                }
                                                                            }

                                                                       },{"_id" : 0, "owners.$" : 1, "drivers" : 1})        
                        i["driverDetails"] = [allDetails["drivers"]]
                    else:
                        if "driver" in i:
                                driverDetails = mongo.db.userRegister.find_one({
                                                                            "_id" : bsonO.ObjectId(i["driver"]),
                                                                            
                                                                       },
                                                                       {
                                                                           "_id" : 0, "drivers" : 1
                                                                        })
                                i["driverDetails"] = [driverDetails["drivers"]]
                        else:
                            i["driverDetails"] = []                         
                    vehicleDataList.append(i)                    
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(vehicleDataList))
        })
