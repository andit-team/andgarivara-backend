from bson.json_util import dumps
from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import datetime
import bson
import json
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from werkzeug.security import generate_password_hash


class ProfileEdit(Resource):
    @staticmethod
    @jwt_required
    def put() -> Response:
        data = request.get_json()
        flag = UpdateData(data)
        return flag


def UpdateData(data):
    idU = bson.ObjectId(get_jwt_identity())
    cityID = ""
    if data["city"]:
        cityID= bson.ObjectId(data["city"])
    areaID = ""
    if data["area"]:
        cityID= bson.ObjectId(data["area"])
    err_msg = None
    try:
        update_ = mongo.db.userRegister.update_one(
            {
                "_id": idU
            },
            {
                "$set": {
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "email": data["email"],
                    "country": data["country"],
                    "city":  cityID,
                    "area": areaID,
                    "address": data["address"],
                    "password": generate_password_hash(data["password"]),
                    "phone_no": data["phone_no"],
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
        err_msg = ex
    return jsonify({
        "msg": msg,
        "error": error,
        "err_msg": str(err_msg),
        "data": json.loads(dumps(data))
    })


class ProfileDelete(Resource):
    @staticmethod
    @jwt_required
    def delete() -> Response:
        data = request.get_json()
        flag = DeleteData(data)
        return flag


def DeleteData(data):
    idU = bson.ObjectId(get_jwt_identity())
    err_msg = None
    try:
        update_ = mongo.db.userRegister.update(
            {
                "_id": idU
            },
            {
                "$set": {
                    "del_status": True,
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
        err_msg = ex
    return jsonify({
        "msg": msg,
        "error": error,
        "err_msg": str(err_msg),
        "data": json.loads(dumps(data))
    })
