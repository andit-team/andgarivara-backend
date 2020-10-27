from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps
from werkzeug.security import generate_password_hash


class UserSignup(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        err_msg = None
        dt = {
            "phone_no": data["phone_no"],
            "password": generate_password_hash(data["password"]),
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "email": data["email"],
            "role": ["passenger"],
            "create_date": datetime.datetime.now()
        }
        try:
            indexCreate = mongo.db.userRegister.create_index(
                'phone_no', unique=True)
            ins = mongo.db.userRegister.insert_one(dt)
            msg = "Inserted Successfully"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error
        })
