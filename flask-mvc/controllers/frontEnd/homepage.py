from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps
from flask_jwt_extended import jwt_required, get_jwt_identity


class HomePage(Resource):
    @staticmethod
    def get() -> Response:
        data = request.get_json()
        dtRentalVehicle = None
        # dtLeasingVehicle = None
        # dtRideShareVehicle = None
        # dtInstantRideVehicle = None
        # dtDrive = None
        userData = None
        try:
            if get_jwt_identity() != None:
                uId = bsonO.ObjectId(get_jwt_identity())
            userData = mongo.db.users.find_one(
                {"_id": uId},
                {

                }
            )
            # retrive rental vehicles by rating
            dtRentalVehicle = mongo.db.locationArea.find({})

            # # retrive Leasing vehicles by rating
            # dtLeasingVehicle = mongo.db.locationArea.find({})
            #
            # # retrive ride share vehicles by rating
            # dtRideShareVehicle = mongo.db.locationArea.find({})
            #
            # # retrive instant ride vehicles by rating
            # dtInstantRideVehicle = mongo.db.locationArea.find({})
            #
            # # retrive driver data by rating
            # dtDrive = mongo.db.drivers.find({})

            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "user_data": json.loads(dumps(userData)),
            "rental_data": json.loads(dumps(dtRentalVehicle)),
            # "leasing_data": json.loads(dumps(dtLeasingVehicle)),
            # "ride_share_data": json.loads(dumps(dtRideShareVehicle)),
            # "instant_ride_data": json.loads(dumps(dtInstantRideVehicle)),
            # "driver_data": json.loads(dumps(dtDrive))
        })
