from flask import Response, request, jsonify, session
from flask_restful import Resource
from extension import mongo
from bson.json_util import dumps
import json


class UserLogin(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        user_collection = mongo.db.users
        userId = data["phn_no"]
        psw = data["password"]
        userData = user_collection.find_one({"phn_no": userId})
        if userData is not None:
            if userData["password"] == psw:
                id = userData["_id"]
                x = json.loads(dumps(userData))
                msg = "ok"
                error = False
            else:
                x = None
                msg = "User name or password not matched"
                error = True

        else:
            x = None
            msg = "No User Found"
            error = True

        return jsonify({
            "msg": msg,
            "error": error,
            "data": x
        })
