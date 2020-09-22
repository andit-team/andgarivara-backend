
from bson.json_util import dumps
from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import datetime
import bson
import json


class AddUser(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
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
            msg = "SUCCESS"
            error = False
        except:
            msg = "SUCCESS"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dt))
        })


class DeleteUser(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        try:
            delD = mongo.db.users.update(
                {
                    "_id": bson.ObjectId(data["_id"])
                },
                {
                    "$set": {
                        "del_satus": True,
                        "del_resone": "Deleted By Admin",
                        "del_date": datetime.datetime.now()
                    }
                }
            )
            msg = "SUCCESSFULL"
            error = False
        except:
            msg = "Failed"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(delD))
        })


class UserList(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        try:
            dt = mongo.db.users.find({})
            msg = "SUCCESSFULL"
            error = False
        except:
            msg = "Failed"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dt))
        })
