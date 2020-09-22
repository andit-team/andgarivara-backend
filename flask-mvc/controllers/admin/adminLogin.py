from flask import Response, request, jsonify, session
from flask_restful import Resource
from extension import mongo
from bson.json_util import dumps
import json


class AdminLogin(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        user_collection = mongo.db.users
        adminId = data["phn_no"]
        psw = data["password"]
        adminData = user_collection.find_one({"phn_no": adminId})
        if adminData is not None:
            if adminData["password"] == psw:
                id = adminData["_id"]
                x = json.loads(dumps(adminData))
                msg = "ok"
                error = False
            else:
                x = None
                msg = "User name or password not matched"
                error = True

        else:
            x = None
            msg = "No Admin Found"
            error = True

        return jsonify({
            "msg": msg,
            "error": error,
            "data": x
        })
