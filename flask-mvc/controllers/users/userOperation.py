from bson.json_util import dumps
from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import datetime
import bson
import json


class ProfileEdit(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        flag = UpdateData(data)
        if flag == True:
            msg = "SUCCESS"
            error = False

        else:
            error = True
            msg = "FAILED"

        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })


def UpdateData(data):
    idU = bson.ObjectId(data["_id"])
    try:
        update_ = mongo.db.users.update(
            {
                "_id": idU
            },
            {
                "$set": {
                    "f_name": data["f_name"],
                    "l_name": data["l_name"],
                    "email": data["email"],
                    "country": data["country"],
                    "city":  bson.ObjectId(data["city"]),
                    "address": data["address"],
                    "password": data["password"],
                    "phn_no": data["phn_no"],
                    "profile_pic": data["profile_pic"],
                    "update_date": datetime.datetime.now()
                }
            }
        )
        return True
    except:
        return False


class ProfileDelete(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        flag = DeleteData(data)
        if flag == True:
            msg = "SUCCESS"
            error = False

        else:
            error = True
            msg = "FAILED"

        return jsonify({
            "msg": msg,
            "error": error,
            "data": data
        })


def DeleteData(data):
    idU = bson.ObjectId(data["_id"])
    try:
        update_ = mongo.db.users.update(
            {
                "_id": idU
            },
            {
                "$set": {
                    "del_satus": True,
                    "del_resone": data["del_resone"],
                    "del_date": datetime.datetime.now()
                }
            }
        )
        return True
    except:
        return False


class GetAllUser(Resource):
    @staticmethod
    def post() -> Response:
        dat = request.get_json()

        data = mongo.db.users.find()
        x = json.loads(dumps(data))
        return jsonify({
            'data': x
        })
        return jsonify(x)


def GetAllUserData():
    try:
        data = mongo.db.users.find()
        for i in data:
            print(i)
            print(i["_id"])
            print(data[i]["_id"])
            data[i]["_id"] = str(i["_id"])
        print(data)
        return data
    except:
        return None
