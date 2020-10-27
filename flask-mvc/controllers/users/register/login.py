from flask import Response, request, jsonify, session
from flask_restful import Resource
from extension import mongo
from bson.json_util import dumps
import json
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import datetime
from werkzeug.security import check_password_hash


class UserLogin(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        user_collection = mongo.db.userRegister
        userId = data["phone_no"]
        psw = data["password"]
        accessToken = None
        userData = user_collection.find_one({"phone_no": userId})
        if userData is not None:
            if check_password_hash(userData["password"], psw) == True:
                id = userData["_id"]
                x = json.loads(dumps(userData))
                expires = datetime.timedelta(hours=8)
                accessToken = create_access_token(
                    identity=str(id), expires_delta=expires)
                msg = "SUCCESS"
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
            "data": x,
            "token": accessToken
        })
