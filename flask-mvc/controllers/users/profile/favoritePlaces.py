from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps
from flask_jwt_extended import jwt_required, get_jwt_identity


class AddFavoritePlace(Resource):
    @staticmethod
    @jwt_required
    def put() -> Response:
        data = request.get_json()
        uId = bsonO.ObjectId(get_jwt_identity())
        try:
            dt = mongo.db.userRegister.update(
                {"_id": uId},
                {
                    "$addToSet": {
                        "favoritePlaces": {
                            "_id": bsonO.ObjectId(),
                            "placeTitle": data["placeTitle"],
                            "placeAddress": data["placeAddress"],
                            "location": data["location"]
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

class DeleteFavoritePlace(Resource):
    @staticmethod
    @jwt_required
    def delete(id) -> Response:
        try:
            dt = mongo.db.userRegister.update_one(
                {
                    "_id": bsonO.ObjectId(get_jwt_identity())
                },
                {
                    "$pull": {
                        "favoritePlaces": {
                            "_id": bsonO.ObjectId(id)
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


class FavoritePlaceList(Resource):
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
                    "favoritePlaces": 1,
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
