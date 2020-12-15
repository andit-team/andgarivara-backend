from bson.json_util import dumps
from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import datetime
import bson
import json
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
import constants.constantValue as constants


class AddUser(Resource):
    @staticmethod
    @jwt_required
    def post() -> Response:
        data = request.get_json()
        userId = data["phn_no"]
        psw = data["password"]
        err_msg = None
        countUser = 0
        if mongo.db.userRegister.count() > 0:
            countUser = mongo.db.userRegister.find({"phn_no": userId}).count()
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
                ins = mongo.db.userRegister.insert(dt)
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


class DeleteUser(Resource):
    @staticmethod
    @jwt_required
    def delete() -> Response:
        data = request.get_json()
        err_msg = None
        try:
            delD = mongo.db.userRegister.update(
                {
                    "_id": bson.ObjectId(data["_id"])
                },
                {
                    "$set": {
                        "del_status": True,
                        "del_resone": "Deleted By Admin",
                        "del_date": datetime.datetime.now()
                    }
                }
            )
            msg = "SUCCESSFULL"
            error = False
        except Exception as ex:
            msg = "SUCCESS"
            error = True
            err_msg = ex
            delD = None
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(delD))
        })


class UserList(Resource):
    @staticmethod
    @jwt_required
    def post() -> Response:
        data = request.get_json()
        msg = None
        try:
            adminCount = mongo.db.adminRegister.find({"_id": bson.ObjectId(get_jwt_identity())}).count()
            if adminCount == 0:
                return jsonify({
                    "msg": "Your Are not Authenticate Admin",
                    "error": True,
                    "data": None
                })
            dt = mongo.db.userRegister.find({"role": data["role"], "del_status": False})
            msg = "SUCCESSFULL"
            error = False
        except Exception as ex:
            msg = "SUCCESS"
            error = True
            dt = None
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dt))
        })
