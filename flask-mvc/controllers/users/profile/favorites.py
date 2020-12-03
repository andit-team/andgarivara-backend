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
    def put(id) -> Response:
        uId = bsonO.ObjectId(get_jwt_identity())
        vID = bsonO.ObjectId(id)
        vData = None
        try:
            vData = mongo.db.vehicles.find_one({"_id": vID}, {"_id": 1, "vehicleTypeTitle": 1, "brandTitle": 1,
                                                              "model": 1, "manufactureYear": 1})
            vehicleDetails = vData["brandTitle"] + " " + vData["model"] + " " + vData["manufactureYear"]
            dt = mongo.db.userRegister.update(
                {"_id": uId},
                {
                    "$addToSet": {
                        "bookmarks": {
                            "_id": vID,
                            "vehicleTypeTitle": vData["vehicleTypeTitle"],
                            "vehicleDetails": vehicleDetails
                        }
                    }
                }
            )
            msg = "SUCCESS"
            error = False
        except Exception as ex:
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(vData))
        })

class DeleteFavorite(Resource):
    @staticmethod
    @jwt_required
    def delete(id) -> Response:
        data = request.get_json()
        uID = bsonO.ObjectId(get_jwt_identity())
        bId = bsonO.ObjectId(id)
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
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error
        })


class FavoriteList(Resource):
    @staticmethod
    @jwt_required
    def get() -> Response:
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
            msg = str(ex)
            error = True
            dt = None
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dt))
        })
