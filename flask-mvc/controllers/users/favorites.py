from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps


class AddFavorite(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        vID = bsonO.ObjectId(data["_id"])
        flag = insertData(vID)
        if flag == True:
            msg = "SUCCESS"
            error = False
            vData = GetAllVehicleData(vID)
        else:
            msg = "FAILED"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(vData))
        })


def insertData(vID):
    dt = mongo.db.users.update(
        {"_id": vID},
        {
            " $push": {
                "bookmarks": vID
            }
        }
    )


def GetAllVehicleData(vID):
    pass


class DeleteFavorite(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        try:

            msg = "SUCCESS"
            error = False
        except:
            msg = "FAILED"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": None
        })
