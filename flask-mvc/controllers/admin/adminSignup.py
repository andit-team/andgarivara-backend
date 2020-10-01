from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps
from werkzeug.security import generate_password_hash


class AdminSignup(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        err_msg = None
        userId = data["phn_no"]
        psw = data["password"]
        dt = {
            "f_name": data["f_name"],
            "l_name": data["l_name"],
            "email": "",
            "password": generate_password_hash(data["password"]),
            "phn_no": data["phn_no"],
            "del_date": "",
            "del_resone": "",
            "profile_pic": "",
            "del_status": False,
            "create_date": datetime.datetime.now()
        }

        try:
            ins = mongo.db.adminsLog.insert_one(dt)
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = "SUCCESS"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dt))
        })
