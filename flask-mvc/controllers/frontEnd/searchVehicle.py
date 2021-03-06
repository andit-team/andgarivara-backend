from os import error
from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps
import constants.constantValue as constants


class SearchVehicle(Resource):
    @staticmethod
    def post() -> Response:
        msg = None
        error = False
        dtVehicle = []
        data = request.get_json()
        queryCodition = {
            "activeService": data["service"], "activeStatus": constants.STATUS_VERIFIED, "del_status": False,
            "carLocation": {
                "$near": {
                    "$maxDistance": 20000,
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [data["long"], data["lat"]]
                    }
                }
            }
        }
        if data["vehicleType"]:
            queryCodition["vehicleType"] = bsonO.ObjectId(data["vehicleType"])

        dtVehicle = mongo.db.vehicles.find(queryCodition,
                                           {
                                               "_id": 1,
                                               "vehicleTypeTitle": 1,
                                               "fuelTypeTitle": 1,
                                               "brandTitle": 1,
                                               "carLocation": 1,
                                               "carAddress": 1,
                                               "thumbImage": 1,
                                               "model": 1,
                                               "manufactureYear": 1,
                                               "amenities.ac": 1,
                                               "millage": 1,
                                               "serviceDetails.perDayBodyRent": 1
                                           }
                                           )
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dtVehicle))
        })
