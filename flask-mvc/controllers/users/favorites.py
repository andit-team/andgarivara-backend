from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps
from flask_jwt_extended import jwt_required, get_jwt_identity,create_access_token


class AddFavorite(Resource):
    @staticmethod
    @jwt_required
    def post() -> Response:
        data = request.get_json()
        err_msg=None
        uId = bsonO.ObjectId(get_jwt_identity())
        vID = bsonO.ObjectId(data["_id"])
        vData=None
        try:
            vData=mongo.db.vehicles.find({"_id": vID})
            for i in vData:
                title = i["title"]
            dt = mongo.db.users.update(
                {"_id": uId},
                {
                    "$addToSet": {
                        "bookmarks": {
                            "_id": bsonO.ObjectId(),
                            "car_id": vID,
                            "title": title,
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
            err_msg=ex
        return jsonify({
            "msg": msg,
            "error": error,
            "err_msg" : str(err_msg),
            "data": json.loads(dumps(vData))
        })
        


class DeleteFavorite(Resource):
    @staticmethod
    @jwt_required
    def post() -> Response:
        data = request.get_json()
        err_msg=None
        uID = bsonO.ObjectId(get_jwt_identity())
        bId = bsonO.ObjectId(data["_id"])
        try:
            dt = mongo.db.users.update_one(
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
            err_msg=ex
        return jsonify({
            "msg": msg,
            "error": error,
            "err_msg" : str(err_msg),
            "data": json.loads(dumps(data))
        })


class FavoriteList(Resource):
    @staticmethod
    @jwt_required
    def post() -> Response:
        data = request.get_json()
        err_msg=None
        uId = bsonO.ObjectId(get_jwt_identity())
        try:
            dt = mongo.db.users.find_one(
                {
                    "_id":uId 
                },
                {
                    "bookmarks":1
                }
            )
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = "FAILED"
            error = True
            err_msg=ex
            dt = None
        return jsonify({
            "msg": msg,
            "error": error,
            "err_msg" : str(err_msg),
            "data": json.loads(dumps(dt))
        })
