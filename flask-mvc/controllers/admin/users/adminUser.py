
from bson.json_util import dumps
from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import datetime
import bson
import json
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token


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
            dt = mongo.db.userRegister.find({"role":data["role"],"del_status":False})
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

class VerifyDriver(Resource):
    @staticmethod
    @jwt_required
    def put(id) -> Response:
        data = request.get_json()
        try:
            update_ = mongo.db.userRegister.update_one(
                {
                    "del_status": False,
                    "_id": bson.ObjectId(id)
                },
                {
                    "$set": {
                        "driverStatus": data["status"],
                        "status_change_date": datetime.datetime.now()
                    }
                }
            )
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
            dt = None
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })

class DriverList(Resource):
    @staticmethod
    @jwt_required
    def get(status) -> Response:
        msg = ""
        driverList = []
        i=None
        try:
            dt= mongo.db.userRegister.find({"driverStatus": status,"del_status": False})
            print(dt.count())
            for i in dt:
                driverList.append(i)
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(driverList))
        })
