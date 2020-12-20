from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps
from flask_jwt_extended import get_jwt_identity, jwt_required
import constants.constantValue as constants
from pymongo import UpdateOne
from werkzeug.security import generate_password_hash


class DriverSignup(Resource):
    @staticmethod
    def post() -> Response:
        msg = None
        error = None
        data = request.get_json()
        try:            
            insertDriver = mongo.db.userRegister.insert_one(
                {
                    "phone_no": data["phone_no"],
                    "password": generate_password_hash(data["password"]),
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "email": data["email"],
                    "address": data["address"],
                    "country": data["country"],
                    "pushNotification": {
                        "on_message_send": True,
                        "on_booking": True,
                        "on_suppport_reply": True
                    },
                    "smsNotification": {
                        "on_message_send": True,
                        "on_booking": True,
                        "on_suppport_reply": True
                    },
                    "default_contact_number" :data["phone_no"],
                    "profile_pic" :data["profile_pic"],
                    "del_status":False,
                    "create_date": datetime.datetime.now(),
                    "role":constants.ROLL_DRIVER,
                    "reference":data["reference"],
                    "drivers" : driverInfo,
                    "driverStatus": constants.STATUS_PENDING,
                    "driverOccupied" : False
                }
            )            
            msg = "Registered Successfully"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data" : json.loads(dumps(data))
        })
