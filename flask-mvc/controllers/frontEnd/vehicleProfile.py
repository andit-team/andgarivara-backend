from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps


class VehicleProfile(Resource):
    @staticmethod
    def get(id) -> Response:
        vehicleDetails = None
        try:
            dt = mongo.db.vehicles.aggregate(
                [{
                    "$match": {
                        "_Id": id,
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
