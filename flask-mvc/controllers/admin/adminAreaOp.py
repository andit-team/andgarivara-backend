from flask import Response, request, jsonify
from flask_restful import Resource
from extension import mongo
import bson.json_util as bsonO
import datetime
import json
from bson.json_util import dumps


class AreaList(Resource):
    @staticmethod
    def get() -> Response:
        data = request.get_json()
        try:
            dt = mongo.db.locationArea.find({})
            msg = "SUCCESS"
            error = False
        except:
            msg = "FAILED"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(dt))
        })


class AddArea(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()

        try:
            dt = mongo.db.locationArea.insert_one(
                {
                    "area": data["area"],
                    "create_date": datetime.datetime.now()
                }
            )
            msg = "SUCCESS"
            error = False
        except:
            msg = "FAILED"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })


class EditArea(Resource):
    @staticmethod
    def put() -> Response:
        data = request.get_json()
        try:
            dt = mongo.db.locationArea.update_one(
                {
                    "_id": bsonO.ObjectId(data["_id"])
                },
                {
                    "$set":
                        {
                            "area": data["area"],
                            "update_date": datetime.datetime.now()
                        }
                }
            )
            msg = "SUCCESS"
            error = False
        except:
            msg = "FAILED"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })


class DeleteArea(Resource):
    @staticmethod
    def delete() -> Response:
        data = request.get_json()
        try:
            dt = mongo.db.locationArea.delete_one(
                {
                    "_id": bsonO.ObjectId(data["_id"])
                }
            )
            msg = "SUCCESS"
            error = False
        except:
            msg = "FAILED"
            error = True
        return jsonify({
            "msg": msg,
            "error": error,
            "data": json.loads(dumps(data))
        })
