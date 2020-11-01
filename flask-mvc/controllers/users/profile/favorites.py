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
        uId = bsonO.ObjectId(get_jwt_identity())
        vID = bsonO.ObjectId(data["_id"])
        vData = None
        brandTitle = ""
        vehicle_type = ""
        model = ""
        vehicleTypeId = None
        brandId = None
        try:
            vData = mongo.db.vehicles.find({"_id": vID})
            for i in vData:
                vehicleTypeId = bsonO.ObjectId(i["vehicle_type"])
                brandId = bsonO.ObjectId(i["brand"])
                model = i["model"]
            vTData = mongo.db.vehicleType.find({"_id": vehicleTypeId})
            for i in vTData:
                vehicle_type = i["title"]
                brands = i["brands"]
                for i in brands:
                    if bsonO.ObjectId(i["_id"]) == brandId:
                        brandTitle = i["brand"]
                        print(brandTitle)

            dt = mongo.db.userRegister.update(
                {"_id": uId},
                {
                    "$addToSet": {
                        "bookmarks": {
                            "_id": bsonO.ObjectId(),
                            "car_id": vID,
                            "vehicle_type": vehicle_type,
                            "brand": brandTitle,
                            "model": model,
                            "bookmark_date": datetime.datetime.now()
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
    def delete() -> Response:
        data = request.get_json()
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
            msg = str(ex)
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
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
