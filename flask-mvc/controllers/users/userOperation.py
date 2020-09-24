from bson.json_util import dumps
from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import datetime
import bson
import json
from flask_jwt_extended import jwt_required, get_jwt_identity,create_access_token
from werkzeug.security import generate_password_hash

class ProfileEdit(Resource):
    @staticmethod
    @jwt_required
    def post() -> Response:
        data = request.get_json()
        flag = UpdateData(data)
        return flag


def UpdateData(data):
    idU = bson.ObjectId(get_jwt_identity())
    err_msg=None
    try:
        update_ = mongo.db.users.update_one(
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
                    "password": generate_password_hash(data["password"]),
                    "phn_no": data["phn_no"],
                    "profile_pic": data["profile_pic"],
                    "update_date": datetime.datetime.now()
                }
            }
        )
        msg = "SUCCESS"
        error = False
    except Exception as ex:
            msg = "FAILED"
            error = True
            err_msg=ex
    return jsonify({
        "msg": msg,
        "error": error,
        "err_msg":str(err_msg),
        "data": json.loads(dumps(data))
    })


class ProfileDelete(Resource):
    @staticmethod
    @jwt_required
    def post() -> Response:
        data = request.get_json()
        flag = DeleteData(data)
        return flag


def DeleteData(data):
    idU = bson.ObjectId(get_jwt_identity())
    err_msg=None
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
        msg = "SUCCESS"
        error = False
    except Exception as ex:
            msg = "FAILED"
            error = True
            err_msg=ex
    return jsonify({
        "msg": msg,
        "error": error,
        "err_msg" : str(err_msg),
        "data": json.loads(dumps(data))
    })

