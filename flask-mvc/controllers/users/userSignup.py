from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps


class UserSignup(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        flag = insertData(data)
        if flag == True:
            msg = "SUCCESS"
            error = False

        else:
            msg = "FAILED"
            error = True

        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })


class PhoneVerification(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        phoneNum = data["phoneNum"]
        vCode = data["vCode"]
        code_collection = mongo.db.codes
        codeAvail = code_collection.find_one(
            {"phoneNum": phoneNum}, {"vCode": 1})
        if codeAvail is None:
            return jsonify(message="FAILED")
        elif (codeAvail["vCode"] != vCode):
            return jsonify(message="Not Matched")
        else:
            return jsonify("phone number:"+phoneNum)


def insertData(data):
    userId = data["phn_no"]
    psw = data["password"]
    dt = {
        "f_name": data["f_name"],
        "l_name": data["l_name"],
        "email": "",
        "country": "",
        "city": "",
        "address": "",
        "password": data["password"],
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
        return True
    except:
        return False
