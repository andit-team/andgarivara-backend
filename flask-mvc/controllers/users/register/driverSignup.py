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
            indexCreate = mongo.db.userRegister.create_index(
                'phone_no', unique=True)     
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
                    "driverStatus": constants.STATUS_PENDING,
                    "driverOccupied" : False,
                    "isMunicipal": data["isMunicipal"],
                    "division": data["division"],
                    "divisionTitle": data["divisionTitle"],
                    "district": data["district"],
                    "districtTitle": data["districtTitle"],
                    "upazila": data["upazila"],
                    "upazilaTitle": data["upazilaTitle"],
                    "union": data["union"],
                    "unionTitle": data["unionTitle"],
                    "village": data["village"],
                    "villageTitle": data["villageTitle"],
                    "municipal": data["municipal"],
                    "municipalTitle": data["municipalTitle"],
                    "ward":data["ward"],
                    "wardTitle": data["wardTitle"],
                    "dob": data["dob"],
                    "nid": data["nid"],
                    "drivingLicence" : data["drivingLicence"],
                    "drivingLicenceImg": data["drivingLicenceImg"],
                    "drivingLicenceType": data["drivingLicenceType"],  
                    "drivingLicenceExpiry": data["drivingLicenceExpiry"]
                }
            )            
            msg = "Registered Successfully"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error
        })
