from bson.json_util import dumps
from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import datetime
import bson
import json
from flask_jwt_extended import jwt_required, get_jwt_identity,create_access_token


class ProfileEdit(Resource):
    @staticmethod
    @jwt_required
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
    idU = bson.ObjectId(get_jwt_identity())
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
    @jwt_required
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
    idU = bson.ObjectId(get_jwt_identity())
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

