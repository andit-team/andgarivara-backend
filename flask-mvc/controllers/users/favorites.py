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
        uId = bsonO.ObjectId(get_jwt_identity())
        vID = bsonO.ObjectId(data["_id"])
        vData = GetAllVehicleData(vID)
        if vData is not None:
            flag = insertData(vData, vID, uId)
            if flag is not None:
                msg = "SUCCESS"
                error = False
                dataR = flag
            else:
                msg = "FAILED"
                error = True
            return jsonify({
                "msg": msg,
                "error": error,
                "data": json.loads(dumps(flag))
            })
        else:
            return jsonify({
                "msg": "FAILED",
                "error": True,
                "data": json.loads(dumps(data))
            })


def insertData(vData, vID, uId):
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
    return dt


def GetAllVehicleData(vID):
    try:
        dt = mongo.db.vehicles.aggregate(
            [{
                "$match": {
                    "_id": vID,
                    "del_satus": False
                }
            },
                {
                "$lookup": {
                    "from": "vehicle_types",
                    "localField": "vehicle_type",
                    "foreignField": "_id",
                    "as": "vehicle_type_details"
                }
            },
            ])
    except:
        dt = None
    return dt


class DeleteFavorite(Resource):
    @staticmethod
    @jwt_required
    def post() -> Response:
        data = request.get_json()
        uID = bsonO.ObjectId(get_jwt_identity())
        vID = bsonO.ObjectId(data["car_id"])
        try:
            dt = mongo.db.users.update(
                {
                    "_id": uID
                },
                {
                    "$pull": {
                        "bookmarks": {
                            "_id": vID
                        }
                    }
                }
            )
            msg = "SUCCESS"
            error = False
        except:
            msg = "FAILED"
            error = True
            dt = None
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dt))
        })


class FavoriteList(Resource):
    @staticmethod
    @jwt_required
    def post() -> Response:
        data = request.get_json()
        try:
            dt = mongo.db.users.find(
                {
                    "_id": bsonO.ObjectId(get_jwt_identity())
                },
                {
                    "_id": 0,
                    "bookmarks": 1
                }
            )
            msg = "SUCCESS"
            error = False
        except:
            msg = "FAILED"
            error = True
            dt = None
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dt))
        })
