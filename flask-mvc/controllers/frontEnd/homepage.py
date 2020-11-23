from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps
from flask_jwt_extended import jwt_required, get_jwt_identity
import constants.constantValue as constants


class HomePage(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        dtRentalVehicle = None
        # dtLeasingVehicle = None
        # dtRideShareVehicle = None
        # dtInstantRideVehicle = None
        dtDrive = None
        try:
            # if get_jwt_identity() != None:
            #     uId = bsonO.ObjectId(get_jwt_identity())
            #     userData = mongo.db.userRegister.find_one(
            #         {"_id": uId},
            #         {

            #         }
            #     )
            # retrive rental vehicles by rating
            dtRentalVehicle = mongo.db.vehicles.find({"activeService": constants.SERVICE_RENTAL, "activeStatus" : constants.STATUS_VERIFIED, "del_status" : False,
                                                      "carLocation": {
                                                                    "$near": {
                                                                    "$maxDistance": 20000,
                                                                    "$geometry": {
                                                                    "type": "Point",
                                                                    "coordinates": [data["long"],data["lat"]]
                                                                    }
                                                                }
                                                            }
                                                      },
                                                     {
                                                         "_id" : 1,
                                                         "vehicleTitle" : 1,
                                                         "carLocation" : 1,
                                                         "carAddress" : 1,
                                                         "vehicle_imgs" : 1,
                                                         "model" : 1,
                                                         "manufactureYear" : 1,
                                                         "ac" : 1,
                                                         "millage" : 1,
                                                         "serviceDetails.perDayRent" : 1,
                                                     }
                                                     )            
            print("vehicles On Rental: " + str(dtRentalVehicle.count()))
            # # retrive Leasing vehicles by rating
            # dtLeasingVehicle = mongo.db.vehicles.find({})
            #
            # # retrive ride share vehicles by rating
            # dtRideShareVehicle = mongo.db.vehicles.find({})
            #
            # # retrive instant ride vehicles by rating
            # dtInstantRideVehicle = mongo.db.vehicles.find({})
            #
            # retrive driver data by rating
            dtDrive = mongo.db.userRegister.find({"driverStatus" : constants.STATUS_VERIFIED, "del_status" : False},
                                                 {
                                                     "drivers" : 1
                                                 }
                                                 )
            print("Drivers: " + str(dtDrive.count()))
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            # "user_data": json.loads(dumps(userData)),
            "rental_data": json.loads(dumps(dtRentalVehicle)),
            # "leasing_data": json.loads(dumps(dtLeasingVehicle)),
            # "ride_share_data": json.loads(dumps(dtRideShareVehicle)),
            # "instant_ride_data": json.loads(dumps(dtInstantRideVehicle)),
            "driver_data": json.loads(dumps(dtDrive))
        })
