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
        vehicelId = bsonO.ObjectId(id)
        userId = bsonO.ObjectId(get_jwt_identity())
        serviceDetails = None
        serviceType = None
        msg = None
        error = None

        if data["serviceType"] == "rental":
            serviceType = constants.SERVICE_RENTAL
            serviceDetails = {
                "service": serviceType,
                "faq": data["faq"],
                "perDayBodyRent": data["perDayBodyRent"],
                "perDayBodyRentNightStay": data["perDayBodyRentNightStay"],
                "perHourRentWithFuel": data["perHourRentWithFuel"],
                "perHourRentWithoutFuel": data["perHourRentWithoutFuel"]
            }

        elif data["serviceType"] == "lease":
            serviceType = constants.SERVICE_LEASE
            serviceDetails = {
                "service": serviceType,
                "faq": data["faq"],
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
                            "_id": vehicelId,
                            "userId": userId
                        },
                        {
                            "$set": {
                                "activeService": serviceType,
                                "serviceDetails": serviceDetails,
                                "description": data["description"]
                            }
                        }
                    ),
                    UpdateOne(
                        {
                            "_id": vehicelId,
                            "userId": userId
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


class GetVehicleServiceCost(Resource):
    @staticmethod
    @jwt_required
    def get(id) -> Response:
        vehicelId = bsonO.ObjectId(id)
        serviceData = None
        msg = None
        error = None
        try:
            serviceData = mongo.db.vehicles.find_one(
                {
                    "_id": vehicelId
                },
                {
                    "activeService": 1,
                    "serviceDetails": 1,
                    "description": 1
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
            "data": json.loads(dumps(serviceData))
        })
