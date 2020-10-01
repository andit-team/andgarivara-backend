from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps
from werkzeug.security import generate_password_hash


class UserSignup(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        flag = insertData(data)
        return flag


def insertData(data):
    userId = data["phn_no"]
    psw = data["password"]
    err_msg = None
    countUser = mongo.db.users.find({"phn_no": userId}).count()
    if countUser > 0:
        msg = "User Already Exist."
        error = True
        err_msg = "Duplicate user found"
        dt = None
    else:
        dt = {
            "f_name": data["f_name"],
            "l_name": data["l_name"],
            "email": "",
            "country": "",
            "city": "",
            "address": "",
            "password": generate_password_hash(data["password"]),
            "phn_no": data["phn_no"],
            "del_date": "",
            "del_resone": "",
            "profile_pic": "",
            "bookmarks": [
            ],
            "del_status": False,
            "create_date": datetime.datetime.now()
        }

        try:
            ins = mongo.db.users.insert(dt)
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = "FAILED"
            error = True
            err_msg = ex
    return jsonify({
        "msg": msg,
        "error": error,
        "data": json.loads(dumps(dt))
    })
