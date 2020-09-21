
from bson.json_util import dumps
from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import datetime
import bson
import json


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
                        "del_date": str(datetime.datetime.now())
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
