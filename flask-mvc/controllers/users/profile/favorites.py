from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps
from flask_jwt_extended import jwt_required, get_jwt_identity


class AddFavorite(Resource):
    @staticmethod
    @jwt_required
    def post() -> Response:
        data = request.get_json()
        err_msg = None
        uId = bsonO.ObjectId(get_jwt_identity())
        vID = bsonO.ObjectId(data["_id"])
        vData = None
        try:
            vData = mongo.db.vehicles.find({"_id": vID})
            for i in vData:
                title = i["title"]
            dt = mongo.db.userRegister.update(
                {"_id": uId},
                {
                    "$addToSet": {
                        "bookmarks": {
                            "_id": bsonO.ObjectId(),
                            "car_id": vID,
                            "brand": title,
                            "model": title,
                            "bookmark_date": datetime.datetime.now()
                        }
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
            "data": json.loads(dumps(vData))
        })


class DeleteFavorite(Resource):
    @staticmethod
    @jwt_required
    def delete() -> Response:
        data = request.get_json()
        err_msg = None
        uID = bsonO.ObjectId(get_jwt_identity())
        bId = bsonO.ObjectId(data["_id"])
        try:
            dt = mongo.db.userRegister.update_one(
                {
                    "_id": uID
                },
                {
                    "$pull": {
                        "bookmarks": {
                            "_id": bId
                        }
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
            "data": json.loads(dumps(data))
        })


class FavoriteList(Resource):
    @staticmethod
    @jwt_required
    def get() -> Response:
        data = request.get_json()
        uId = bsonO.ObjectId(get_jwt_identity())
        try:
            dt = mongo.db.userRegister.find(
                {
                    "_id": uId
                },
                {
                    "bookmarks": 1,
                    "_id": 0
                }
            )
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = "FAILED"
            error = True
            dt = None
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dt))
        })
