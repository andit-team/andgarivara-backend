from bson import objectid
from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
from pymongo import UpdateOne
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps
from flask_jwt_extended import jwt_required, get_jwt_identity
import constants.constantValue as constants


class AddVehicleInService(Resource):
    @staticmethod
    @jwt_required
    def put(id) -> Response:
        data = request.get_json()
        vehicelTypeId = bsonO.ObjectId(id)
        serviceDetails = None
        serviceType = None
        msg = None
        error = None
        
        if data["serviceType"] == "rental":
            serviceType = constants.SERVICE_RENTAL
            serviceDetails ={
                "service" : serviceType,
                "faq" :data["faq"],
                "perDayRent": data["perDayRent"],
                "perHourRent": data["perHourRent"]
            }
            
        elif data["serviceType"] == "lease":
            serviceType = constants.SERVICE_LEASE
            serviceDetails ={
                "service" : serviceType,
                "faq" :data["faq"],
                "leaseRate": data["leaseRate"]
            }
        elif data["serviceType"] == "rideshare":
            serviceType = constants.SERVICE_RIDESHARE
        else:
            serviceType = constants.SERVICE_INSTANTRIDE
            
        
        try:           
            bulkAction = mongo.db.vehicles.bulk_write(
                [
                    UpdateOne(
                        {
                            "_id":vehicelTypeId
                        },
                        {
                            "$set":{
                                "activeService" : serviceType,
                                "serviceDetails": serviceDetails,
                                "description": data["description"],
                                "vehicle_imgs": data["vehicle_imgs"],
                                "video": data["video"]
                            }
                        }
                    ),
                    UpdateOne(
                        {
                            "_id":vehicelTypeId
                        },
                        {
                            "$addToSet": {  
                                "service": serviceType                                         
                            }
                        }
                        )
                ]
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