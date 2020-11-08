from bson.json_util import dumps
from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import datetime
import bson
import json
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash


class ProfileEdit(Resource):
    @staticmethod
    @jwt_required
    def put() -> Response:
        data = request.get_json()
        flag = UpdateData(data)
        return flag


def UpdateData(data):
    idU = bson.ObjectId(get_jwt_identity()) 
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
                    "default_contact_number":  data["default_contact_number"],
                    "address": data["address"],
                    "profile_pic": data["profile_pic"],
                    "pushNotification": {
                    "on_message_send": data["push_on_message_send"],
                    "on_booking": data["push_on_booking"],
                    "on_suppport_reply": data["push_on_suppport_reply"]
                    },
                    "smsNotification": {
                        "on_message_send": data["sms_on_message_send"],
                        "on_booking": data["sms_on_booking"],
                        "on_suppport_reply": data["sms_on_suppport_reply"]
                    },
                    "update_date": datetime.datetime.now()
                }
            }
        )
        msg = "SUCCESS"
        error = False
    except Exception as ex:
        msg = str(ex)
        error = True
    return jsonify({
        "msg": msg,
        "error": error,
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


class GetUserDataByToken(Resource):
    @staticmethod
    @jwt_required
    def get() -> Response:
        uId = bson.ObjectId(get_jwt_identity())
        try:
            dt = mongo.db.userRegister.find(
                {
                    "_id": uId
                },
                {
                    "password": 0
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
            "data": json.loads(dumps(dt))
        })
        
        
class UpdateUserProfileImage(Resource):
    @staticmethod
    @jwt_required
    def put() -> Response:
        data = request.get_json()
        uId = bson.ObjectId(get_jwt_identity())
        try:
            update_ = mongo.db.userRegister.update_one(
                {
                "_id": uId
                },
                {
                "$set": {
                    "profile_pic": data["profile_pic"],                    
                    "update_date": datetime.datetime.now()
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
        
class ResetPassword(Resource):
    @staticmethod
    @jwt_required
    def put() -> Response:
        data = request.get_json()
        uId = bson.ObjectId(get_jwt_identity())
        try:
            userData = mongo.db.userRegister.find_one({"_id": uId},{"password":1})
            print(userData["password"])
            if check_password_hash(userData["password"], data["oldPassword"]) == True:
                update_ = mongo.db.userRegister.update_one(
                    {
                    "_id": uId
                    },
                    {
                    "$set": {
                        "password": generate_password_hash(data["newPassword"]),                    
                        "update_date": datetime.datetime.now()
                        }
                    }
                    )
                msg = "SUCCESS"
                error = False
            else:
                msg = "Password Didn't match!!!"
                error = True
        except Exception as ex:
            msg = str(ex)
            error = True
            dt = None
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })

