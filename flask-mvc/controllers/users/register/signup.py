from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps
from werkzeug.security import generate_password_hash
import constants.constantValue as constants


class UserSignup(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        dt = {
            "phone_no": data["phone_no"],
            "password": generate_password_hash(data["password"]),
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "email": data["email"],
            "role": [constants.ROLL_PASSENGER],
            "address": "",
            "country": "",
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
            "default_contact_number" :"",
            "del_status":False,
            "create_date": datetime.datetime.now()
        }
        try:
            indexCreate = mongo.db.userRegister.create_index(
                'phone_no', unique=True)
            ins = mongo.db.userRegister.insert_one(dt)
            msg = "Inserted Successfully"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error
        })
