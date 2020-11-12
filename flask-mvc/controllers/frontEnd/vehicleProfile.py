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
            vehicleDetails = mongo.db.vehicles.find_one({"del_status": False,"_id":bsonO.ObjectId(id)})                     
            vehicelTypeId = bsonO.ObjectId(vehicleDetails["vehicleType"])
            fuelTypeDetails = mongo.db.fuelType.find_one({"_id":bsonO.ObjectId(vehicleDetails["fuelType"])})
            vehicleTypeDetails = mongo.db.vehicleType.find_one({"_id":vehicelTypeId})
            vehicleDetails["vehicleTypeTitle"]= vehicleTypeDetails["title"]  
            vehicleDetails["fuelTypeTitle"]= fuelTypeDetails["title"]  
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
