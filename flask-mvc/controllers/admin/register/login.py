from flask import Response, request, jsonify, session
from flask_restful import Resource
from extension import mongo
from bson.json_util import dumps
import json
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import datetime
from werkzeug.security import check_password_hash


class AdminLogin(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        admin_collection = mongo.db.adminRegister
        userId = data["phone_no"]
        psw = data["password"]
        adminData = admin_collection.find_one({"phone_no": userId})
        if adminData is not None:
            if check_password_hash(adminData["password"], psw) == True:
                id = adminData["_id"]
                x = json.loads(dumps(adminData))
                msg = "SUCCESS"
                error = False
            else:
                x = None
                msg = "Admin Id or password not matched"
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
