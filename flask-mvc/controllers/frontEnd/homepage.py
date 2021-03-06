from re import error
from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps
from flask_jwt_extended import jwt_required, get_jwt_identity
import constants.constantValue as constants


class GetRentalList(Resource):
    @staticmethod
    def get() -> Response:
        dtRentalVehicle = None
        msg = None
        error = False
        try:
            dtRentalVehicle = mongo.db.vehicles.find(
                {"activeService": constants.SERVICE_RENTAL, "activeStatus": constants.STATUS_VERIFIED,
                 "del_status": False,
                 # "carLocation": {
                 #             "$near": {
                 #             "$maxDistance": 20000,
                 #             "$geometry": {
                 #             "type": "Point",
                 #             "coordinates": [data["long"],data["lat"]]
                 #             }
                 #         }
                 #     }
                 },
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
                ).limit(5)
        except Exception as ex:
            msg = str(ex)
            error = True
        print(dtRentalVehicle.count())
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dtRentalVehicle))
        })

class GetDriverList(Resource):
    @staticmethod
    def get() -> Response:
        dtDriver = None
        msg = None
        error = False
        try:
            dtDriver = mongo.db.userRegister.find({"driverStatus": constants.STATUS_VERIFIED, "del_status": False},
                                                  {
                                                      "_id": 1,
                                                      "first_name": 1,
                                                      "last_name": 1,
                                                      "drivers.address": 1,
                                                      "drivers.image": 1,
                                                      "status_change_date": 1
                                                  }
                                                  ).limit(5)
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dtDriver))
        })
