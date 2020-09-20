from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo


class SignUp(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        online_users = mongo.db.users.insert(data)
        return jsonify(message="OK")


class Login(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        user_collection = mongo.db.users
        user = user_collection.find_one(data)
        user["_id"] = str(user["_id"])
        return jsonify({
            "name": user['name'],
            "id": user["_id"]
        })
